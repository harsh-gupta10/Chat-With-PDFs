import React, { useState } from 'react';
import axios from 'axios';
import io from 'socket.io-client';
// import ReactMarkdown from 'react-markdown';
import './ChatInterface.css';
import MarkdownRenderer from './MarkdownRenderer';
import { CopyBlock, dracula } from 'react-code-blocks';

function parseTextAndCode(input) {
  const output = [];
  let currentText = "";
  let currentCode = "";
  let inCodeBlock = false;

  const codeBlockStartPattern = /^```(\w+)?/;
  const codeBlockEndPattern = /^```$/;

  const lines = input.split('\n');

  for (const line of lines) {
    if (inCodeBlock) {
      if (codeBlockEndPattern.test(line)) {
        inCodeBlock = false;
        if (currentCode.trim() !== "") {
          output.push({ code: currentCode.trim() });
          currentCode = "";
        }
      } else {
        currentCode += line + '\n';
      }
    } else {
      if (codeBlockStartPattern.test(line)) {
        inCodeBlock = true;
        if (currentText.trim() !== "") {
          output.push({ text: currentText.trim() });
          currentText = "";
        }
      } else {
        currentText += line + '\n';
      }
    }
  }

  if (currentText.trim() !== "") {
    output.push({ text: currentText.trim() });
  }

  if (currentCode.trim() !== "") {
    output.push({ code: currentCode.trim() });
  }

  return output;
}

function MyCoolCodeBlock({ code, language, showLineNumbers }) {
  return (
    <CopyBlock
      text={code}
      language={language}
      showLineNumbers={showLineNumbers}
      theme={dracula}
      codeBlock
    />
  );
}

const socket = io('http://localhost:5000');

const ChatInterface = () => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [useVectorEmbeddings, setUseVectorEmbeddings] = useState(true);
  const handleToggleClick = () => {
    setUseVectorEmbeddings(!useVectorEmbeddings);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('http://localhost:5000/chat', { query, useVectorEmbeddings });
      setResponse(res.data.response);
      setChatHistory([...chatHistory, { query, response: res.data.response }]);
      setQuery('');
    } catch (err) {
      console.error(err);
    }
  };

  socket.on('response', (data) => {
    setResponse(data.response);
    setChatHistory([...chatHistory, { query, response: data.response }]);
    setQuery('');
  });
  let parts =[]
  return (
    <div className="chat-container">
      <div className="toggle-container">
        <label>
          <input
            type="checkbox"
            checked={useVectorEmbeddings}
            onChange={handleToggleClick}
          />
          Use Loded Docs
        </label>
      </div>
      <div className="chat-history">
        {chatHistory.map((chat, index) => (
          <div key={index} className="chat-message">
            <div className="user-message">
              <span>You:</span>
              <p>{chat.query}</p>
            </div>
            <div className="bot-message">
              <span>Bot:</span>
              {/* <ReactMarkdown>{chat.response}</ReactMarkdown> */}
              {/* <MarkdownRenderer markdown={chat.response} /> */}
              {/* <MyCoolCodeBlock code={chat.response} language="cpp" showLineNumbers={true} /> */}
              {parseTextAndCode(chat.response).map((part, index) => (
                <div key={index}>
                  {part.text && <MarkdownRenderer markdown={part.text} />}
                  {part.code && <MyCoolCodeBlock code={part.code} language="cpp" showLineNumbers={true} />}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit} className="chat-input">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter your query"
          autoFocus
        />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default ChatInterface;