import requests
import json

CLOUD_PC_IP = "35.237.213.211"
FLASK_APP_PORT = 5000

def test_claude_integration(message):
    url = f"http://{CLOUD_PC_IP}:{FLASK_APP_PORT}/claude_message"
    headers = {"Content-Type": "application/json"}
    payload = {"message": message}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

if __name__ == "__main__":
    test_message = "Hello Claude, how are you today?"
    print(f"Sending message to Claude: {test_message}")
    result = test_claude_integration(test_message)
    print(f"Received response: {result}")

    test_message_no_key = "What is the capital of France?"
    print(f"\nSending message to Claude (expecting API key error): {test_message_no_key}")
    result_no_key = test_claude_integration(test_message_no_key)
    print(f"Received response: {result_no_key}")
