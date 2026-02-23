import React from 'react';

const AllConversations = ({ chatbot }) => {
    return (
        <div className="tab-content">
            <div className="tab-header">
                <h3>All Conversations: {chatbot.name}</h3>
                <p>Review interaction history and user messages.</p>
            </div>
            <div className="tab-placeholder" style={{ marginTop: '20px' }}>
                Conversation history tracking will be available soon.
            </div>
        </div>
    );
};

export default AllConversations;
