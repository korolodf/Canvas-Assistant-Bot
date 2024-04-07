import React, { useState } from 'react';
import axios from 'axios';

import meProfilePhotoUrl from './circle.svg';
import chatProfilePhotoUrl from './circlelogo.svg';

function ChatApp() {
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState('');

    const sendMessage = async () => {
        try {
            // Add the user's message to the messages array with "Me: " prefix and timestamp
            const currentTime = new Date().toLocaleTimeString();
            const userMessage = typeof inputMessage === 'object' ? JSON.stringify(inputMessage) : inputMessage; // Convert object to string if necessary
            const updatedMessages = [...messages, { sender: 'Me', text: userMessage, timestamp: currentTime, profilePhotoUrl: meProfilePhotoUrl }];
            setMessages(updatedMessages);

            // Clear the input field
            setInputMessage('');

            // Make a request to the Flask API endpoint with the user's message
            const response = await axios.post('http://127.0.0.1:3000/chatbot', { message: inputMessage });
            const chatbotResponse = response.data.response;

            // Add the chatbot's response to the messages array with timestamp
            const botMessage = typeof chatbotResponse === 'object' ? JSON.stringify(chatbotResponse) : chatbotResponse; // Convert object to string if necessary
            const updatedMessagesWithBotResponse = [...updatedMessages, { sender: 'Chatterbox', text: botMessage, timestamp: currentTime, profilePhotoUrl: chatProfilePhotoUrl }];
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
                    <div key={index} className={`message ${message.sender === 'Me' ? 'user' : 'Chatterbox'}`}>
                        <img src={message.profilePhotoUrl} alt={message.sender} className="profile-photo" style={{ width: '40px', height: '40px' }} />
                        <div>
                            <div><strong>{message.sender}</strong></div>
                            <div dangerouslySetInnerHTML={{ __html: message.text }}></div> {/* Render HTML tags */}
                            <span className="timestamp">{message.timestamp}</span>
                        </div>
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
