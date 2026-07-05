import os
import psutil
import time
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL from environment variables
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'default_user')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'default_password')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DATABASE', 'default_db')

# Initialize MySQL
mysql = MySQL(app)

# Store historical data for metrics
history = {
    'timestamps': [],
    'cpu': [],
    'ram': [],
    'cpu_cores': []
}

def init_db():
    with app.app_context():
        cur = mysql.connection.cursor()
        # Create messages table
        cur.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')

        # Create metrics table for historical data
        cur.execute('''
        CREATE TABLE IF NOT EXISTS metrics (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            cpu_percent FLOAT,
            ram_percent FLOAT,
            disk_percent FLOAT,
            cpu_frequency FLOAT
        );
        ''')
        mysql.connection.commit()
        cur.close()

@app.route('/')
def hello():
    cur = mysql.connection.cursor()
    cur.execute('SELECT message FROM messages ORDER BY id DESC')
    messages = cur.fetchall()
    cur.close()
    return render_template('index.html', messages=messages)

@app.route('/submit', methods=['POST'])
def submit():
    new_message = request.form.get('new_message')
    if new_message:
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO messages (message) VALUES (%s)', [new_message])
        mysql.connection.commit()
        cur.close()
        return jsonify({'success': True, 'message': new_message})
    return jsonify({'success': False, 'error': 'No message provided'}), 400

@app.route('/health')
def health():
    """Health check endpoint for Docker"""
    return jsonify({'status': 'healthy', 'service': 'flask-app'})

@app.route('/api/metrics')
def get_metrics():
    """Get system metrics"""
    try:
        # Get CPU usage per core
        cpu_percent_per_core = psutil.cpu_percent(interval=0.5, percpu=True)

        # Get overall CPU usage
        cpu_percent = psutil.cpu_percent(interval=0.5)

        # Get RAM usage
        ram = psutil.virtual_memory()
        ram_percent = ram.percent
        ram_used_gb = ram.used / (1024**3)
        ram_total_gb = ram.total / (1024**3)

        # Get CPU frequency
        cpu_freq = psutil.cpu_freq()
        cpu_freq_current = cpu_freq.current if cpu_freq else 0

        # Get CPU count
        cpu_count = psutil.cpu_count()

        # Get disk usage
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        disk_used_gb = disk.used / (1024**3)
        disk_total_gb = disk.total / (1024**3)

        # Get network stats
        net_io = psutil.net_io_counters()
        net_sent_mb = net_io.bytes_sent / (1024**2)
        net_recv_mb = net_io.bytes_recv / (1024**2)

        # Get system uptime
        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time
        uptime_days = int(uptime_seconds // 86400)
        uptime_hours = int((uptime_seconds % 86400) // 3600)
        uptime_minutes = int((uptime_seconds % 3600) // 60)

        # Store history
        current_time = datetime.now().strftime('%H:%M:%S')
        history['timestamps'].append(current_time)
        history['cpu'].append(cpu_percent)
        history['ram'].append(ram_percent)
        history['cpu_cores'].append(cpu_percent_per_core)

        # Keep last 30 data points
        if len(history['timestamps']) > 30:
            history['timestamps'].pop(0)
            history['cpu'].pop(0)
            history['ram'].pop(0)
            history['cpu_cores'].pop(0)

        # Store metrics in MySQL
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO metrics (cpu_percent, ram_percent, disk_percent, cpu_frequency)
                VALUES (%s, %s, %s, %s)
            """, (cpu_percent, ram_percent, disk_percent, cpu_freq_current))
            mysql.connection.commit()
            cur.close()
        except Exception as e:
            print(f"Error storing metrics in DB: {e}")

        metrics = {
            'cpu': {
                'percent': cpu_percent,
                'cores': cpu_percent_per_core,
                'count': cpu_count,
                'frequency': cpu_freq_current
            },
            'ram': {
                'percent': ram_percent,
                'used_gb': round(ram_used_gb, 2),
                'total_gb': round(ram_total_gb, 2)
            },
            'disk': {
                'percent': disk_percent,
                'used_gb': round(disk_used_gb, 2),
                'total_gb': round(disk_total_gb, 2)
            },
            'network': {
                'sent_mb': round(net_sent_mb, 2),
                'recv_mb': round(net_recv_mb, 2)
            },
            'uptime': {
                'days': uptime_days,
                'hours': uptime_hours,
                'minutes': uptime_minutes
            },
            'history': history
        }

        return jsonify(metrics)

    except Exception as e:
        print(f"Error getting metrics: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)
