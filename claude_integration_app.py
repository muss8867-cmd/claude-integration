import os
from flask import Flask, request, jsonify
import anthropic

app = Flask(__name__)

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
app.logger.info(f"ANTHROPIC_API_KEY loaded: {ANTHROPIC_API_KEY[:5]}...{ANTHROPIC_API_KEY[-5:]}" if ANTHROPIC_API_KEY else "ANTHROPIC_API_KEY not found")

@app.route('/claude_message', methods=['POST'])
def claude_message():
    if not ANTHROPIC_API_KEY:
        return jsonify({"error": "ANTHROPIC_API_KEY not set"}), 500

    data = request.json
    user_message = data.get('message')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        response = client.messages.create(
            model="claude-opus-4-8", # Updated to a newer model
            max_tokens=1024,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        return jsonify({"claude_response": response.content[0].text}), 200
    except Exception as e:
        import traceback
        app.logger.error("Error in claude_message: %s", traceback.format_exc())
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
