package com.example.minilogin.Controller;

import com.example.minilogin.dto.LoginRequest;
import com.example.minilogin.dto.RegisterRequest;
import jakarta.servlet.http.HttpSession;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class PageController {

    @GetMapping("/")
    public String root(HttpSession session) {
        if (session.getAttribute("loggedUser") != null) {
            return "redirect:/home";
        }
        return "redirect:/login";
    }

    @GetMapping("/login")
    public String loginPage(Model model, HttpSession session) {
        if (session.getAttribute("loggedUser") != null) {
            return "redirect:/home";
        }

        model.addAttribute("loginRequest", new LoginRequest());
        return "login";
    }

    @GetMapping("/register")
    public String registerPage(Model model, HttpSession session) {
        if (session.getAttribute("loggedUser") != null) {
            return "redirect:/home";
        }

        model.addAttribute("registerRequest", new RegisterRequest());
        return "register";
    }

    @GetMapping("/home")
    public String homePage(HttpSession session, Model model) {
        Object user = session.getAttribute("loggedUser");

        if (user == null) {
            return "redirect:/login";
        }

        model.addAttribute("userName", user);
        return "home";
    }
}