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
