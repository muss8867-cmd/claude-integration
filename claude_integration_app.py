import os
from flask import Flask, request, jsonify
import anthropic

app = Flask(__name__)

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

@app.route('/claude_message', methods=['POST'])
def claude_message():
    if not ANTHROPIC_API_KEY:
        return jsonify({"error": "ANTHROPIC_API_KEY not set"}), 500

    data = request.json
    user_message = data.get('message')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        response = client.messages.create(
            model="claude-3-opus-20240229", # You can choose a different model if needed
            max_tokens=1024,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        return jsonify({"claude_response": response.content[0].text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
