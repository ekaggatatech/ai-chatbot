import { useState, useRef, useEffect } from "react";
import ChatbotIcon from "./Component/ChatbotIcon";
import "./index.css";
import { RiSendInsFill } from "react-icons/ri";
import { IoCloseCircle } from "react-icons/io5";
import ReactMarkdown from "react-markdown";
import axios from "axios";

function App() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  // Auto Scroll Ref
  const messagesEndRef = useRef(null);

  // Scroll to bottom whenever messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  const toggleChat = () => {
    if (isOpen) {
      setMessages([]);
    } else {
      setMessages([
        {
          text: "Hi 👋 How can I help?",
          sender: "bot",
        },
      ]);
    }

    setIsOpen(!isOpen);
  };

  const sendMessage = async () => {
    if (input.trim() === "") return;

    const userMessage = input;

    // Add user message
    setMessages((prev) => [
      ...prev,
      {
        text: userMessage,
        sender: "user",
      },
    ]);

    setInput("");
    setLoading(true);

    try {
      const response = await axios.post(
        "http://localhost:8000/chat",
        {
          message: userMessage,
        }
      );

      // Add bot response
      setMessages((prev) => [
        ...prev,
        {
          text: response.data.answer,
          sender: "bot",
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          text: "Can't connect to Server",
          sender: "bot",
        },
      ]);
    }

    setLoading(false);
  };

  return (
    <>
      <h1>AI Assistant</h1>

      <ChatbotIcon toggleChat={toggleChat} />

      {isOpen && (
        <div className="chatbot-window">
          {/* Header */}
          <div className="chat-header">
            <h3>Chatbot</h3>

            <button
              className="close-btn"
              onClick={toggleChat}
            >
              <IoCloseCircle size={22} />
            </button>
          </div>

          {/* Chat Body */}
          <div className="chat-body">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={
                  msg.sender === "bot"
                    ? "message-bot-message"
                    : "message-user-message"
                }
              >
                <ReactMarkdown>{msg.text}</ReactMarkdown>
              </div>
            ))}

            {loading && (
              <p className="loading">
                Bot is typing...
              </p>
            )}

            {/* Auto Scroll Target */}
            <div ref={messagesEndRef}></div>
          </div>

          {/* Chat Input */}
          <div className="chat-input">
            <input
              type="text"
              value={input}
              placeholder="Type a message..."
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !loading) {
                  sendMessage();
                }
              }}
            />

            <button
              onClick={sendMessage}
              disabled={loading}
            >
              <RiSendInsFill size={18} />
            </button>
          </div>
        </div>
      )}
    </>
  );
}

export default App;