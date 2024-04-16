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

This JavaScript file is part of a React web application, primarily focused on creating a user interface for a chatbot named "Chatterbox". The file sets up the primary layout and functionality of the application, including importing necessary components and styles, and rendering the main application structure.

Key Components of the File:
1. Imports:
   - `logo` from './logo.svg': The logo image used in the app header.
   - `./App.css`: The CSS file for styling the application.
   - `ChatApp` from './ChatApp': A React component that handles the chat interface functionality.

2. Function Component (App):
   - This function defines the main app component.
   - The JSX returned by this function constructs the HTML structure of the app.

3. Structure:
   - **Header**: Contains the app's logo and a link to the project documentation on GitHub, ensuring accessibility standards are met with `noopener noreferrer`.
   - **Body**: Hosts the main content including a welcoming message and instructions for users to generate a new access token. This area also integrates the `ChatApp` component which presumably handles the chat interactions within the app.

4. Accessibility and Navigation:
   - Links include `target="_blank"` and `rel="noopener noreferrer"` to enhance security and usability when opening new tabs.
   - Informative and user-friendly text guides users on how to interact with the application.

Purpose:
- The script is designed to facilitate user interaction with the Chatterbox chatbot by providing a clear and structured interface.
- It aims to make it easy for users to understand how to enable and interact with the chatbot through Canvas by guiding them to generate an access token.

This file exemplifies the use of React's component-based architecture to build dynamic and interactive web applications, focusing on user experience and seamless functionality.

*/

import logo from './logo.svg';
import './App.css';
import ChatApp from './ChatApp';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <a
          className="App-link"
          href="https://github.com/korolodf/Canvas-Assistant-Bot"
          target="_blank"
          rel="noopener noreferrer"
        >
          Read our documentation
        </a>
      </header>
    <div className="App-body">
    {/* Your main content goes here */}
    <h1> 👋 Hi! I’m Chatterbox, your personalized Canvas helper. </h1>
    <p> For me to access your information, please go to <a href="https://q.utoronto.ca/profile/settings" target="_blank" rel="noopener noreferrer">https://q.utoronto.ca/profile/settings</a> (Account Settings) scroll to <strong>Approved Integrations</strong> and generate a <strong>New Access Token</strong>.</p>
    <p> </p>
    <ChatApp /> {/* Render your chat component */}
  </div>
  </div>
  );
}

export default App;
