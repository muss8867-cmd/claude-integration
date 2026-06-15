import os
from flask import Flask, request, jsonify
import anthropic

app = Flask(__name__)

try:
    with open("api_key.txt", "r") as f:
        ANTHROPIC_API_KEY = f.read().strip()
except FileNotFoundError:
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
app.logger.info(f"ANTHROPIC_API_KEY loaded: {ANTHROPIC_API_KEY[:5]}...{ANTHROPIC_API_KEY[-5:]}" if ANTHROPIC_API_KEY else "ANTHROPIC_API_KEY not found (from file or env)")

@app.route('/claude_message', methods=['POST'])
def claude_message():
    if not ANTHROPIC_API_KEY:
        return jsonify({"error": "ANTHROPIC_API_KEY not set"}), 500

    data = request.json
    user_message = data.get('message')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        api_key_to_use = ANTHROPIC_API_KEY
        app.logger.info(f"API Key being used: {api_key_to_use[:5]}...{api_key_to_use[-5:]}" if api_key_to_use else "API Key is None")
        client = anthropic.Anthropic(api_key=api_key_to_use)
        response = client.messages.create(
            model="claude-sonnet-4-6", # Updated to a generally available model for testing
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
