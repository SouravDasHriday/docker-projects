# ========================
# Builder
# ========================
FROM <builder-image> AS builder

WORKDIR /app

COPY . .

RUN <build-command>

# ========================
# Runtime
# ========================
FROM gcr.io/distroless/<runtime>

WORKDIR /app

COPY --from=builder /app/<artifact> .

# Security
USER nonroot:nonroot

# Metadata
LABEL maintainer="your-team"
LABEL org.opencontainers.image.source="repository"

# Healthcheck handled externally
EXPOSE 8080

ENTRYPOINT ["<entrypoint>"]
CMD ["<default-args>"]
