# Lab 02: Docker LAMP Stack

This project uses Docker Compose to run a multi-container LAMP (Linux, Apache, MySQL, PHP) stack.

*   `db`: A MySQL 8.0 container.
*   `web`: An Apache + PHP container built from a custom Dockerfile.

The PHP service connects to the MySQL service, retrieves data, and displays it.

## How to Run

1.  **Clone the repository.**

2.  **Navigate to the project directory:**
    ```bash
    cd 02-docker-lamp-stack
    ```

3.  **Start the services:**
    This command will build the custom PHP image and start both the `web` and `db` containers.
    ```bash
    docker compose up -d
    ```

4.  **Access the application:**
    Open your browser and go to `http://localhost:8080`.

    ![Screenshot of App](<your-screenshot-url-here>)

5.  **Stop and clean up:**
    To stop the containers and remove the network and volumes, run:
    ```bash
    docker compose down --volumes
    ```

### Key Concepts Demonstrated

*   **Multi-service application** with `docker-compose.yml`.
*   **Custom image build** as part of the compose lifecycle (`build: .`).
*   **Service discovery** where the `web` container finds the `db` container by its service name.
*   **Environment variables** for configuration (`MYSQL_ROOT_PASSWORD`, etc.).
*   **Bind mounts** for source code (`./src:/var/www/html`) and init scripts (`./db/init.sql:...`).
*   **Named volumes** for persistent database storage (`db_data`).
*   **Controlling startup order** with `depends_on`.
