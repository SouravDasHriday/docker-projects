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
