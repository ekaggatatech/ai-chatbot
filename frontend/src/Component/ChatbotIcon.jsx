
import { TbMessageFilled } from "react-icons/tb";
export default function ChatbotIcon({ toggleChat }) {
  return (
    <button className="chatbot-icon" onClick={toggleChat}>
       <TbMessageFilled size={30}/>
    </button>
  )
}