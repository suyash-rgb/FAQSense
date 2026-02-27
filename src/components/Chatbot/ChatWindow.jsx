import React, { useState, useEffect, useRef } from 'react';
import { getTopFaqs, askQuestion, submitEnquiry, recordChatbotClick } from '../../utils/api';
import './ChatWindow.css';

const ChatWindow = ({ initialBotId, height = '520px', forceOpen = false, isWidget = false }) => {
    const chatbotId = initialBotId || new URLSearchParams(window.location.search).get('id') || 1;
    const [messages, setMessages] = useState([
        { text: "Hi there! How can I help you today?", sender: 'bot' }
    ]);
    const [input, setInput] = useState('');
    const [isOpen, setIsOpen] = useState(forceOpen);
    const [topFaqs, setTopFaqs] = useState([]);
    const [conversationId, setConversationId] = useState(null);
    const [showEnquiryForm, setShowEnquiryForm] = useState(false);
    const [isTyping, setIsTyping] = useState(false);
    const [enquiryData, setEnquiryData] = useState({ name: '', contact: '' });

    const messagesEndRef = useRef(null);
    const scrollContainerRef = useRef(null);

    const scrollToBottom = () => {
        if (scrollContainerRef.current) {
            scrollContainerRef.current.scrollTop = scrollContainerRef.current.scrollHeight;
        }
    };

    const handleToggle = () => {
        if (!isOpen) {
            // Record click when opening
            recordChatbotClick(chatbotId).catch(err => console.error("Error recording click:", err));
        }
        setIsOpen(!isOpen);
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isTyping]);

    useEffect(() => {
        let active = true;
        // Reset messages and session when bot changes
        setMessages([{ text: "Hi there! How can I help you today?", sender: 'bot' }]);
        setConversationId(`conv_${Math.random().toString(36).substr(2, 9)}`);
        setShowEnquiryForm(false);

        // Fetch suggestions
        const fetchSuggestions = async () => {
            try {
                const faqs = await getTopFaqs(chatbotId);
                if (active) {
                    setTopFaqs(faqs.slice(0, 3));
                }
            } catch (error) {
                console.error("Error fetching suggestions:", error);
            }
        };
        fetchSuggestions();

        return () => {
            active = false;
        };
    }, [chatbotId]);

    const handleSend = async (text) => {
        if (!text.trim()) return;

        const userMsg = { text, sender: 'user' };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setIsTyping(true);
        setShowEnquiryForm(false); // Hide fallback form if user manually type/sends something
        try {
            const response = await askQuestion(chatbotId, text, conversationId);
            setIsTyping(false);

            const botMsg = { text: response.answer, sender: 'bot' };
            setMessages(prev => [...prev, botMsg]);

            // Fallback trigger
            if (response.answer.includes("I did not understand")) {
                setShowEnquiryForm(true);
            }
        } catch (error) {
            console.error("Chat Error:", error);
            setIsTyping(false);
            const errorMsg = error.response ?
                `Error ${error.response.status}: ${error.response.data?.detail || 'Server error'}` :
                "Connection failed. Please check if your backend is running.";
            setMessages(prev => [...prev, { text: `Sorry, I'm having trouble connecting. (${errorMsg})`, sender: 'bot' }]);
        }
    };

    const handleEnquirySubmit = async (e) => {
        e.preventDefault();
        try {
            const isEmail = enquiryData.contact.includes('@');
            await submitEnquiry(chatbotId, {
                visitor_name: enquiryData.name,
                visitor_email: isEmail ? enquiryData.contact : null,
                visitor_phone: !isEmail ? enquiryData.contact : null,
                query_text: messages[messages.length - 2].text // Use the user's last question
            });
            setMessages(prev => [...prev, { text: "Thank you! Your enquiry has been registered. We'll get back to you soon.", sender: 'bot' }]);
            setShowEnquiryForm(false);
        } catch (error) {
            console.error("Enquiry submission error:", error);
        }
    };

    return (
        <div className={`chatbot-container ${isOpen ? 'open' : ''} ${isWidget ? 'is-widget' : ''}`}>
            {!isOpen && (
                <button className="chat-toggle" onClick={handleToggle}>
                    <span className="chat-icon">💬</span>
                </button>
            )}

            {isOpen && (
                <div className="chat-window glass" style={{ height }}>
                    <div className="chat-header">
                        <h3>FAQSense Chat</h3>
                        <button className="close-btn" onClick={handleToggle}>×</button>
                    </div>

                    <div className="chat-messages" ref={scrollContainerRef}>
                        {messages.map((msg, idx) => (
                            <div key={idx} className={`message ${msg.sender}`}>
                                <div className="message-bubble">
                                    {msg.text}
                                </div>
                            </div>
                        ))}

                        {isTyping && (
                            <div className="message bot">
                                <div className="message-bubble typing">
                                    <span className="dot"></span>
                                    <span className="dot"></span>
                                    <span className="dot"></span>
                                </div>
                            </div>
                        )}

                        {!showEnquiryForm && messages.length === 1 && topFaqs && topFaqs.length > 0 && (
                            <div className="suggestions">
                                <p>Popular Questions:</p>
                                <div className="chip-container">
                                    {topFaqs.map((faq, i) => (
                                        <button key={i} className="faq-chip" onClick={() => handleSend(faq)}>
                                            {faq}
                                        </button>
                                    ))}
                                </div>
                            </div>
                        )}

                        {showEnquiryForm && (
                            <div className="enquiry-form-container">
                                <form onSubmit={handleEnquirySubmit} className="mini-enquiry-form">
                                    <div className="enquiry-header">
                                        <p>Leave your details and we'll reply via email:</p>
                                        <button
                                            type="button"
                                            className="dismiss-enquiry"
                                            onClick={() => setShowEnquiryForm(false)}
                                            title="I'll just rephrase my question"
                                        >
                                            ×
                                        </button>
                                    </div>
                                    <input
                                        type="text"
                                        placeholder="Your Name"
                                        required
                                        value={enquiryData.name}
                                        onChange={e => setEnquiryData({ ...enquiryData, name: e.target.value })}
                                    />
                                    <input
                                        type="text"
                                        placeholder="Email or Phone"
                                        required
                                        value={enquiryData.contact}
                                        onChange={e => setEnquiryData({ ...enquiryData, contact: e.target.value })}
                                    />
                                    <button type="submit" className="submit-enquiry-btn">Submit Request</button>
                                </form>
                            </div>
                        )}
                    </div>

                    <form className="chat-input" onSubmit={(e) => { e.preventDefault(); handleSend(input); }}>
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Type a message..."
                        />
                        <button type="submit" aria-label="Send message">
                            <img src="/sendbutton.png" alt="Send" className="send-icon" />
                        </button>
                    </form>
                </div>
            )}
        </div>
    );
};

export default ChatWindow;
