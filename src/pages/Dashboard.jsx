import React, { useState, useEffect } from 'react';
import { useUser, UserButton } from "@clerk/clerk-react";
import { Link } from 'react-router-dom';
import { getChatbots, createChatbot } from '../utils/api';
import KnowledgeBase from '../components/Dashboard/KnowledgeBase';
import EnquiryInbox from '../components/Dashboard/EnquiryInbox';
import ChatbotAnalytics from '../components/Dashboard/ChatbotAnalytics';
import ChatbotCard from '../components/Dashboard/ChatbotCard';
import ChatbotPreview from '../components/Dashboard/ChatbotPreview';
import AllConversations from '../components/Dashboard/AllConversations';
import './Dashboard.css';

const Dashboard = () => {
    const { user, isLoaded } = useUser();
    const [chatbots, setChatbots] = useState([]);
    const [selectedBot, setSelectedBot] = useState(null);
    const [activeTab, setActiveTab] = useState('kb'); // kb, enquiries, analytics, preview, conversations, settings
    const [newBotName, setNewBotName] = useState('');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        let active = true;
        if (isLoaded && user) {
            const fetchBots = async () => {
                console.log("Fetching chatbots for user:", user.id);
                try {
                    const data = await getChatbots(user.id);
                    if (active) {
                        console.log("Chatbots fetched:", data);
                        setChatbots(data);
                    }
                } catch (error) {
                    console.error("Error fetching bots:", error);
                } finally {
                    if (active) {
                        console.log("Setting loading to false");
                        setLoading(false);
                    }
                }
            };
            fetchBots();
        }
        return () => {
            active = false;
        };
    }, [isLoaded, user]);


    const handleCreateBot = async (e) => {
        e.preventDefault();
        if (!newBotName.trim()) return;
        try {
            const newBot = await createChatbot(user.id, newBotName);
            setChatbots([...chatbots, newBot]);
            setSelectedBot(newBot);
            setNewBotName('');
            setActiveTab('kb');
        } catch (error) {
            console.error("Error creating bot:", error);
        }
    };

    if (!isLoaded || loading) return <div className="loading">Loading FAQSense Dashboard...</div>;

    const renderManagementView = () => (
        <>
            <header className="dashboard-header">
                <div className="header-title-row">
                    <button className="back-btn" onClick={() => setSelectedBot(null)}>← Back</button>
                    <h2>Management: {selectedBot.name}</h2>
                </div>
                <div className="header-tabs">
                    <button className={`tab-btn ${activeTab === 'kb' ? 'active' : ''}`} onClick={() => setActiveTab('kb')}>Knowledge Base</button>
                    <button className={`tab-btn ${activeTab === 'enquiries' ? 'active' : ''}`} onClick={() => setActiveTab('enquiries')}>Enquiries</button>
                    <button className={`tab-btn ${activeTab === 'analytics' ? 'active' : ''}`} onClick={() => setActiveTab('analytics')}>Analytics</button>
                    <button className={`tab-btn ${activeTab === 'preview' ? 'active' : ''}`} onClick={() => setActiveTab('preview')}>Preview</button>
                    <button className={`tab-btn ${activeTab === 'conversations' ? 'active' : ''}`} onClick={() => setActiveTab('conversations')}>All Conversations</button>
                    <button className={`tab-btn ${activeTab === 'settings' ? 'active' : ''}`} onClick={() => setActiveTab('settings')}>Settings</button>
                </div>
            </header>

            <section className="dashboard-content">
                {activeTab === 'kb' && <KnowledgeBase chatbot={selectedBot} userId={user.id} onUploadSuccess={setActiveTab} />}
                {activeTab === 'enquiries' && <EnquiryInbox chatbot={selectedBot} userId={user.id} />}
                {activeTab === 'analytics' && <ChatbotAnalytics chatbot={selectedBot} userId={user.id} />}
                {activeTab === 'preview' && <ChatbotPreview chatbot={selectedBot} />}
                {activeTab === 'conversations' && <AllConversations chatbot={selectedBot} />}
                {activeTab === 'settings' && <div className="tab-placeholder">Chatbot Settings Coming Soon</div>}
            </section>
        </>
    );

    const renderCollectionView = () => (
        <div className="collection-view">
            <header className="collection-header">
                <h1>My Chatbots</h1>
                <p>Select a chatbot to manage it or create a new one.</p>
            </header>

            <div className="chatbot-grid">
                {chatbots.map(bot => (
                    <ChatbotCard
                        key={bot.id}
                        chatbot={bot}
                        onClick={(bot) => {
                            setSelectedBot(bot);
                            setActiveTab('kb');
                        }}
                    />
                ))}
            </div>

            <div className="create-bot-card">
                <form onSubmit={handleCreateBot}>
                    <input
                        type="text"
                        placeholder="Name your new AI assistant..."
                        value={newBotName}
                        onChange={(e) => setNewBotName(e.target.value)}
                    />
                    <button type="submit">✨ Create New Bot</button>
                </form>
            </div>
        </div>
    );

    return (
        <div className="dashboard-container">
            <aside className="dashboard-sidebar">
                <div className="sidebar-logo">FAQSense<span>.ai</span></div>
                <nav className="sidebar-nav">
                    <Link to="/" className="nav-item">🏠 Home</Link>
                    <div
                        className={`nav-item ${!selectedBot ? 'active' : ''}`}
                        onClick={() => setSelectedBot(null)}
                    >
                        🤖 My Chatbots
                    </div>
                </nav>
                <div className="sidebar-footer">
                    <div className="user-profile">
                        <UserButton afterSignOutUrl="/" />
                        <div className="user-info">
                            <span className="user-name">{user.fullName || user.username}</span>
                        </div>
                    </div>
                </div>
            </aside>

            <main className="dashboard-main">
                {selectedBot ? renderManagementView() : renderCollectionView()}
            </main>
        </div>
    );
};

export default Dashboard;
