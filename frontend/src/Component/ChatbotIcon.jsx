
import {BsChatDotsFill} from "react-icons/bs";
import {IoMdClose} from "react-icons/io";
export default function ChatbotIcon({ toggleChat, isOpen }) {
  return (
   <div className="chatbot-icon-wrapper">
    {!isOpen && <span className="chat-tooltip">Chat with Us</span>}

    <button className="chatbot-icon-btn" onClick={toggleChat}>
      {isOpen? <IoMdClose size={24}/>:<BsChatDotsFill size={24}/> }
    </button>
   </div>
  );
}