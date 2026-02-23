import React, { useState, useEffect, useRef } from 'react';
import { getTopFaqs, askQuestion, submitEnquiry } from '../../utils/api';
import './ChatWindow.css';

const ChatWindow = ({ initialBotId, height = '520px', forceOpen = false }) => {
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

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isTyping]);

    useEffect(() => {
        // Reset messages and session when bot changes
        setMessages([{ text: "Hi there! How can I help you today?", sender: 'bot' }]);
        setConversationId(`conv_${Math.random().toString(36).substr(2, 9)}`);
        setShowEnquiryForm(false);

        // Fetch suggestions
        const fetchSuggestions = async () => {
            try {
                const faqs = await getTopFaqs(chatbotId);
                setTopFaqs(faqs.slice(0, 3));
            } catch (error) {
                console.error("Error fetching suggestions:", error);
            }
        };
        fetchSuggestions();
    }, [chatbotId]);

    const handleSend = async (text) => {
        if (!text.trim()) return;

        const userMsg = { text, sender: 'user' };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setIsTyping(true);

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
            setIsTyping(false);
            setMessages(prev => [...prev, { text: "Sorry, I'm having trouble connecting.", sender: 'bot' }]);
        }
    };

    const handleEnquirySubmit = async (e) => {
        e.preventDefault();
        try {
            await submitEnquiry(chatbotId, {
                visitor_name: enquiryData.name,
                visitor_contact: enquiryData.contact,
                query_text: messages[messages.length - 2].text // Use the user's last question
            });
            setMessages(prev => [...prev, { text: "Thank you! Your enquiry has been registered. We'll get back to you soon.", sender: 'bot' }]);
            setShowEnquiryForm(false);
        } catch (error) {
            console.error("Enquiry submission error:", error);
        }
    };

    return (
        <div className={`chatbot-container ${isOpen ? 'open' : ''}`}>
            {!isOpen && (
                <button className="chat-toggle" onClick={() => setIsOpen(true)}>
                    <span className="chat-icon">💬</span>
                </button>
            )}

            {isOpen && (
                <div className="chat-window glass" style={{ height }}>
                    <div className="chat-header">
                        <h3>FAQSense Chat</h3>
                        <button className="close-btn" onClick={() => setIsOpen(false)}>×</button>
                    </div>

                    <div className="chat-messages">
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
                                    <p>Leave your details and we'll reply via email:</p>
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

                        <div ref={messagesEndRef} />
                    </div>

                    {!showEnquiryForm && (
                        <form className="chat-input" onSubmit={(e) => { e.preventDefault(); handleSend(input); }}>
                            <input
                                type="text"
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                placeholder="Type a message..."
                            />
                            <button type="submit">Send</button>
                        </form>
                    )}
                </div>
            )}
        </div>
    );
};

export default ChatWindow;
