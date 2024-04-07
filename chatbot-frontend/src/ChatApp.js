import React, { useState } from 'react';
import axios from 'axios';

function ChatApp() {
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState('');

    const sendMessage = async () => {
        try {
            // Add the user's message to the messages array with "Me: " prefix and timestamp
            const currentTime = new Date().toLocaleTimeString();
            const userMessage = <span><strong>Me:</strong> {inputMessage}</span>; // Wrap "Me" in <strong> tag
            const updatedMessages = [...messages, { sender: 'Me', text: userMessage, timestamp: currentTime }];
            setMessages(updatedMessages);

            // Clear the input field
            setInputMessage('');

            // Make a request to the Flask API endpoint with the user's message
            const response = await axios.post('http://127.0.0.1:3000/chatbot', { message: inputMessage });
            const chatbotResponse = response.data.response;

            // Add the chatbot's response to the messages array with timestamp
            const botMessage = <span><strong>Chatterbox:</strong> {chatbotResponse}</span>; // Wrap "Bot" in <strong> tag
            const updatedMessagesWithBotResponse = [...updatedMessages, { sender: 'Bot', text: botMessage, timestamp: currentTime }];
            setMessages(updatedMessagesWithBotResponse);

        } catch (error) {
            console.error('Error sending message to chatbot:', error);
        }
    };

    return (
        <div className="chat-container">
            <div className="chat-window">
                {/* Display the chat messages */}
                {messages.map((message, index) => (
                    <div key={index} className={`message ${message.sender === 'Me' ? 'user' : 'bot'}`}>
                        <span className="timestamp">{message.timestamp}</span> {message.text}
                    </div>
                ))}
            </div>
            <div className="input-box">
                {/* Input field for sending messages */}
                <input
                    type="text"
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    placeholder="Type your message..."
                />
                {/* Button to send message */}
                <button onClick={sendMessage}>Send</button>
            </div>
        </div>
    );
}

export default ChatApp;