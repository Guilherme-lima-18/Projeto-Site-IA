package com.example.minilogin.repository;

import com.example.minilogin.model.User;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Repository;

import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Repository
public class JsonUserRepository {

    private final Path filePath;

    public JsonUserRepository(@Value("${app.data.file}") String fileName) {
        this.filePath = Paths.get(fileName);
        initializeFile();
    }

    private void initializeFile() {
        try {
            if (!Files.exists(filePath)) {
                Files.createFile(filePath);
            }
        } catch (IOException e) {
            throw new RuntimeException("Erro ao criar arquivo de usuários", e);
        }
    }

    public synchronized List<User> findAll() {
        List<User> users = new ArrayList<>();

        try {
            List<String> lines = Files.readAllLines(filePath);

            for (String line : lines) {
                if (line.isBlank()) {
                    continue;
                }

                String[] parts = line.split(";", 4);

                if (parts.length < 4) {
                    continue;
                }

                User user = new User();
                user.setId(Long.parseLong(parts[0]));
                user.setName(parts[1]);
                user.setEmail(parts[2]);
                user.setPasswordHash(parts[3]);

                users.add(user);
            }

            return users;
        } catch (IOException e) {
            throw new RuntimeException("Erro ao ler arquivo de usuários", e);
        }
    }

    public synchronized Optional<User> findByEmail(String email) {
        return findAll()
                .stream()
                .filter(user -> user.getEmail().equalsIgnoreCase(email))
                .findFirst();
    }

    public synchronized User save(User user) {
        List<User> users = findAll();

        if (user.getId() == null) {
            long nextId = users.stream()
                    .mapToLong(User::getId)
                    .max()
                    .orElse(0L) + 1;
            user.setId(nextId);
        }

        String line = user.getId() + ";" +
                user.getName() + ";" +
                user.getEmail() + ";" +
                user.getPasswordHash();

        try (BufferedWriter writer = Files.newBufferedWriter(
                filePath,
                StandardOpenOption.APPEND
        )) {
            writer.write(line);
            writer.newLine();
            return user;
        } catch (IOException e) {
            throw new RuntimeException("Erro ao salvar usuário", e);
        }
    }
}