# Lab 01: Hello Docker - Containerized Flask App 🐳

This project is a simple Python Flask application containerized using Docker.  
It demonstrates how to:
- Build a custom Docker image using a `Dockerfile`
- Install Python dependencies in a clean image
- Expose the application on port 5000
- Run it as a container locally

✅ This is part of a DevOps learning series by [Sourav Das](https://github.com/SouravDasHriday)

## How to Run

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd 01-hello-docker
    ```

2.  **Build the Docker image:**
    ```bash
    docker build -t hello-flask:v1 .
    ```

3.  **Run the Docker container:**
    ```bash
    docker run -d -p 5000:5000 --name my-first-app hello-flask:v1
    ```

4.  **Access the application:**
    Open your browser and go to `http://localhost:5000` or use `curl`:
    ```bash
    curl http://localhost:5000
    ```

### Project Structure

```
.
├── Dockerfile      # The recipe to build our image
├── README.md       # This file
├── app.py          # The Python Flask application code
└── requirements.txt # Python dependencies
```
