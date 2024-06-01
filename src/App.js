import logo from './logo.svg';
import './App.css';
import MdContent from './MdContent';
import ChatInterface from './ChatInterface';

function App() {
  return (
    <div className="App">
      {/* <MdContent/> */}
      <h1>Chat with PDF</h1>
      <ChatInterface />
    </div>
  );
}

export default App;
