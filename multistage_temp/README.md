markdown_content = """# 🐳 Universal Docker Multi-Stage Build Guide & Cheat Sheet

Welcome to the ultimate baseline guide for containerizing applications. This repository contains a universal standard operating procedure (SOP) and copy-paste templates for building production-grade `Dockerfile`s from scratch.

---

## 📑 Table of Contents
1. [Phase 1: Pre-Flight Investigation Checklist](#-phase-1-the-pre-flight-investigation-checklist)
2. [Phase 2: Universal Multi-Stage Mental Model](#-phase-2-the-universal-multi-stage-mental-model)
3. [Phase 3: Language-Specific Templates](#-phase-3-language-specific-production-templates)
    - [Go](#go)
    - [Node.js (Backend API)](#nodejs-backend-api)
    - [React / Vue / Vite (Frontend)](#react--vue--vite-frontend)
    - [Java (Maven)](#java-maven)
    - [Python](#python-standard-pip)
    - [C# / .NET](#c--net)
    - [Rust](#rust)
4. [Phase 4: ENV vs CMD vs ENTRYPOINT](#-phase-4-env-vs-cmd-vs-entrypoint-detection)
5. [Phase 5: Production Best Practices](#-phase-5-production-best-practices-checklist)

---

## 🛠️ Phase 1: The Pre-Flight Investigation Checklist
Before touching a `Dockerfile`, answer these 5 questions to determine your build strategy.

### 1. What language/framework is this?
Look at the root of the repository for these signature dependency files:

| Technology | Dependency File | Output Artifact |
| :--- | :--- | :--- |
| **Go** | `go.mod` | Binary executable |
| **Node.js** | `package.json` | `dist/` or `build/` folder |
| **Java (Maven)** | `pom.xml` | `.jar` or `.war` file |
| **Java (Gradle)**| `build.gradle` | `.jar` file |
| **Python** | `requirements.txt` | Source files |
| **Python (Poetry)**| `pyproject.toml` | Source files |
| **Rust** | `Cargo.toml` | Binary executable |
| **C# / .NET** | `*.csproj` | `.dll` and assets |
| **PHP** | `composer.json` | Source files |
| **Ruby** | `Gemfile` | Source files |

### 2. How are dependencies installed?
- `go mod download`
- `npm install` / `yarn install`
- `pip install -r requirements.txt`
- `mvn dependency:resolve` (or `go-offline`)
- `cargo fetch`

### 3. How is the application built? (Stage 1)
- `go build -o app .`
- `npm run build`
- `mvn clean package`
- `cargo build --release`

### 4. How does it start? (Stage 2)
- `./app`
- `java -jar app.jar`
- `node dist/index.js`
- `python app.py`

---

## 🏗️ Phase 2: The Universal Multi-Stage Mental Model
Multi-stage builds separate the "compilation" environment (heavy, full of tools) from the "runtime" environment (lightweight, secure). 

```dockerfile
# ==========================================
# STAGE 1: BUILD (Heavyweight)
# ==========================================
FROM build-image AS builder
WORKDIR /app

# Step A: Cache dependencies first (Best Practice)
COPY dependency-files .
RUN install-dependencies

# Step B: Copy source code and compile
COPY . .
RUN build-command

# ==========================================
# STAGE 2: RUNTIME (Lightweight)
# ==========================================
FROM runtime-image
WORKDIR /app

# Step C: Copy ONLY the compiled output from Stage 1
COPY --from=builder /app/output-artifact .

EXPOSE 8080
ENTRYPOINT ["run-command"]
```


## 💻 Phase 3: Language-Specific Production Templates

Go
Identify: go.mod, go.sum | Build: go build

```Dockerfile
FROM golang:1.24-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN go build -o app .

FROM alpine
WORKDIR /app
COPY --from=builder /app/app .
EXPOSE 8080
ENTRYPOINT ["./app"]
```

Node.js (Backend API)
Identify: package.json, package-lock.json | Build: npm run build

```Dockerfile
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM node:22-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node","dist/index.js"]
```

React / Vite (Frontend)
Build Output: dist/

```Dockerfile
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx","-g","daemon off;"]
```

Java (Maven)
Identify: pom.xml | Build: mvn package | Output: target/*.jar

```Dockerfile
FROM maven:3.9-eclipse-temurin-21 AS builder
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline
COPY . .
RUN mvn clean package

FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=builder /app/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java","-jar","app.jar"]
```

Java (Gradle)
Identify: build.gradle | Build: gradle build

```Dockerfile
FROM gradle:jdk21 AS builder
WORKDIR /app
COPY . .
RUN gradle build

FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=builder /app/build/libs/*.jar app.jar
ENTRYPOINT ["java","-jar","app.jar"]
```

Python (Standard PIP)
Identify: requirements.txt

```Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python","app.py"]
```

# FastAPI Example: CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]
Python (Poetry)
Identify: pyproject.toml

```Dockerfile
FROM python:3.12-slim
WORKDIR /app
RUN pip install poetry
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root
COPY . .
CMD ["poetry","run","python","main.py"]
```

Rust
Identify: Cargo.toml | Build: cargo build --release

```Dockerfile
FROM rust:latest AS builder
WORKDIR /app
COPY . .
RUN cargo build --release

FROM debian:bookworm-slim
WORKDIR /app
COPY --from=builder /app/target/release/app .
ENTRYPOINT ["./app"]
```

C# / .NET
Identify: *.csproj | Build: dotnet publish

```Dockerfile
FROM [mcr.microsoft.com/dotnet/sdk:9.0](https://mcr.microsoft.com/dotnet/sdk:9.0) AS build
WORKDIR /src
COPY . .
RUN dotnet publish -c Release -o /app

FROM [mcr.microsoft.com/dotnet/aspnet:9.0](https://mcr.microsoft.com/dotnet/aspnet:9.0)
WORKDIR /app
COPY --from=build /app .
ENTRYPOINT ["dotnet","MyApp.dll"]
```

PHP Laravel
Identify: composer.json

```Dockerfile
FROM composer:latest AS builder
WORKDIR /app
COPY . .
RUN composer install --no-dev

FROM php:8.3-apache
COPY --from=builder /app /var/www/html
```

Ruby on Rails
Identify: Gemfile

```Dockerfile
FROM ruby:3.4
WORKDIR /app
COPY Gemfile Gemfile.lock ./
RUN bundle install
COPY . .
CMD ["rails","server","-b","0.0.0.0"]
```


🔎 Phase 4: ENV vs CMD vs ENTRYPOINT Detection
How to look at application code and know what Dockerfile commands to use:

Search for Environment Variables

Go: ``` os.Getenv()```

Java: ``` System.getenv()```

Node: ```process.env```

Python: ```os.environ```

.NET: ```Environment.GetEnvironmentVariable()```
If found, ENV SOME_VAR=value may be needed.

Search for Command Line Arguments

Go: ```flag.String(), flag.Parse()```

Java: ```args[]```

Node:``` process.argv```

Python: ```argparse, sys.argv```
If found, CMD ["--port=8080"] may be appropriate.

The Golden Rule:

```ENTRYPOINT```: The executable that must run (e.g., ```["./app"]```).

CMD: Default arguments passed to the Entrypoint, which can be easily overridden by the user (e.g., ["--port=8080"]).


🚀 Phase 5: Production Best Practices Checklist
Always try to:

✅ Use multi-stage builds

✅ Copy only required files (dependency cache trick)

✅ Use Alpine/slim runtime images when possible

✅ Run as non-root user (advanced but recommended)

✅ Add .dockerignore

✅ Separate build stage and runtime stage

✅ Prefer ENTRYPOINT for applications

✅ Use CMD for default arguments

A common production pattern is:

```bash
ENTRYPOINT ["./app"]
CMD ["--port=8080"]
```


