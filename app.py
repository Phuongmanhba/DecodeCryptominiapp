from flask import Flask, render_template, request, jsonify
from engine import MiniAppCrypto

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run():
    data = request.get_json()
    text = data.get("text", "")
    action = data.get("action", "")
    key = data.get("key", "")
    mode = data.get("mode", "decrypt")

    try:
        crypto = MiniAppCrypto(text)

        if action == "hextobytes":
            crypto.hextobytes()
        elif action == "tobinary":
            crypto.tobinary()
        elif action == "xor":
            crypto.xor(key)
        elif action == "caesar":
            shift = int(key) if key else 0
            crypto.caesar(shift, mode)
        elif action == "rot":
            crypto.rot()
        elif action == "vigenere":
            crypto.vigenere(key, mode)
        else:
            return jsonify({"ok": False, "error": "Chức năng không hợp lệ"})

        return jsonify({
            "ok": True,
            "result": crypto.text,
            "history": crypto.history
        })

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

if __name__ == "__main__":
    app.run(debug=True, port=5000)