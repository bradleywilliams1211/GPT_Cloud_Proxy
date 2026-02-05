from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# OpenAI client reads API key from environment variable automatically
client = OpenAI()

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Force JSON parse
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"reply": "Invalid JSON"}), 400

    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"reply": "Empty prompt"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60
        )
        reply_text = response.choices[0].message.content.strip()
        return jsonify({"reply": reply_text})

    except Exception as e:
        return jsonify({"reply": f"Error contacting OpenAI: {str(e)}"}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
