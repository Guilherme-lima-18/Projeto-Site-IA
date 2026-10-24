# 🚀 Projeto Site IA — Guia de instalação

Site com **login** e **chat de IA** (a chatbot "Aisha"). Este guia leva você do
`git clone` até o site rodando no navegador.

---

## 🧩 Como o projeto é montado

São **três peças** que conversam entre si:

```
Navegador  →  Spring Boot (Java)  →  Flask (Python)  →  OpenAI
              porta 8080             porta 5000            ↓
              login + páginas        cérebro do chat    MySQL (memória)
                                                        porta 3306
```

- **Spring Boot** (`LoginProject/mini-login-json`) — login, cadastro e as páginas do site. Os usuários ficam num arquivo de texto (`users.txt`), **não** no banco.
- **Flask** (`src/main/java/com/example/minilogin/app.py`) — recebe a mensagem, chama a OpenAI e guarda resumos da conversa no MySQL.
- **MySQL** — só a memória de longo prazo da IA.

> ⚠️ **As três peças precisam estar rodando.** Se você subir só o Java, o chat
> responde *"Não foi possível se comunicar com a IA Python no momento."*

---

## ✅ O que você precisa antes de começar

### Caminho A — Docker (recomendado, muito mais simples)

| Software | Observação |
|---|---|
| [Git](https://git-scm.com/downloads) | para clonar |
| [Docker Desktop](https://www.docker.com/products/docker-desktop/) | já traz o `docker compose` |
| Chave da API da OpenAI | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) — é **paga**, precisa de créditos |

Não precisa instalar Java, Maven, Python nem MySQL — tudo roda dentro dos containers.

### Caminho B — Instalação manual

| Software | Versão |
|---|---|
| Git | qualquer |
| **JDK 25** | obrigatório (o projeto usa Java 25 + Spring Boot 4) |
| **Python 3.10+** | com `pip` |
| **MySQL Server 8+** | rodando localmente |
| Chave da API da OpenAI | idem acima |

Maven **não** precisa instalar: o projeto já vem com o wrapper (`mvnw`).

---

## 📦 1. Clonar o projeto

```bash
git clone <URL_DO_REPOSITORIO>
cd Projeto-Site-IA/LoginProject/mini-login-json
```

> 📌 Todos os comandos deste guia são executados dentro de
> **`LoginProject/mini-login-json`** — é onde ficam o `pom.xml` e o `docker-compose.yml`.

---

## 🔑 2. Criar o arquivo `.env` (obrigatório nos dois caminhos)

O `.env` guarda a chave da OpenAI e a senha do banco. Ele **não vem no clone**
(está no `.gitignore`, por segurança), então você precisa criar o seu:

**Windows (PowerShell / CMD):**
```powershell
copy .env.example .env
```

**Linux / macOS:**
```bash
cp .env.example .env
```

Abra o `.env` e preencha:

```env
OPENAI_API_KEY=sk-sua_chave_real_aqui
DB_PASSWORD=uma_senha_qualquer_que_voce_escolher
DB_NAME=aisha_memory
```

> ❗ Sem a `OPENAI_API_KEY` o site abre e o login funciona, mas o chat não responde.
> ❗ Nunca comite o `.env`. Se sua chave vazar, revogue-a na OpenAI e gere outra.

---

## 🐳 Caminho A — Rodar com Docker

### 3A. Subir tudo

```bash
docker compose up -d --build
```

A primeira vez demora alguns minutos (baixa o Java, o Python e o MySQL).

### 4A. Conferir se subiu

```bash
docker compose ps
```

Você deve ver os três containers em `Up` — `aisha-mysql` (healthy), `aisha-ai` e `mini-login`.

### 5A. Acessar

👉 **http://localhost:8080**

Crie uma conta em *Cadastrar*, faça login e use o chat.

### Comandos do dia a dia

```bash
docker compose logs -f app       # logs do Java
docker compose logs -f ai        # logs da IA Python
docker compose restart ai        # reiniciar só a IA
docker compose down              # desligar tudo
docker compose down -v           # desligar E apagar banco + usuários (reset total)
docker compose up -d --build     # rebuildar depois de mexer no código
```

### Portas usadas

| Serviço | Porta no seu PC |
|---|---|
| Site (Spring Boot) | `8080` |
| IA (Flask) | `5000` |
| MySQL | **`3307`** (3307 de propósito, pra não conflitar com um MySQL que você já tenha) |

---

## 🔧 Caminho B — Rodar manualmente (sem Docker)

Aqui você abre **dois terminais** e precisa do MySQL já instalado e rodando.

### 3B. Preparar o MySQL

Não precisa criar o banco na mão — o `app.py` cria o banco e a tabela sozinho no
primeiro start. Só garanta que:

- o MySQL está rodando na porta `3306`;
- as credenciais no `.env` (`DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`) estão corretas;
- o usuário tem permissão para criar bancos.

### 4B. Terminal 1 — subir a IA (Python)

```bash
# criar e ativar um ambiente virtual
python -m venv .venv

# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# instalar as dependências
pip install -r requirements-ai.txt

# rodar
python src/main/java/com/example/minilogin/app.py
```

Esperado no terminal: `[OK] Banco de dados MySQL inicializado com sucesso.` e o
Flask ouvindo na porta `5000`. **Deixe este terminal aberto.**

### 5B. Terminal 2 — subir o site (Java)

```bash
# Windows:
mvnw.cmd spring-boot:run

# Linux/macOS:
./mvnw spring-boot:run
```

### 6B. Acessar

👉 **http://localhost:8080**

---

## 🆘 Problemas comuns

| Sintoma | Causa / solução |
|---|---|
| Chat responde *"Não foi possível se comunicar com a IA Python"* | O Flask não está rodando (ou morreu). Veja `docker compose logs ai`, ou o Terminal 1 no caminho manual. |
| Chat responde *"Usuário não autenticado."* | Você não está logado. Faça login novamente — a sessão expira. |
| `port is already allocated` / `Web server failed to start. Port 8080 was already in use` | Algo já usa a 8080 (outra instância do projeto?). Feche o outro processo ou troque a porta em `docker-compose.yml` (ex.: `"8081:8080"`). |
| MySQL não sobe no Docker | `DB_PASSWORD` está vazio no `.env`. Preencha e rode `docker compose down -v` + `up -d`. |
| Logs da IA mostram `Access denied for user 'root'` | Você mudou a `DB_PASSWORD` **depois** do primeiro start. O MySQL só aplica a senha quando cria o banco pela primeira vez, e `docker compose down` preserva o volume. Rode `docker compose down -v` e suba de novo. |
| `aisha-ai` fica em `Restarting` | Quase sempre é o banco: veja `docker compose logs ai` e confira a linha de erro (senha, host ou chave da OpenAI). |
| Erro de autenticação da OpenAI (`401` / `invalid_api_key`) nos logs da IA | Chave errada, expirada ou sem créditos na conta. |
| `release 25 not supported` no build Java | Seu JDK é antigo. Instale o **JDK 25** (ou use o caminho Docker, que não depende do seu Java). |
| Esqueci a senha / quero limpar os usuários | Docker: `docker compose down -v`. Manual: apague o arquivo `users.txt`. |

---

## 📝 Notas

- **Login não usa banco de dados.** Os usuários ficam em `users.txt` (senhas com hash BCrypt). O MySQL é exclusivamente a memória do chatbot.
- No Docker, o `users.txt` fica num volume (`app-data`), então sobrevive a `docker compose down` — mas é apagado por `down -v`.
- O Flask roda com o servidor de desenvolvimento (`debug=True`). Para produção, troque por um WSGI como gunicorn e desligue o debug.
- A IA resume a conversa a cada 5 mensagens e salva o resumo no MySQL — é assim que ela "lembra" de você entre conversas.
