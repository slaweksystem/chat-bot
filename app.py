import os

from flask import Flask, request, jsonify
from google import genai
from google.genai.types import GenerateContentConfig

from flask_cors import CORS 

app = Flask(__name__)
CORS(app)

# Configure the Gemini API key
client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

@app.route('/get_recommendation', methods=['POST'])
def get_recommendation():
    """Handles a conversational request for car recommendations."""
 
    try:
        data = request.json
        # Expect a 'history' key which is a list of messages
        if not data or 'history' not in data:
            return jsonify({'error': 'Invalid request. Missing "history" in the body.'}), 400

        chat_history = data['history']
        
        # Start a chat session with the existing history
        chat = client.chats.create(model="gemini-2.5-flash",
                                   history=chat_history[:-1],
                                   config=GenerateContentConfig(
                                        system_instruction=[
                                            "You're a car-recommender chat assistant.",
                                            "Your mission is to engage with users, ",
                                            "asking relevant questions to comprehend their car preferences such as budget,",
                                            "car type, fuel type, brand, or specific features.",
                                            "Upon capturing these responses You will suggest the most suitable cars with their specifications.",
                                            "The focus should be on user-friendliness to ensure a smooth experience."
                                            ],
                                        temperature = 0.6
                                        ),
        )
        
        # The last message in the history is the new user prompt
        user_message = chat_history[-1]['parts'][0]['text']
        
        response = chat.send_message(user_message)

        print(f"response: {response.text}")

        # The updated history now includes the model's response
        updated_history = chat.get_history()
        
        # Convert the response to a JSON-serializable format
        json_history = [{'role': msg.role, 'parts': [{'text': msg.parts[0].text}]} for msg in updated_history]

        return jsonify({'history': json_history})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'Sorry, an error occurred on our end.'}), 500

if __name__ == '__main__':
    app.run(debug=True)