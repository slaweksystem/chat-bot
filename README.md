# chat-bot

This is an experimental, conversational AI chatbot designed to help users find their ideal car. It engages in a natural conversation, remembers the context of the chat, and provides car recommendations based on user preferences like budget, brand, and features.
The project uses a Python Flask backend to connect to the Google Gemini API and a simple HTML, CSS, and JavaScript frontend for the user interface.

## Setup and Installation

Follow these steps to get the project running on your local machine.

### Clone the Repository

```bash
git clone https://github.com/slaweksystem/chat-bot.git
cd chat-bot
```

### Install Dependencies

Install the required Python libraries using pip.

```bash
pip3 install -r requirements.txt
```

## How to Run

To run the chat, open two separate terminals in the project directory and run the following commands:

### Terminal 1: Start the Backend API

First add your Gemini API key to env variable:

```bash
export GEMINI_API_KEY="YOUR_SECRET_API_KEY_HERE"
```

Then start the Flask server:

```bash
python3 app.py
```

### Terminal 2: Start the Frontend GUI

This command serves the user interface files.

```bash
python -m http.server 8000
```

### Open the Chat

Once both servers are running, open your web browser and navigate to:

<http://localhost:8000>
