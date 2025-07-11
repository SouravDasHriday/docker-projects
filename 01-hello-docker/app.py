# app.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "<h1>Hello from Docker!</h1><p>This is my first containerized Flask application. 🔥</p>"

if __name__ == '__main__':
    # Listen on all network interfaces (0.0.0.0)
    # This is crucial for Docker networking
    app.run(host='0.0.0.0', port=5000)
