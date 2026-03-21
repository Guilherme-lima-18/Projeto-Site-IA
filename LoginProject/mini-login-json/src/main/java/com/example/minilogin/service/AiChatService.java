package com.example.minilogin.service;

import com.example.minilogin.dto.ChatRequest;
import com.example.minilogin.dto.ChatResponse;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

@Service
public class AiChatService {

    private final RestClient restClient;

    public AiChatService(RestClient restClient) {
        this.restClient = restClient;
    }

    public String askAi(String message) {
        try {
            ChatResponse response = restClient.post()
                    .uri("/chat")
                    .body(new ChatRequest(message))
                    .retrieve()
                    .body(ChatResponse.class);

            if (response == null || response.getResponse() == null || response.getResponse().isBlank()) {
                return "A IA não retornou resposta.";
            }

            return response.getResponse();
        } catch (Exception e) {
            return "Não foi possível se comunicar com a IA Python no momento.";
        }
    }
}