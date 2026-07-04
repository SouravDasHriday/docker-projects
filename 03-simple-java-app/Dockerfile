# Buid stage:
FROM eclipse-temurin:21-jdk-alpine AS builder
WORKDIR /app
COPY /src .
RUN javac -d . Main.java

# Runtime stage:
FROM eclipse-temurin:21-jdk-alpine
WORKDIR /app
COPY --from=builder /app/ .
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
ENTRYPOINT ["java", "Main"]
