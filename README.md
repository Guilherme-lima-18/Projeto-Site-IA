# 🤖 AI Website Project - Spring Boot + Python

## 📌 About the project

This project is a web application that integrates a **Spring Boot backend** with an **Artificial Intelligence service in Python**, enabling communication between the user and an AI model through HTTP requests.

The application simulates how modern AI systems work (like ChatGPT), where the frontend sends messages to the Java backend, which then communicates with an AI service and returns responses to the user.

📚 **This project was developed as part of a college assignment**, aiming to apply backend development concepts and AI integration in a practical scenario.

---

## 🚀 Technologies Used

### 🔧 Backend

* Java 17+
* Spring Boot
* Spring Web

### 🤖 Artificial Intelligence

* Python
* Flask
* (Possible use of local models via Ollama or external APIs)

### 🌐 Frontend

* HTML
* CSS
* JavaScript

---

## 🧠 System Architecture

The project follows a service-based communication architecture:

1. The user sends a message through the frontend
2. Spring Boot receives the request (Controller)
3. The backend forwards the message to the Python AI service
4. The AI processes the request and returns a response
5. The backend sends the response back to the frontend

---

## 🔄 Application Flow

```text
Frontend → Spring Boot → Python AI API → Response → Frontend
```

---

## 📂 Project Structure

### Backend (Spring Boot)

* `controller` → handles HTTP requests
* `service` → business logic
* `model/dto` → data structure

### AI (Python)

* `app.py` → Flask server with AI endpoints

---

## ▶️ How to Run the Project

### 🔹 Backend (Spring Boot)

1. Open the project in IntelliJ
2. Run the application
3. The server will start at:

```
http://localhost:8080
```

---

### 🔹 AI (Python)

1. Install dependencies:

```bash
pip install flask
```

2. Run the server:

```bash
python app.py
```

3. The service will be available at:

```
http://localhost:5000
```

---

## 📡 Example Request

### Endpoint:

```
POST /chat
```

### Request Body (JSON):

```json
{
  "message": "Hello, AI!"
}
```

### Response:

```json
{
  "response": "Hello! How can I help you?"
}
```

---

## 💡 Project Goals

This project was developed to:

* Practice integration between different languages (Java + Python)
* Understand how REST APIs work in real-world scenarios
* Simulate real systems that use Artificial Intelligence
* Improve backend and system architecture skills

---

## 🚀 Future Improvements

* Integration with more advanced AI models
* More interactive user interface
* User authentication
* Cloud deployment

---

## 👨‍💻 Author

Developed by Guilherme Lima
🔗 GitHub: https://github.com/Guilherme-lima-18

---

## ⭐ Notes

This project is part of my learning journey in backend development and Artificial Intelligence integration.
