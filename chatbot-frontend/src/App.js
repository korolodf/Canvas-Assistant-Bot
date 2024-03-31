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
    <h1> Hi there 👋</h1>
    <p> Hi I’m Chatterbox, your personalized Canvas helper. Please feel free to ask me any questions you might about this course, including assignment due dates, weekly announcements, or syllabus related concerns. </p>
    <p> </p>
    <ChatApp /> {/* Render your chat component */}
  </div>
  </div>
  );
}

export default App;
