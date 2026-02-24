import React, { useState, useEffect } from 'react';
import { getTopFaqs } from '../../utils/api';

const ChatbotAnalytics = ({ chatbot }) => {
    const [topFaqs, setTopFaqs] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        let active = true;
        const fetchAnalytics = async () => {
            setLoading(true);
            try {
                const data = await getTopFaqs(chatbot.id);
                if (active) {
                    setTopFaqs(data.slice(0, 5));
                }
            } catch (error) {
                console.error("Error fetching analytics:", error);
            } finally {
                if (active) {
                    setLoading(false);
                }
            }
        };

        fetchAnalytics();

        return () => {
            active = false;
        };
    }, [chatbot.id]);


    if (loading) return <div className="loading-small">Fetching analytics...</div>;

    return (
        <div className="tab-content">
            <div className="tab-header">
                <h3>Popular Questions: {chatbot.name}</h3>
                <p>Understand what your customers are asking the most.</p>
            </div>

            <div className="analytics-section">
                {topFaqs.length === 0 ? (
                    <div className="empty-state">No data available yet. Start chatting to see analytics!</div>
                ) : (
                    <div className="top-faqs-list">
                        {topFaqs.map((faq, index) => (
                            <div key={index} className="faq-analytic-item">
                                <div className="faq-rank">#{index + 1}</div>
                                <div className="faq-info">
                                    <div className="faq-question">{faq.original_question}</div>
                                    <div className="faq-hits">{faq.hits} hits</div>
                                </div>
                                <div className="faq-progress-bar">
                                    <div
                                        className="progress-fill"
                                        style={{ width: `${(faq.hits / topFaqs[0].hits) * 100}%` }}
                                    ></div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default ChatbotAnalytics;
