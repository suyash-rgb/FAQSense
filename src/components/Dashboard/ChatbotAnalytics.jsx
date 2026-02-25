import React, { useState, useEffect } from 'react';
import { getChatbotStats } from '../../utils/api';
import './ChatbotAnalytics.css';

const ChatbotAnalytics = ({ chatbot, userId }) => {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        let active = true;
        const fetchStats = async () => {
            setLoading(true);
            try {
                const data = await getChatbotStats(userId, chatbot.id);
                if (active) {
                    setStats(data);
                }
            } catch (error) {
                console.error("Error fetching analytics:", error);
            } finally {
                if (active) {
                    setLoading(false);
                }
            }
        };

        fetchStats();

        return () => {
            active = false;
        };
    }, [chatbot.id, userId]);

    if (loading) return (
        <div className="analytics-loading">
            <div className="loader"></div>
            <p>Crunching the numbers...</p>
        </div>
    );

    if (!stats) return <div className="empty-state">Unable to load analytics data.</div>;

    const { total_faq_hits, total_enquiries, total_conversations, resolved_enquiries, total_chatbot_clicks, top_faqs } = stats;

    return (
        <div className="analytics-container">
            <div className="analytics-header">
                <h3>Performance Overview: {chatbot.name}</h3>
                <p>Real-time insights into your bot's performance and engagement.</p>
            </div>

            <div className="stats-grid">
                <div className="stat-card">
                    <div className="stat-icon hits">📊</div>
                    <div className="stat-info">
                        <span className="stat-label">Total FAQ Hits</span>
                        <span className="stat-value">{total_faq_hits}</span>
                    </div>
                </div>
                <div className="stat-card">
                    <div className="stat-icon convs">💬</div>
                    <div className="stat-info">
                        <span className="stat-label">Total Conversations</span>
                        <span className="stat-value">{total_conversations}</span>
                    </div>
                </div>
                <div className="stat-card">
                    <div className="stat-icon enquiries">📩</div>
                    <div className="stat-info">
                        <span className="stat-label">Unanswered Enquiries</span>
                        <span className="stat-value">{total_enquiries - resolved_enquiries}</span>
                    </div>
                </div>
                <div className="stat-card">
                    <div className="stat-icon conversion">📈</div>
                    <div className="stat-info">
                        <span className="stat-label">Resolution Rate</span>
                        <span className="stat-value">
                            {total_conversations > 0
                                ? Math.round(((total_conversations - total_enquiries) / total_conversations) * 100)
                                : 0}%
                        </span>
                    </div>
                </div>
                <div className="stat-card">
                    <div className="stat-icon clicks">🖱️</div>
                    <div className="stat-info">
                        <span className="stat-label">Click Throughs</span>
                        <span className="stat-value">{total_chatbot_clicks.toLocaleString()}</span>
                    </div>
                </div>
            </div>

            <div className="analytics-charts-row">
                <div className="chart-container large">
                    <h4>Most Frequent FAQs</h4>
                    {top_faqs.length === 0 ? (
                        <div className="empty-chart">No FAQ data yet.</div>
                    ) : (
                        <div className="vertical-bar-chart">
                            {top_faqs.map((faq, index) => (
                                <div key={index} className="faq-bar-item">
                                    <div className="faq-bar-label">
                                        <span className="faq-text" title={faq.original_question}>{faq.original_question}</span>
                                        <span className="faq-count">{faq.hit_count} hits</span>
                                    </div>
                                    <div className="faq-bar-outer">
                                        <div
                                            className="faq-bar-inner"
                                            style={{ width: `${(faq.hit_count / top_faqs[0].hit_count) * 100}%` }}
                                        >
                                            <span className="bar-percentage">{Math.round((faq.hit_count / total_faq_hits) * 100)}%</span>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>

                <div className="chart-container small">
                    <h4>Engagement Health</h4>
                    <div className="health-metrics">
                        <div className="health-circle">
                            <svg viewBox="0 0 36 36" className="circular-chart indigo">
                                <path className="circle-bg"
                                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                                />
                                <path className="circle"
                                    strokeDasharray={`${total_conversations > 0 ? ((total_conversations - total_enquiries) / total_conversations) * 100 : 0}, 100`}
                                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                                />
                                <text x="18" y="20.35" className="percentage">
                                    {total_conversations > 0 ? Math.round(((total_conversations - total_enquiries) / total_conversations) * 100) : 0}%
                                </text>
                            </svg>
                        </div>
                        <p className="health-note">Self-service resolution rate</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ChatbotAnalytics;
