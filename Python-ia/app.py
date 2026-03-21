# Flask Imports
from flask import Flask, request, jsonify
from flask_cors import CORS

# Imports da IA
import atexit
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from tinydb import TinyDB, Query

#Database Setup
db = TinyDB("memory.json")
UserData = Query()

#Global Variables
global_context = []
BOT_NAME = "Aisha"
PERSONALITY = """
You are a sarcastic and witty AI with a love for sci-fi, cyberpunk, and retro video games.
Your main goal is to provide engaging and entertaining conversations for users.
"""

#Prompt Template
template = """
You are {bot_name}, a chatbot with a distinct personality.

{personality}

Here is what you remember about the user: {memory}

Here is the recent conversation history: {context}

Question: {question}

Be brief and to the point. Keep your response up to one sentence.
"""

#Model Setup
model = OllamaLLM(
    model="mistral:7b",
    temperature=0.7,
    max_tokens=100
)

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

MAX_HISTORY = 5

#Summarization Function
def summarize_events(history):
    """
    Summarize the last few messages to create a memory snapshot.
    """
    summary_prompt = ChatPromptTemplate.from_template("""
    Summarize the following conversation history in one paragraph, focusing only on key events and important details.
    Ignore small talk. Do not return anything else than the summary itself.

    History:
    {history}

    Summary:
    """)
    summary_chain = summary_prompt | model
    summary = summary_chain.invoke({"history": "\n".join(history)})

    return summary.content.strip() if hasattr(summary, "content") else str(summary).strip()

#Memory Save/Load Functions
def save_summary(summary):
    """Store summary in the database."""
    if not db.contains(UserData.summary == summary):
        db.insert({"summary": summary})

def load_memory():
    """Load all stored conversation summaries from the database."""
    return "\n".join([entry["summary"] for entry in db.all()])

#API Setup
app = Flask(__name__)
# Permite CORS para que o seu frontend (p. ex., http://localhost:8080) possa acessar a API
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    global global_context

    # 1. Obter a mensagem do usuário do corpo da requisição JSON
    data = request.get_json()
    user_input = data.get('message', '').strip()

    if not user_input:
        return jsonify({"response": "No message provided."}), 400

    # 2. Processamento da IA (similar à função handle_conversation)
    global_context.append(f"User: {user_input}")

    message_count = len(global_context)
    # O contador será o tamanho do global_context, já que ele é limpo após o resumo.

    if message_count >= MAX_HISTORY:
        summary = summarize_events(global_context)
        save_summary(summary)
        global_context.clear() # Limpa o contexto temporário
        # O user_input foi adicionado acima, precisamos re-adicionar a última mensagem
        # após a limpeza para que ela não seja perdida.
        global_context.append(f"User: {user_input}")

    memory = load_memory() # Carrega a memória de longo prazo

    # 3. Chamar a cadeia da LangChain/Ollama
    result = chain.invoke({
        "bot_name": BOT_NAME,
        "personality": PERSONALITY,
        "memory": memory,
        "context": "\n".join(global_context),
        "question": user_input
    })

    ai_response = result.content if hasattr(result, "content") else str(result)

    # 4. Adicionar a resposta da IA ao contexto (para o próximo ciclo)
    global_context.append(f"{BOT_NAME}: {ai_response}")

    # 5. Retornar a resposta em formato JSON
    return jsonify({"response": ai_response})

# === Auto-save on Exit (mantido, mas só funciona ao desligar o servidor Flask) ===
atexit.register(lambda: save_summary(summarize_events(global_context)) if global_context else None)

# === Entry Point da API ===
if __name__ == "__main__":
    # Rodar o servidor Flask. Host '0.0.0.0' permite acesso externo.
    # Mantenha a porta 5000 por convenção ou mude se necessário.
    print(f"Starting Flask server...")
    app.run(host='0.0.0.0', port=5000, debug=True)