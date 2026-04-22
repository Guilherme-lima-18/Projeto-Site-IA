# ============================================================
#  app.py  –  Aisha Chatbot  |  OpenAI + MySQL
# ============================================================

# Flask Imports
from flask import Flask, request, jsonify
from flask_cors import CORS

# OpenAI
from openai import OpenAI

# MySQL
import mysql.connector
from mysql.connector import Error

# Outros
import atexit
import os

from dotenv import load_dotenv
load_dotenv()

# ============================================================
# Configurações  –  edite aqui ou use variáveis de ambiente
# ============================================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "SUA_CHAVE_AQUI")

DB_CONFIG = {
    "host":     os.getenv("DB_HOST",     "localhost"),
    "port":     int(os.getenv("DB_PORT", "3306")),
    "user":     os.getenv("DB_USER",     "root"),
    "password": os.getenv("DB_PASSWORD", "sua_senha_aqui"),
    "database": os.getenv("DB_NAME",     "aisha_memory"),
}

# ============================================================
# Variáveis Globais
# ============================================================
global_context = []
BOT_NAME   = "Aisha"
CHAT_MODEL = "gpt-4o-mini"   # troque por "gpt-4o" se quiser o modelo maior
MAX_HISTORY = 5

PERSONALITY = (
    "Você é uma IA sarcástica e espirituosa com paixão por ficção científica, cyberpunk e videogames retrô. "
    "Seu principal objetivo é proporcionar conversas envolventes e divertidas para os usuários."
)

# ============================================================
# Cliente OpenAI
# ============================================================
client = OpenAI(api_key=OPENAI_API_KEY)

# ============================================================
# Banco de dados MySQL  –  cria tabela se não existir
# ============================================================
def get_db_connection():
    """Abre e retorna uma conexão MySQL."""
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn

def init_db():
    """Cria o banco e a tabela de memórias caso não existam."""
    try:
        # Primeiro conecta sem especificar o banco para poder criá-lo
        init_config = {k: v for k, v in DB_CONFIG.items() if k != "database"}
        conn = mysql.connector.connect(**init_config)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_CONFIG['database']}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        conn.commit()
        cursor.close()
        conn.close()

        # Agora conecta ao banco correto e cria a tabela
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversation_summaries (
                id         INT AUTO_INCREMENT PRIMARY KEY,
                summary    TEXT         NOT NULL,
                created_at TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("[OK]  Banco de dados MySQL inicializado com sucesso.")
    except Error as e:
        print(f"❌  Erro ao inicializar o banco de dados: {e}")
        raise

# ============================================================
# Funções de Memória (MySQL)
# ============================================================
def save_summary(summary: str):
    """Salva um resumo de conversa no MySQL."""
    try:
        conn   = get_db_connection()
        cursor = conn.cursor()
        # Evita duplicatas exatas
        cursor.execute("SELECT id FROM conversation_summaries WHERE summary = %s LIMIT 1", (summary,))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO conversation_summaries (summary) VALUES (%s)", (summary,))
            conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print(f"[ERRO]  Erro ao salvar resumo: {e}")

def load_memory() -> str:
    """Carrega todos os resumos armazenados no MySQL."""
    try:
        conn   = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT summary FROM conversation_summaries ORDER BY created_at ASC")
        rows   = cursor.fetchall()
        cursor.close()
        conn.close()
        return "\n".join(row[0] for row in rows)
    except Error as e:
        print(f"[ERRO]  Erro ao carregar memória: {e}")
        return ""

# ============================================================
# Função de Sumarização (OpenAI)
# ============================================================
def summarize_events(history: list[str]) -> str:
    """Resume o histórico recente usando a OpenAI para criar um snapshot de memória."""
    history_text = "\n".join(history)
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        temperature=0.3,
        max_tokens=200,
        messages=[
            {
                "role": "user",
                "content": (
                    "Resuma o seguinte histórico de conversa em um parágrafo, "
                    "focando apenas em eventos importantes e detalhes relevantes. Ignore conversa fiada. "
                    "Retorne apenas o resumo, nada mais.\n\n"
                    f"Histórico:\n{history_text}"
                ),
            }
        ],
    )
    return response.choices[0].message.content.strip()

# ============================================================
# API Flask
# ============================================================
app = Flask(__name__)
CORS(app)   # Permite acesso do frontend (ex: http://localhost:8080)

@app.route("/chat", methods=["POST"])
def chat():
    global global_context

    # 1. Ler mensagem do usuário
    data       = request.get_json()
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"response": "Nenhuma mensagem fornecida."}), 400

    # 2. Adicionar ao contexto temporário
    global_context.append({"role": "user", "content": user_input})

    # 3. Sumarizar e limpar quando atingir o limite
    if len(global_context) >= MAX_HISTORY:
        history_text = [
            f"{'Usuário' if m['role'] == 'user' else BOT_NAME}: {m['content']}"
            for m in global_context
        ]
        summary = summarize_events(history_text)
        save_summary(summary)
        global_context.clear()
        global_context.append({"role": "user", "content": user_input})

    # 4. Montar memória de longo prazo
    memory = load_memory()

    # 5. Construir o system prompt com personalidade + memória
    system_prompt = (
        f"Você é {BOT_NAME}, um chatbot com uma personalidade marcante.\n\n"
        f"{PERSONALITY}\n\n"
        f"Isso é o que você lembra do usuário:\n{memory if memory else 'Nada ainda.'}\n\n"
        "Seja breve e direto. Mantenha sua resposta em uma ou duas frases. Responda sempre em português."
    )

    # 6. Chamar a API da OpenAI
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        temperature=0.7,
        max_tokens=150,
        messages=[
            {"role": "system", "content": system_prompt},
            *global_context,  # histórico recente
        ],
    )

    ai_response = response.choices[0].message.content.strip()

    # 7. Adicionar resposta da IA ao contexto
    global_context.append({"role": "assistant", "content": ai_response})

    # 8. Retornar JSON
    return jsonify({"response": ai_response})


# ============================================================
# Auto-save ao encerrar o servidor
# ============================================================
def on_exit():
    if global_context:
        history_text = [
            f"{'Usuário' if m['role'] == 'user' else BOT_NAME}: {m['content']}"
            for m in global_context
        ]
        save_summary(summarize_events(history_text))

atexit.register(on_exit)

# ============================================================
# Entry Point
# ============================================================
if __name__ == "__main__":
    init_db()   # Garante que o banco e a tabela existam
    print(f"  Iniciando servidor Flask com OpenAI ({CHAT_MODEL}) + MySQL...")
    app.run(host="0.0.0.0", port=5000, debug=True)