import React, { useState } from 'react';
import axios from 'axios';

import meProfilePhotoUrl from './circle.svg';
import chatProfilePhotoUrl from './circlelogo.svg';

function ChatApp() {
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState('');
    const [accessToken, setAccessToken] = useState('');
    const [loading, setLoading] = useState(false); // State to track loading status

    const sendMessage = async () => {
        try {
            // Set loading state to true
            setLoading(true);

            // Add the user's message to the messages array with "Me: " prefix and timestamp
            const currentTime = new Date().toLocaleTimeString();
            const userMessage = inputMessage;
            const updatedMessages = [...messages, { sender: 'Me', text: userMessage, timestamp: currentTime, profilePhotoUrl: meProfilePhotoUrl }];
            setMessages(updatedMessages);

            // Clear the input field
            setInputMessage('');

            // Make a request to the Flask API endpoint with the user's message and access token
            const response = await axios.post('http://127.0.0.1:3000/chatbot', { message: inputMessage, access_token: accessToken });
            const chatbotResponse = response.data.response;

            // Add the chatbot's response to the messages array with timestamp
            const botMessage = chatbotResponse;
            const updatedMessagesWithBotResponse = [...updatedMessages, { sender: 'Chatterbox', text: botMessage, timestamp: currentTime, profilePhotoUrl: chatProfilePhotoUrl }];
            setMessages(updatedMessagesWithBotResponse);

        } catch (error) {
            console.error('Error sending message to chatbot:', error);
        } finally {
            // Set loading state to false after response or error
            setLoading(false);
        }
    };

    const handleSendMessage = () => {
        if (accessToken) {
            sendMessage();
        } else {
            window.alert('Please fill in the access token.');
        }
    };

    return (
        <div className="chat-container">
            <div className="input-box">
                <input
                    type="text"
                    value={accessToken}
                    onChange={(e) => setAccessToken(e.target.value)}
                    placeholder="Paste your access token..."
                />
            </div>
            <div className="chat-window">
                {messages.map((message, index) => (
                    <div key={index} className={`message ${message.sender === 'Me' ? 'user' : 'Chatterbox'}`}>
                        <img src={message.profilePhotoUrl} alt={message.sender} className="profile-photo" style={{ width: '40px', height: '40px' }} />
                        <div>
                            <div><strong>{message.sender}</strong></div>
                            <div dangerouslySetInnerHTML={{ __html: message.text }}></div>
                            <span className="timestamp">{message.timestamp}</span>
                        </div>
                    </div>
                ))}
                {loading && <div className="loading-text">Loading...</div>}
            </div>
            <div className="input-box">
                <input
                    type="text"
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    placeholder="Type your message..."
                />
                <button onClick={handleSendMessage}>Send</button>
            </div>
        </div>
    );
}

export default ChatApp;
