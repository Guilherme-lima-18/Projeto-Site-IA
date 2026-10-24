# ============================================================
#  Backend Spring Boot (mini-login-json) - Java 25
# ============================================================

# ---------- Etapa 1: build ----------
FROM maven:3.9-eclipse-temurin-25 AS build
WORKDIR /build

# Baixa as dependencias primeiro (aproveita o cache do Docker)
COPY pom.xml .
RUN mvn -B dependency:go-offline

# Compila o jar
COPY src ./src
RUN mvn -B clean package -DskipTests

# ---------- Etapa 2: runtime ----------
FROM eclipse-temurin:25-jre-alpine
WORKDIR /app

# Usuario sem privilegios
RUN addgroup -S spring && adduser -S spring -G spring

COPY --from=build /build/target/*.jar app.jar

# Pasta onde fica o users.txt (login em JSON)
RUN mkdir -p /app/data && chown -R spring:spring /app
USER spring

ENV JAVA_OPTS=""
EXPOSE 8080

ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar /app/app.jar"]
