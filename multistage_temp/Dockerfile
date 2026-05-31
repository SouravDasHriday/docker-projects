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
