# Lab 02: Docker LAMP Stack 🐳🔥

This project demonstrates how to build and run a full LAMP (Linux, Apache, MySQL, PHP) stack using Docker Compose.  
It includes:

- Building a custom Apache + PHP image
- Connecting to a MySQL container via environment variables
- Using volumes and init scripts for persistent DB and schema
- Launching the stack with a single `docker compose up` command

✅ This is part of a DevOps learning series by [Sourav Das](https://github.com/SouravDasHriday)

---

## Project Overview

*   `db`: A MySQL 8.0 container with initialization SQL.
*   `web`: An Apache + PHP container built from a custom Dockerfile.
*   `src/index.php`: The PHP app queries the DB and renders the result in the browser.

---

## How to Run

1.  **Clone the repository and navigate to the lab:**
    ```bash
    git clone https://github.com/SouravDasHriday/docker-projects.git
    cd docker-projects/02-docker-lamp-stack
    ```

2.  **Start the services:**
    ```bash
    docker compose up -d
    ```

3.  **Access the application:**
    Open your browser and go to:  
    `http://localhost:8080`

    _You should see dynamic content fetched from MySQL displayed via PHP._

    <!-- Optional screenshot -->
    <!-- ![Screenshot of App](lamp-preview.png) -->

4.  **Stop and clean up:**
    ```bash
    docker compose down --volumes
    ```

---

## Project Structure

02-docker-lamp-stack/
├── docker-compose.yml
├── Dockerfile
├── README.md
├── src/
│ └── index.php
└── db/
└── init.sql


---

## 🔑 Key Concepts Demonstrated

- Multi-container app using **Docker Compose**
- PHP app and MySQL DB communicating via **Docker network**
- Custom PHP image with **Apache and bind mounts**
- MySQL initialization using `init.sql`
- Environment variables and **named volumes**
- `depends_on` for container startup order

---

## 📌 Notes

- Default port for the PHP app: `8080`
- MySQL credentials are set via `environment` in `docker-compose.yml`
- You can extend this to use **phpMyAdmin**, **MariaDB**, or **Adminer**

---


