# app.py
from flask import Flask, render_template, jsonify
import threading
import main  

app = Flask(__name__)

assistant_thread = None
running = False

def run_assistant():
    global running
    running = True
    main.start() 
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    global assistant_thread
    if assistant_thread is None or not assistant_thread.is_alive():
        assistant_thread = threading.Thread(target=run_assistant)
        assistant_thread.start()
    return jsonify({"status": "started"})

@app.route("/stop", methods=["POST"])
def stop():
    global running
    running = False
    main.stop()   
    return jsonify({"status": "stopped"})

if __name__ == "__main__":
    app.run(debug=True)
