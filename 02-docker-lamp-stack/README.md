# Lab 02: Docker LAMP Stack 🐳🔥

A simple but powerful **LAMP stack** (Linux + Apache + MySQL + PHP) setup using **Docker Compose**.
This lab teaches you how to containerize a PHP web app that connects to a MySQL database and run both using Docker.

---

## 🔍 What You'll Learn

* How to build a custom Docker image for PHP + Apache
* How to run a MySQL database container with an auto-run SQL script
* How to wire multiple containers with Docker Compose
* How to use bind mounts and named volumes for development and persistence

---

## 🚀 Quick Start

### 1. Clone this repository and navigate into the lab:

```bash
git clone https://github.com/SouravDasHriday/docker-projects.git
cd docker-projects/02-docker-lamp-stack
```

### 2. Run the stack:

```bash
docker compose up -d
```

### 3. Access your PHP app:

Open your browser and go to:

```
http://localhost:8080
```
or in terminal:

```
curl http://localhost:8080
```


You should see a page showing MySQL data via PHP.

### 4. Tear it down:

```bash
docker compose down --volumes
```

---

## 📊 Architecture Overview

* `db`: MySQL 8.0 container with database initialized from `init.sql`
* `web`: Custom PHP + Apache container serving `src/index.php`
* Docker Compose manages network and volume creation automatically

```plaintext
[HOST:8080] → [web container:80] → PHP → MySQL (db container)
```

---

## 📁 Project Structure

```
02-docker-lamp-stack/
├── Dockerfile                  # Builds custom PHP + Apache image
├── docker-compose.yml         # Defines multi-container setup
├── README.md
├── LICENSE
├── db/
│   └── init.sql               # SQL file to create and seed DB
└── src/
    └── index.php              # Main PHP frontend
```

---

## 📃 docker-compose.yml Deep Dive

```yaml
services:
  db:
    image: mysql:8.0
    container_name: mysql_db
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: myrootpassword
      MYSQL_DATABASE: mydatabase
      MYSQL_USER: myuser
      MYSQL_PASSWORD: mypassword
    volumes:
      - db_data:/var/lib/mysql
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql

  web:
    build: .
    container_name: php_apache_web
    restart: always
    ports:
      - "8080:80"
    volumes:
      - ./src:/var/www/html
    depends_on:
      - db

volumes:
  db_data:
```

### 🔍 Key Points

* `services:` defines two containers: `db` and `web`
* MySQL uses env vars to create user/db and loads `init.sql`
* PHP container maps the `src/` folder for live editing
* Port `8080` on host maps to `80` in container
* `depends_on` ensures DB starts before PHP

---

## 🔧 Dockerfile Explained

```Dockerfile
FROM php:8.1-apache
RUN docker-php-ext-install mysqli
RUN a2enmod rewrite
```

* Starts from official PHP+Apache image
* Installs `mysqli` for DB connections
* Enables Apache rewrite (for future URL rewrites/frameworks)

---

## 👚 db/init.sql

```sql
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY_KEY,
    name VARCHAR(255) NOT NULL
);
INSERT INTO products (name) VALUES ('Laptop'), ('Keyboard');
```

* Auto-executed by MySQL at first startup
* Creates `products` table and inserts 2 rows

---

## 🌐 src/index.php

```php
<?php  // <--- THIS LINE IS CRITICAL!
// These are the details for the connection.
// The host is 'db' because that is the name of our database service in docker-compose.yml.
$host = 'db';
$user = 'myuser';
$pass = 'mypassword';
$db_name = 'mydatabase';

// Create a new mysqli connection
$conn = new mysqli($host, $user, $pass, $db_name);

// Check for connection errors
if ($conn->connect_error) {
    die("<h1>Connection failed: " . $conn->connect_error . "</h1>");
}

echo "<h1>🔥 Successfully connected to MySQL! 🔥</h1>";
echo "<h2>My Awesome LAMP Stack is running via Docker Compose.</h2>";

// Query the database to get the data
$sql = 'SELECT * FROM products';
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    echo "<h3>Products from our Database:</h3>";
    echo "<ul>";
    // output data of each row
    while($row = $result->fetch_assoc()) {
        echo "<li>ID: " . $row["id"]. " - Name: " . $row["name"]. "</li>";
    }
    echo "</ul>";
} else {
    echo "0 results";
}

$conn->close();
?>
```

* Connects to MySQL using service name `db` as host
* Queries all products and shows them in a list

---

## 📍 Notes

* Docker Compose is used to avoid managing `docker run` manually
* Bind mounts allow you to edit PHP files and reflect changes instantly
* MySQL init scripts save time on DB setup and demo data
* Named volumes keep your data persistent across `up/down` cycles
* Great foundation for extending to include Adminer, phpMyAdmin, etc.

---

## 📅 Credits

This lab is part of the [DevOps Learning Series](https://github.com/SouravDasHriday) by **Sourav Das**.

---

## 📄 License

MIT License

Copyright (c) 2025 Sourav Das

