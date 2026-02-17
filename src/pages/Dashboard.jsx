import React from 'react';
import FlowEditor from '../components/FlowEditor/FlowEditor';
import ChatWindow from '../components/Chatbot/ChatWindow';
import { Link } from 'react-router-dom';
import './Dashboard.css';

const Dashboard = () => {
    return (
        <div className="dashboard-container">
            <aside className="dashboard-sidebar">
                <div className="sidebar-logo">FAQSense<span>.ai</span></div>
                <nav className="sidebar-nav">
                    <Link to="/" className="nav-item">🏠 Home</Link>
                    <div className="nav-item active">🧠 Flow Editor</div>
                    <div className="nav-item">📊 Analytics</div>
                    <div className="nav-item">⚙️ Settings</div>
                </nav>
                <div className="sidebar-footer">
                    <div className="user-profile">
                        <div className="user-avatar">AD</div>
                        <span>Admin User</span>
                    </div>
                </div>
            </aside>

            <main className="dashboard-main">
                <header className="dashboard-header">
                    <h2>Neural Flow Editor</h2>
                    <div className="header-actions">
                        <button className="deploy-btn">Deploy to Live</button>
                    </div>
                </header>

                <section className="dashboard-content">
                    <FlowEditor />
                </section>

                <ChatWindow />
            </main>
        </div>
    );
};

export default Dashboard;
