import React, { useState } from 'react';
import ChatWindow from '../Chatbot/ChatWindow';

const ChatbotPreview = ({ chatbot }) => {
    const [showEmbed, setShowEmbed] = useState(false);
    const [copied, setCopied] = useState(false);

    const embedCode = `<script 
  src="http://localhost:8000/static/widget.js" 
  data-bot-id="${chatbot.id}"
  async>
</script>`;

    const handleCopy = () => {
        navigator.clipboard.writeText(embedCode);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <div className="tab-content">
            <div className="tab-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div>
                    <h3 style={{ fontSize: '1.25rem', fontWeight: '800', color: '#1e293b', marginBottom: '8px' }}>Preview: {chatbot.name}</h3>
                    <p style={{ color: '#64748b', fontSize: '0.95rem' }}>Interact with your chatbot to see how it behaves with the current knowledge base.</p>
                </div>
                <button
                    onClick={() => setShowEmbed(!showEmbed)}
                    style={{
                        background: 'linear-gradient(135deg, #6366f1, #a855f7)',
                        color: 'white',
                        border: 'none',
                        padding: '10px 20px',
                        borderRadius: '10px',
                        fontWeight: '700',
                        fontSize: '0.9rem',
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        boxShadow: '0 4px 12px rgba(99, 102, 241, 0.3)',
                        transition: 'all 0.2s'
                    }}
                    className="go-live-btn"
                >
                    🚀 Go Live!
                </button>
            </div>

            {showEmbed && (
                <div className="embed-code-section" style={{
                    marginTop: '24px',
                    padding: '24px',
                    background: '#1e293b',
                    borderRadius: '16px',
                    color: '#e2e8f0',
                    animation: 'slideDown 0.3s ease-out'
                }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
                        <span style={{ fontWeight: '600', fontSize: '1rem', color: '#818cf8' }}>Embed Script</span>
                        <button
                            onClick={handleCopy}
                            style={{
                                background: copied ? '#10b981' : 'rgba(255,255,255,0.1)',
                                color: 'white',
                                border: 'none',
                                padding: '6px 12px',
                                borderRadius: '6px',
                                cursor: 'pointer',
                                fontSize: '0.8rem',
                                transition: 'all 0.2s'
                            }}
                        >
                            {copied ? '✓ Copied!' : 'Copy Code'}
                        </button>
                    </div>
                    <pre style={{
                        background: '#0f172a',
                        padding: '16px',
                        borderRadius: '8px',
                        fontSize: '0.85rem',
                        overflowX: 'auto',
                        fontFamily: 'monospace',
                        lineHeight: '1.5',
                        border: '1px solid rgba(255,255,255,0.05)'
                    }}>
                        {embedCode}
                    </pre>
                    <p style={{ marginTop: '12px', fontSize: '0.8rem', color: '#94a3b8' }}>
                        Paste this script at the end of your <code>&lt;body&gt;</code> tag to enable FAQSense on your website.
                    </p>
                </div>
            )}

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
