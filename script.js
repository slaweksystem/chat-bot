const form = document.getElementById('input-form');
const userInput = document.getElementById('user-input');
const chatBox = document.getElementById('chat-box');

// 1. Create a variable to store the chat history
let chatHistory = [];

// Add an initial message from the assistant
document.addEventListener('DOMContentLoaded', () => {
    chatHistory = [
        {
            "role": "model",
            "parts": [{ "text": "Hello! I'm your AI car recommender. What are you looking for in a car today? (e.g., budget, brand, features)" }]
        }
    ];
    renderChat();
});


form.addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent the form from reloading the page
    const userMessage = userInput.value.trim();

    if (userMessage === '') return;

    // 2. Add the user's new message to our history
    chatHistory.push({
        "role": "user",
        "parts": [{ "text": userMessage }]
    });

    // Clear the input and re-render the chat
    userInput.value = '';
    renderChat();
    
    // Show a thinking indicator
    chatBox.innerHTML += `<p class="assistant-message thinking"><span>.</span><span>.</span><span>.</span></p>`;
    chatBox.scrollTop = chatBox.scrollHeight;


    // 3. Send the ENTIRE history to the backend
    try {
        const response = await fetch('http://127.0.0.1:5000/get_recommendation', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ history: chatHistory })
        });

        const data = await response.json();

        if (data.history) {
            // 4. Replace our local history with the updated one from the server
            chatHistory = data.history;
        } else {
            // Handle errors from the backend
            chatHistory.push({
                "role": "model",
                "parts": [{ "text": data.error || "Sorry, something went wrong." }]
            });
        }

    } catch (error) {
        chatHistory.push({
            "role": "model",
            "parts": [{ "text": "I couldn't connect to the server. Please try again." }]
        });
    } finally {
        // 5. Re-render the chat with the final, updated history
        renderChat();
    }
});

function renderChat() {
    chatBox.innerHTML = ''; // Clear the chat box
    chatHistory.forEach(message => {
        // The role determines the message styling
        const messageClass = message.role === 'user' ? 'user-message' : 'assistant-message';
        // Gemini's API returns text in message.parts[0].text
        const messageText = message.parts[0].text;

        chatBox.innerHTML += `<p class="${messageClass}">${messageText.replace(/\n/g, '<br>')}</p>`;
    });

    // Auto-scroll to the latest message
    chatBox.scrollTop = chatBox.scrollHeight;
}