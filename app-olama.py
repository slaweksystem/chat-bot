import os
import requests
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# The URL for your local Ollama's chat endpoint
OLLAMA_URL = os.environ.get('OLLAMA_URL')

# The name of the local model you are using (e.g., "llama3", "mistral")
# Make sure this model is available in your Ollama instance.
OLLAMA_MODEL = "llama3" 

SYSTEM_PROMPT = """
You're a car-recommender chat assistant.
Your mission is to engage with users, 
asking relevant questions to comprehend their car preferences such as budget,
car type, fuel type, brand, or specific features.
Upon capturing these responses You will suggest the most suitable cars with their specifications.
The focus should be on user-friendliness to ensure a smooth experience.
"""


@app.route('/get_recommendation', methods=['POST'])
def get_recommendation():
    """Handles a conversational request using a local Ollama model."""
    try:
        data = request.json
        if not data or 'history' not in data:
            return jsonify({'error': 'Invalid request. Missing "history" in the body.'}), 400

        # The history from the frontend is in Gemini's format
        gemini_history = data['history']

        # --- Step 1: Convert Gemini history to Ollama's expected format ---
        # Ollama expects a 'messages' list with 'role' and 'content'.
        # It also uses 'assistant' for the model's role, not 'model'.
        ollama_messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        for message in gemini_history:
            role = "assistant" if message['role'] == 'model' else message['role']
            content = message['parts'][0]['text']
            ollama_messages.append({'role': role, 'content': content})

        # --- Step 2: Prepare the payload and call the Ollama API ---
        payload = {
            "model": OLLAMA_MODEL,
            "messages": ollama_messages,
            "stream": False  # We want the full response at once
        }

        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        
        ollama_response_data = response.json()
        
        # --- Step 3: Format Ollama's response back into Gemini's format ---
        # Extract the assistant's message from the response
        assistant_message_content = ollama_response_data['message']['content']
        
        # Append the new message to our original history to send back to the client
        gemini_history.append({
            "role": "model",
            "parts": [{"text": assistant_message_content}]
        })

        return jsonify({'history': gemini_history})

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Ollama: {e}")
        error_message = "I couldn't connect to the local AI model. Is Ollama running?"
        gemini_history.append({"role": "model", "parts": [{"text": error_message}]})
        return jsonify({'history': gemini_history}), 500
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'Sorry, an unexpected error occurred on the server.'}), 500

if __name__ == '__main__':
    # Running on port 5000
    app.run(debug=True, port=5000)
