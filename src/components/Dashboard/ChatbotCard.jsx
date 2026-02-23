import React from 'react';
import './ChatbotCard.css';

const ChatbotCard = ({ chatbot, onClick }) => {
    return (
        <div className="chatbot-card" onClick={() => onClick(chatbot)}>
            <div className="chatbot-card-icon">🤖</div>
            <div className="chatbot-card-info">
                <h3>{chatbot.name}</h3>
                <p>Status: Active</p>
            </div>
            <div className="chatbot-card-arrow">→</div>
        </div>
    );
};

export default ChatbotCard;
