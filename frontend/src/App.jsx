import { useState, useRef, useEffect } from "react";
import ChatbotIcon from "./Component/ChatbotIcon";
import "./index.css";
import { RiSendInsFill } from "react-icons/ri";
import{ MdSmartToy,MdPerson} from "react-icons/md";
import ReactMarkdown from "react-markdown";
import axios from "axios";
import {FiMenu,FiMail, FiLogOut} from "react-icons/fi";
import { RiDownloadCloud2Line } from "react-icons/ri";
import {db} from "./firebase_config";
import {collection, addDoc, serverTimestamp} from "firebase/firestore";

function App() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [showMenu,setShowMenu]=useState(false);

  // contact form
  const[showSupportForm,setShowSupportForm]=useState(false);
  const[supportForm,setSupportForm]=useState({
    name:"",
    email:"",
    subject:"",
    PhoneNumber:"",
    message:""
  });
  const [errors,setErrors]=useState({});

  const formRef=useRef(null);

  const validateForm=()=>{
    let newErrors={};
  //Name validation 
  if (!supportForm.name.trim()){
    newErrors.name="Name is required";
  }
  // email validation
  if (!supportForm.email.trim()){
    newErrors.email="Email is required";
  }else if (
    !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(supportForm.email)
  ){
    newErrors.email="Enter a valid email id."
  }
  // Phone Number Validation
  if (!supportForm.PhoneNumber.trim()){
    newErrors.PhoneNumber="Phone Number is required";
  }else if (!/^[0-9]{10}$/.test(supportForm.PhoneNumber)){
    newErrors.PhoneNumber="Number must be of 10 digits";
  }
  // Subject Validation
  if (!supportForm.subject.trim()){
    newErrors.subject="Subject is required";
  }
  // Message Validation
  if (!supportForm.message.trim()){
    newErrors.message="Message is required";
  }else if (supportForm.message.trim().length < 10) {
    newErrors.message = "Message should be at least 10 characters";
  }
  setErrors(newErrors);
  return Object.keys(newErrors).length === 0;
  };
  const submitSupportForm = async () => {
  if(!validateForm()){
    return;
  }

  //connect the supportform or the contact form to firebase
  try{
    await addDoc(collection(db,"contacts"),{
      name:supportForm.name,
      email:supportForm.email,
      phone:supportForm.PhoneNumber,
      subject:supportForm.subject,
      message:supportForm.message,
      source:"chatbot_contact_form",
      createdAt:serverTimestamp()
    });
    console.log("Save to Firebase");

    setMessages((prev) => [
    ...prev,
    {
      text: "Thank you! Your support request has been submitted successfully. We will connect with you soon.",
      sender: "bot",
    },
  ]);
  }
  catch(error){
    console.error("Error in saving:",error);
    alert("Failed to submit.Please try again later.");

    setMessages((prev)=>[
      ...prev,{
        text:"Sorry, Something went wrong . Please try again later.",
        sender:"bot",
      },
    ]);
  }
  setShowSupportForm(false);

  setSupportForm({
    name: "",
    email: "",
    PhoneNumber:"",
    subject: "",
    message: "",
  });
};
  
  const menuRef=useRef(null);

  // Auto Scroll Ref
  const messagesEndRef = useRef(null);

  // Scroll to bottom whenever messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

// to scroll the contact form
useEffect(()=>{
  if (showSupportForm && formRef.current){
    setTimeout(()=>{
      formRef.current.scrollIntoView({behavior:"smooth",block:"center"})
    },100)
  }
},[showSupportForm])
// Load chat from sessionStorage when the icon opens
  useEffect(()=>{
    setMessages([{text:"Hi! How can I help?", sender:"bot",time:new Date().toLocaleTimeString(),}]);
  },[]);

  // Scroll to bottom when reopen chat
  useEffect(()=>{
    if(isOpen){
      setTimeout(()=>messagesEndRef.current?.scrollIntoView({behavior:"smooth"}),100);
    }
  },[isOpen]);

  // Close menu on outside click 
  useEffect(()=>{
     const handleCLickOutside=(e)=>{
    if (menuRef.current && !menuRef.current.contains(e.target)){
      setShowMenu(false);
    }
  };
  document.addEventListener("mousedown",handleCLickOutside);
  },[]);


  const toggleChat=()=>{
    setIsOpen(!isOpen);
  };

  //contact
  const handleContactSupport=()=>{

    setShowSupportForm(true);
    setShowMenu(false);
  };

  const handleSupportChange =(e)=> {
    const { name, value } = e.target;
    setSupportForm((prev) => ({
    ...prev,
    [name]: value,
  }));
   let error = "";
   // Name Validation
  if (name === "name") {
    if (!value.trim()) {
      error = "Name is required";
    } else if (!/^[A-Za-z ]+$/.test(value)) {
      error = "Name should contain only letters";
    } else if (value.trim().length < 2) {
      error = "Name should be at least 2 characters";
    }
  }

  // Email Validation
  if (name === "email") {
    const email=value.trim().toLowerCase();
    if (!email) {
      error = "Email is required";
    } else if (
      !/^[A-Z0-9._%+-]+@(gmail|yahoo|outlook|hotmail)\.(com|in)$/i.test(email)
    ) {
      error = "Enter a valid email address";
    }
  }

  // Phone Number Validation
  if (name === "PhoneNumber") {
    if (!value.trim()) {
      error = "Phone Number is required";
    } else if (!/^[0-9]{10}$/.test(value)) {
      error = "Phone Number must be exactly 10 digits";
    }
  }

  // Subject Validation
  if (name === "subject") {
    if (!value.trim()) {
      error = "Subject is required";
    }
  }

  // Message Validation
  if (name === "message") {
    if (!value.trim()) {
      error = "Message is required";
    } else if (value.trim().length < 10) {
      error = "Message should be at least 10 characters";
    }
  }

  // Update errors
  setErrors((prev) => ({
    ...prev,
    [name]: error,
  }));
  };
  const handleCloseChat=()=>{
    setIsOpen(false);//just for hidden not the message get clear
    setShowMenu(false);
  };

  
  const sendMessage = async () => {
    if (input.trim() === "") return;

    const userMessage = input;

    // Add user message
    setMessages((prev)=>[
      ...prev,
      {
        text:userMessage,
        sender:"user",
        time:new Date().toLocaleTimeString(),
      },
      
    ]);
    setInput("");
    setLoading(true);
  //  connect with backend
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
          time:new Date().toLocaleTimeString(),
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          text: "Can't connect to Server",
          sender: "bot",
          time:new Date().toLocaleTimeString(),
        },
      ]);
    }

    setLoading(false);
  };
  // Download Chat
  const handleDownloadChat=()=>{
    if(messages.length===0){
      alert("No chat available to download.");
      return;
    }
    let chatText="Chat\n";
    messages.forEach((msg) => {
      const sender = msg.sender === "user" ? "You" : "Bot";

     chatText += `[${msg.time}] ${sender}: ${msg.text}\n\n`;
    }); 

    const blob=new Blob([chatText],{
      type:"text/plain",
    });

    const url=window.URL.createObjectURL(blob);
    const link=document.createElement("a");
    link.href=url;
    link.download="Chat.txt";

    document.body.appendChild(link);
    link.click();

    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
    setShowMenu(false);

  };

  return (
    <>
      <h1>AI Assistant</h1>

      <ChatbotIcon toggleChat={toggleChat} isOpen={isOpen} />
      {isOpen && (
        <div className="chatbot-window">
          {/* Header */}
          <div className="chat-header-pro">
            <div className="header-left">
              <div className="bot-avatar-header">
                <MdSmartToy size={20} />
                <span className="online-dot"></span>
              </div>
              <div>
                <h3>Bot</h3>
                <p>Customer Support</p>
              </div>
            </div>

          <div className="header-right" ref={menuRef} style={{ display: "flex", gap: 8 }}>
            {/* Menu Button */}
            <button className="menu-btn" onClick={() => setShowMenu(!showMenu)}>
              <FiMenu size={20} />
            </button>
            {/* Dropdown Menu */}
            {showMenu && (
              <div className="chat-menu-dropdown">
                <button onClick={handleDownloadChat} className="menu-item">
                  <RiDownloadCloud2Line size={16}/> Download Chat
                </button>
                <button onClick={handleContactSupport} className="menu-item">
                  <FiMail size={16} /> Contact Support
                </button>
                <button onClick={handleCloseChat} className="menu-item close-item">
                  <FiLogOut size={16} /> Close Chat
                </button>
              </div>
            )}
          </div>
        </div>

          {/* Chat Body */}
          <div className="chat-body">
          {messages.map((msg,index)=>(
            <div key ={index} className={`message-row ${msg.sender}`}>
            {msg.sender==="bot"&&(
              <div className="avatar-col">
              <div className="bot-avatar-circle">
              <MdSmartToy size={16}/>
              </div>
              <span>Bot</span>
            </div>  
            )}
            <div className={`message-bubble ${msg.sender}`}>
             <ReactMarkdown>{msg.text}</ReactMarkdown>
            </div>

            {msg.sender==="user"&&(
              <div className="avatar-col">
                <div className="user-avatar-circle">
               <MdPerson size={16}/>
               </div>
              <span>You</span>
              </div>

            )}
          </div>  
          ))}
          {/* Contact Support Form */}
          {showSupportForm && (
             <div className="message-row bot">
              <div className="avatar-col">
              <div className="bot-avatar-circle">
              <MdSmartToy size={16} />
               </div>
               <span>Bot</span>
               </div>
               <div className="contact-card" ref={formRef}>
                  <h4 className="contact-title">Contact Support</h4>
                  <p className="contact-desc">We'll get back to you within 24 hours</p>
                  <div className="support-form">
                  <input
                  name="name"
                  className={errors.name?"error":""}
                  placeholder="Enter Your Name *"
                  value={supportForm.name}
                  onChange={handleSupportChange}
                  required
                  />
                  {errors.name && <p className="error">{errors.name}</p>}
                  <input
                  type="email"
                  className={errors.email?"error":""}
                  name="email"
                  placeholder="Enter Your Email ID *"
                  value={supportForm.email}
                  onChange={handleSupportChange}
                 />
                 {errors.email && <p className="error">{errors.email}</p>}
                 <input
                  type="tel"
                  className={errors.PhoneNumber?"error":""}
                  name="PhoneNumber"
                  placeholder="Phone No"
                  value={supportForm.PhoneNumber}
                  onChange={handleSupportChange}
                 />
                 {errors.PhoneNumber && <p className="error">{errors.PhoneNumber}</p>}
                 <input
                  type="text"
                  className={errors.subject?"error":""}
                  name="subject"
                  placeholder="Subject"
                  value={supportForm.subject}
                  onChange={handleSupportChange}
                 />
                 {errors.subject && <p className="error">{errors.subject}</p>}
                 <textarea
                  name="message"
                  className={errors.message?"error":""}
                  rows={5}
                  placeholder="Write your issue... *"
                  value={supportForm.message}
                  onChange={handleSupportChange}
                  required
                  />
                  {errors.message && <p className="error">{errors.message}</p>}
                  <button onClick={submitSupportForm} className="contact-submit">
                   Submit
                  </button>
              </div>
             </div>
        
          </div>
          )}
              {/* Typing Indicator */}
               {loading &&(
                <div className="bot-typing">
                  <span></span>
                  <span></span>
                  <span></span>
                </div> 

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