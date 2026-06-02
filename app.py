from flask import Flask, render_template, jsonify
import psutil
import platform
import time
app = Flask(__name__)


@app.route("/")
def home():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    

    return render_template(
        "index.html",
        cpu=cpu,
        ram=ram,
        disk=disk
    )


@app.route("/stats")
def stats():
    processes = []
    net = psutil.net_io_counters()
    cpu_cores = psutil.cpu_percent(interval=0.1 , percpu=True)
    for proc in psutil.process_iter(
        ['pid', 'name', 'cpu_percent', 'memory_percent']
    ):
        try:
            processes.append({
                "pid": proc.info['pid'],
                "name": proc.info['name'],
                "cpu": proc.info['cpu_percent'],
                "memory": round(proc.info['memory_percent'], 2)
            })
        except:
            pass

    processes.sort(
        key=lambda x: x["cpu"],
        reverse=True
    )

    boot_time = psutil.boot_time()
    uptime_seconds = int(time.time() - boot_time)

    return jsonify({
        "cpu": psutil.cpu_percent(interval=0.1),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "cpu_cores": cpu_cores,
        "processes": processes[:10],
        "bytes_sent": round(net.bytes_sent / (1024 * 1024), 2),
        "bytes_recv": round(net.bytes_recv / (1024 * 1024), 2),
        "os": platform.system(),
        "kernel": platform.release(),
        "architecture": platform.machine(),
        "uptime": uptime_seconds

    })

if __name__ == "__main__":
    app.run(debug=True)
