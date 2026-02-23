import React from 'react';
import ChatWindow from '../Chatbot/ChatWindow';

const ChatbotPreview = ({ chatbot }) => {
    return (
        <div className="tab-content">
            <div className="tab-header">
                <h3>Preview: {chatbot.name}</h3>
                <p>Interact with your chatbot to see how it behaves with the current knowledge base.</p>
            </div>
            <div className="preview-container" style={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                minHeight: '500px',
                border: '1px solid #e2e8f0',
                borderRadius: '12px',
                marginTop: '20px',
                background: '#f8fafc',
                position: 'relative',
                padding: '20px'
            }}>
                <ChatWindow initialBotId={chatbot.id} height="450px" forceOpen={true} />
            </div>
        </div>
    );
};

export default ChatbotPreview;
