import React, { useState, useEffect, useCallback } from 'react';
import { uploadKnowledgeBase, getChatbotData } from '../../utils/api';
import FlowEditor from '../FlowEditor/FlowEditor';

const KnowledgeBase = ({ chatbot, userId, onUploadSuccess }) => {
    const [file, setFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [message, setMessage] = useState(null);
    const [showFlow, setShowFlow] = useState(false);
    const [csvData, setCsvData] = useState([]);

    const fetchData = useCallback(async () => {
        if (!chatbot?.id) return;
        try {
            const data = await getChatbotData(userId, chatbot.id);
            setCsvData(data);
        } catch (error) {
            console.error("Error fetching bot data:", error);
        }
    }, [chatbot?.id, userId]);

    useEffect(() => {
        fetchData();
    }, [fetchData]);

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        setFile(selectedFile);
        setMessage(null);

        // Preview CSV logic (simplified)
        if (selectedFile) {
            const reader = new FileReader();
            reader.onload = (event) => {
                const text = event.target.result;
                const rows = text.split('\n').filter(r => r.trim()).slice(1);
                const data = rows.map(row => {
                    const [q, a] = row.split(',');
                    return { Question: q, Answer: a };
                });
                setCsvData(data);
            };
            reader.readAsText(selectedFile);
        }
    };

    const handleUpload = async (customData = null) => {
        let fileToUpload = file;

        if (customData) {
            const csvContent = "Question,Answer\n" + customData.map(row => `"${row.Question}","${row.Answer}"`).join('\n');
            fileToUpload = new File([csvContent], 'knowledge_base.csv', { type: 'text/csv' }); //?
        }

        if (!fileToUpload) {
            setMessage({ type: 'error', text: 'Please select a CSV file or use the Flow Editor.' });
            return;
        }

        setUploading(true);
        setMessage(null);

        try {
            const result = await uploadKnowledgeBase(userId, chatbot.id, fileToUpload);
            setMessage({
                type: 'success',
                text: `Success! Processed ${result.count} FAQs for ${chatbot.name}.`
            });

            // Redirect based on source
            setTimeout(async () => {
                if (customData) {
                    if (onUploadSuccess) onUploadSuccess('preview');
                } else {
                    // Refetch latest data from backend to ensure Flow Designer is accurate
                    await fetchData();
                    setShowFlow(true);
                }
            }, 1000);

            if (!customData) {
                setFile(null);
                const input = document.getElementById('faq-upload');
                if (input) input.value = '';
            }
        } catch (error) {
            console.error("Upload error:", error);
            setMessage({ type: 'error', text: 'Failed to upload knowledge base. Please try again.' });
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="tab-content">
            <div className="tab-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '40px' }}>
                <div>
                    <h3 style={{ fontSize: '1.25rem', fontWeight: '800', color: '#1e293b', marginBottom: '8px' }}>Bot Training: {chatbot.name}</h3>
                    <p style={{ color: '#64748b', fontSize: '0.95rem' }}>Train your bot using a CSV file or the Interactive Flow Designer.</p>
                </div>
                <div className="toggle-container" style={{ background: '#f1f5f9', padding: '6px', borderRadius: '12px', display: 'flex', gap: '8px' }}>
                    <button
                        className={`toggle-btn ${!showFlow ? 'active' : ''}`}
                        onClick={() => setShowFlow(false)}
                        style={{
                            padding: '8px 16px',
                            borderRadius: '8px',
                            border: 'none',
                            fontSize: '0.85rem',
                            fontWeight: '600',
                            cursor: 'pointer',
                            transition: 'all 0.2s',
                            background: !showFlow ? 'white' : 'transparent',
                            color: !showFlow ? '#6366f1' : '#64748b',
                            boxShadow: !showFlow ? '0 2px 4px rgba(0,0,0,0.05)' : 'none'
                        }}
                    >
                        File Upload
                    </button>
                    <button
                        className={`toggle-btn ${showFlow ? 'active' : ''}`}
                        onClick={() => setShowFlow(true)}
                        style={{
                            padding: '8px 16px',
                            borderRadius: '8px',
                            border: 'none',
                            fontSize: '0.85rem',
                            fontWeight: '600',
                            cursor: 'pointer',
                            transition: 'all 0.2s',
                            background: showFlow ? 'white' : 'transparent',
                            color: showFlow ? '#6366f1' : '#64748b',
                            boxShadow: showFlow ? '0 2px 4px rgba(0,0,0,0.05)' : 'none'
                        }}
                    >
                        Flow Designer
                    </button>
                </div>
            </div>

            {!showFlow ? (
                <div className="upload-zone">
                    <div className="upload-icon">📄</div>
                    <input
                        type="file"
                        id="faq-upload"
                        accept=".csv"
                        onChange={handleFileChange}
                    />
                    {file && <p className="selected-file">Selected: {file.name}</p>}

                    <button
                        className="deploy-btn"
                        onClick={() => handleUpload()}
                        disabled={uploading || !file}
                    >
                        {uploading ? 'Processing...' : 'Upload Knowledge Base'}
                    </button>
                </div>
            ) : (
                <FlowEditor
                    initialData={csvData}
                    onSave={(updatedData) => handleUpload(updatedData)}
                />
            )}

            {message && (
                <div className={`status-message ${message.type}`} style={{
                    marginTop: '20px',
                    padding: '12px',
                    borderRadius: '8px',
                    backgroundColor: message.type === 'success' ? '#ecfdf5' : '#fef2f2',
                    color: message.type === 'success' ? '#065f46' : '#991b1b',
                    border: `1px solid ${message.type === 'success' ? '#10b981' : '#ef4444'}`
                }}>
                    {message.text}
                </div>
            )}

            <div className="template-download" style={{ marginTop: '20px', fontSize: '0.9rem' }}>
                <p>Don't have a file? <a href="#" onClick={(e) => {
                    e.preventDefault();
                    const csvContent = "Question,Answer\nHi,Hello! How can I help you today?\nWhat is FAQSense?,FAQSense is an AI-powered FAQ management platform.";
                    const blob = new Blob([csvContent], { type: 'text/csv' });
                    const url = URL.createObjectURL(blob);
                    const link = document.createElement('a');
                    link.href = url;
                    link.download = 'faq_template.csv';
                    link.click();
                }}>Download Template</a></p>
            </div>
        </div>
    );
};

export default KnowledgeBase;
