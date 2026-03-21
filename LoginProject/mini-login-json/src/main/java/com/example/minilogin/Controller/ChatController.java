package com.example.minilogin.Controller;

import com.example.minilogin.dto.ChatRequest;
import com.example.minilogin.dto.ChatResponse;
import com.example.minilogin.service.AiChatService;
import jakarta.servlet.http.HttpSession;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/chat")
public class ChatController {

    private final AiChatService aiChatService;

    public ChatController(AiChatService aiChatService) {
        this.aiChatService = aiChatService;
    }

    @PostMapping
    public ChatResponse chat(@RequestBody ChatRequest request, HttpSession session) {
        System.out.println("ChatController recebeu: " + request.getMessage());

        Object user = session.getAttribute("loggedUser");

        if (user == null) {
            return new ChatResponse("Usuário não autenticado.");
        }

        if (request == null || request.getMessage() == null || request.getMessage().isBlank()) {
            return new ChatResponse("Mensagem vazia.");
        }

        String response = aiChatService.askAi(request.getMessage());
        return new ChatResponse(response);
    }
}