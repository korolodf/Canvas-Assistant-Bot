/*
Faculty of Information
University of Toronto
Bachelor of Information
INF453: Capstone Project
Instructor: Dr Maher Elshakankiri
Supervisor: Dr Rohan Alexander
Names: Jayden Jung, Finn Korol-O'Dwyer, Sofia Sellitto
Date created: March 10, 2024
Date last modified: April 10, 2024

This JavaScript file is part of a React application specifically designed to manage a chat interface, allowing users to interact with a backend Flask chatbot API. The file handles state management, user input, and network requests using React's functional component structure with hooks, and Axios for HTTP requests.

Key Components of the File:
1. Imports:
   - `React`, `useState`: Imported from the 'react' library to use React's core functionalities and the state hook within functional components.
   - `axios`: Used for making HTTP requests to the backend.
   - `meProfilePhotoUrl`, `chatProfilePhotoUrl`: Imported SVG URLs for displaying profile photos in chat messages.

2. ChatApp Functional Component:
   - Manages state for messages, input messages, access token, and loading status using React's `useState`.
   - Defines `sendMessage` function to handle sending messages and receiving responses from the chatbot.
   - Includes error handling and state updates throughout the interaction process.

3. Key Functionalities:
   - Input Handling: Users can enter their access token and chat messages through input fields.
   - Message Sending: On sending a message, the app updates the message list and makes an API call.
   - Chatbot Integration: Uses Axios to post data to a Flask API and handles the response by updating the chat interface.
   - Loading State: Indicates to the user that a process is ongoing when waiting for the chatbot's response.

4. User Interface:
   - Renders a chat window where messages are displayed along with profile photos, sender names, and timestamps.
   - Provides input fields for the access token and new messages, with a button to send messages.
   - Displays a loading indicator when the app is processing a request.

Purpose:
- The `ChatApp` component provides a user-friendly interface for interacting with a backend chatbot, facilitating real-time communication.
- It aims to simplify user interactions by managing state effectively and ensuring that all user inputs and chatbot responses are handled asynchronously.

This file demonstrates advanced React practices such as functional components with hooks, conditional rendering, and client-server communication via Axios, designed to create a robust user experience in web applications.
*/

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
            const response = await axios.post('http://127.0.0.1:4000/chatbot', { message: inputMessage, access_token: accessToken });
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
