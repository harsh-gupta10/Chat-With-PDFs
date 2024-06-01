import React, { useState } from 'react';
import axios from 'axios';
import io from 'socket.io-client';
// import ReactMarkdown from 'react-markdown';
import MarkdownRenderer from './MarkdownRenderer';
import './ChatInterface.css';
import { CopyBlock, dracula } from 'react-code-blocks';

// import MarkdownRenderer from './MarkdownRenderer';
// import remarkGfm from 'remark-gfm';


const socket = io('http://localhost:5000');

const ChatInterface = () => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [chatHistory, setChatHistory] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('http://localhost:5000/chat', { query });
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

  function processContent(originalContent) {
    const codeBlockPattern = /```(\w*)\n(.*?)\n```/gs;
    let match;
    let lastIndex = 0;
    const parts = [];

    while ((match = codeBlockPattern.exec(originalContent)) !== null) {
      // Text before the code block
      const textPart = originalContent.slice(lastIndex, match.index).replace(/`/g, '\\`');
      if (textPart.trim()) {
        parts.push({ text: textPart, code: null });
      }

      // The code block
      const codePart = match[2].replace(/`/g, '\\`');
      parts.push({ text: null, code: codePart });

      lastIndex = match.index + match[0].length;
    }

    // Text after the last code block
    const textPart = originalContent.slice(lastIndex).replace(/`/g, '\\`');
    if (textPart.trim()) {
      parts.push({ text: textPart, code: null });
    }

    return parts;
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

  let parts

  return (
    <div className="chat-container">
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
              {/* {chat.response} */}
              {/* <MarkdownRenderer markdown={chat.response} /> */}
              {chat.response}
              {/* { parts = processContent(chat.response)} */}


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