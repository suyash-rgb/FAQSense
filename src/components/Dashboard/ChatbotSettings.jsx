import React, { useState } from 'react';
import { deleteChatbot } from '../../utils/api';
import { toast } from 'react-hot-toast';
import './ChatbotSettings.css';

const ChatbotSettings = ({ chatbot, userId, onDeleteSuccess }) => {
    const [isDeleting, setIsDeleting] = useState(false);
    const [confirmName, setConfirmName] = useState('');

    const handleDelete = async () => {
        if (confirmName !== chatbot.name) {
            toast.error("Please type the chatbot name correctly to confirm.");
            return;
        }

        const loadingToast = toast.loading("Deleting chatbot...");
        setIsDeleting(true);
        try {
            await deleteChatbot(userId, chatbot.id);
            toast.success("Chatbot deleted successfully", { id: loadingToast });
            if (onDeleteSuccess) onDeleteSuccess();
        } catch (error) {
            console.error("Error deleting chatbot:", error);
            toast.error("Failed to delete chatbot", { id: loadingToast });
            setIsDeleting(false);
        }
    };

    return (
        <div className="tab-content settings-tab">
            <div className="tab-header">
                <div>
                    <h3 className="settings-title">Chatbot Settings</h3>
                    <p className="settings-subtitle">Manage configuration and lifecycle for <strong>{chatbot.name}</strong></p>
                </div>
            </div>

            <div className="settings-grid">
                <div className="settings-card">
                    <div className="card-header">
                        <h4>General Information</h4>
                    </div>
                    <div className="card-body">
                        <div className="settings-item">
                            <label>Chatbot Name</label>
                            <input type="text" value={chatbot.name} readOnly disabled />
                        </div>
                        <div className="settings-item">
                            <label>Chatbot ID</label>
                            <input type="text" value={chatbot.id} readOnly disabled />
                            <small>Unique identifier for API integration</small>
                        </div>
                        <div className="settings-item">
                            <label>Created At</label>
                            <input type="text" value={new Date(chatbot.created_at).toLocaleString()} readOnly disabled />
                        </div>
                    </div>
                </div>

                <div className="settings-card danger-card">
                    <div className="card-header">
                        <h4>Danger Zone</h4>
                    </div>
                    <div className="card-body">
                        <p className="danger-text">
                            Deleting this chatbot will permanently remove all of its data, including:
                        </p>
                        <ul className="danger-list">
                            <li>Knowledge base and training data</li>
                            <li>Enquiry logs and visitor queries</li>
                            <li>Chat analytics and performance metrics</li>
                            <li>Conversation history</li>
                        </ul>

                        <div className="delete-confirmation">
                            <p>To confirm deletion, type <strong>{chatbot.name}</strong> below:</p>
                            <input
                                type="text"
                                value={confirmName}
                                onChange={(e) => setConfirmName(e.target.value)}
                                placeholder="Chatbot name..."
                                className="confirm-input"
                            />
                            <button
                                className={`delete-action-btn ${confirmName === chatbot.name ? 'enabled' : ''}`}
                                onClick={handleDelete}
                                disabled={isDeleting || confirmName !== chatbot.name}
                            >
                                {isDeleting ? 'Deleting...' : 'Permanently Delete Chatbot'}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ChatbotSettings;
