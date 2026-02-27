import React, { useState, useEffect } from 'react';
import { useUser } from '@clerk/clerk-react';
import { getConversations } from '../../utils/api';
import './AllConversations.css';

const AllConversations = ({ chatbot, initialSelectedId }) => {
    const { user } = useUser();
    const [conversations, setConversations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedId, setSelectedId] = useState(initialSelectedId);

    useEffect(() => {
        const fetchConversations = async () => {
            if (!user) return;
            try {
                const data = await getConversations(user.id, chatbot?.id);
                // Sort by most recent
                const sorted = data.sort((a, b) => new Date(b.started_at) - new Date(a.started_at));
                setConversations(sorted);

                // If we have an initial ID, used it. Otherwise default to first one.
                if (initialSelectedId) {
                    setSelectedId(initialSelectedId);
                } else if (sorted.length > 0) {
                    setSelectedId(sorted[0].id);
                }
            } catch (error) {
                console.error("Error fetching conversations:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchConversations();
    }, [user]);

    const selectedConv = conversations.find(c => c.id === selectedId);

    if (loading) return <div className="tab-placeholder">Loading conversations...</div>;

    if (conversations.length === 0) {
        return (
            <div className="tab-placeholder">
                <div className="empty-state">
                    <span className="empty-icon">💬</span>
                    <h3>No conversations yet</h3>
                    <p>When visitors interact with your chatbots, their history will appear here.</p>
                </div>
            </div>
        );
    }

    return (
        <div className="conversations-layout">
            <div className="conversations-sidebar">
                <div className="sidebar-header">
                    <h4>Hits</h4>
                    <span className="count-badge">{conversations.length}</span>
                </div>
                <div className="conversations-list">
                    {conversations.map(conv => (
                        <div
                            key={conv.id}
                            className={`conv-item ${selectedId === conv.id ? 'active' : ''}`}
                            onClick={() => setSelectedId(conv.id)}
                        >
                            <div className="conv-item-info">
                                <span className="visitor-id">Visitor: {conv.visitor_id.substring(0, 8)}...</span>
                                <span className="conv-date">
                                    {new Date(conv.started_at).toLocaleDateString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                                </span>
                            </div>
                            <div className="conv-preview">
                                {conv.messages && conv.messages.length > 0 ?
                                    conv.messages[conv.messages.length - 1].content :
                                    "No messages"}
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            <div className="conversation-detail">
                {selectedConv ? (
                    <>
                        <div className="detail-header">
                            <div className="visitor-meta">
                                <h3>Conversation Log</h3>
                                <p>ID: {selectedConv.id}</p>
                            </div>
                            <div className="bot-meta">
                                <span className="bot-label">Bot ID: {selectedConv.chatbot_id}</span>
                            </div>
                        </div>
                        <div className="messages-display">
                            {selectedConv.messages && selectedConv.messages.length > 0 ? (
                                selectedConv.messages.map((msg, i) => (
                                    <div key={i} className={`msg-row ${msg.sender}`}>
                                        <div className="msg-bubble">
                                            <div className="msg-sender-label">{msg.sender}</div>
                                            <div className="msg-text">{msg.content}</div>
                                            <div className="msg-time">
                                                {new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                            </div>
                                        </div>
                                    </div>
                                ))
                            ) : (
                                <div className="no-messages">No messages found for this conversation.</div>
                            )}
                        </div>
                    </>
                ) : (
                    <div className="no-selection">Select a conversation to view details</div>
                )}
            </div>
        </div>
    );
};

export default AllConversations;
