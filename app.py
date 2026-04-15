from flask import Flask, render_template, jsonify
import threading
import main  

app = Flask(__name__)

assistant_thread = None

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start():
    global assistant_thread

    if not main.running:
        main.running = True
        assistant_thread = threading.Thread(target=main.phantom_loop)
        assistant_thread.start()

    return jsonify({"status": "started"})


@app.route("/stop", methods=["POST"])
def stop():
    main.running = False   
    return jsonify({"status": "stopped"})


if __name__ == "__main__":
    app.run(debug=True)

