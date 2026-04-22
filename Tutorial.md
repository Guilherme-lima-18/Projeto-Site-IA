# 🚀 Tutorial - Como rodar o projeto de Chat com IA

Este guia vai te ajudar a configurar e rodar o projeto localmente no seu computador.

---

## 📋 Pré-requisitos

Antes de começar, certifique-se de que você tem os seguintes softwares instalados:

- Java 17 ou superior
- Maven
- MySQL Server
- Git
- Navegador (Google Chrome recomendado)

(Opcional)
- Node.js (caso utilize frontend separado)

---

## 📦 1. Clonar o projeto

Abra o terminal e execute:

```bash

git clone <URL_DO_REPOSITORIO>
cd nome-do-projeto

2. Configurar o banco de dados (MySQL)
Abra o MySQL
Crie um banco de dados com o comando:
CREATE DATABASE chat_ai;
Configure o arquivo application.properties ou application.yml com suas credenciais:
spring.datasource.url=jdbc:mysql://localhost:3306/chat_ai
spring.datasource.username=SEU_USUARIO
spring.datasource.password=SUA_SENHA

spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
🧱 3. Rodar o backend (Spring Boot)

No terminal, dentro da pasta do projeto, execute:

mvn spring-boot:run

Ou, se estiver usando o wrapper do Maven:

./mvnw spring-boot:run
🌐 4. Acessar o sistema

Após iniciar o servidor, abra o navegador e acesse:

http://localhost:8080
