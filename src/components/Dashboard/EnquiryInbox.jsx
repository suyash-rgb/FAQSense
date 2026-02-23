import React, { useState, useEffect } from 'react';
import { getEnquiries, updateEnquiry } from '../../utils/api';

const EnquiryInbox = ({ chatbot, userId }) => {
    const [enquiries, setEnquiries] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedEnquiry, setSelectedEnquiry] = useState(null);
    const [adminNotes, setAdminNotes] = useState('');
    const [updating, setUpdating] = useState(false);

    useEffect(() => {
        fetchEnquiries();
    }, [chatbot.id]);

    const fetchEnquiries = async () => {
        setLoading(true);
        try {
            const data = await getEnquiries(userId, chatbot.id);
            setEnquiries(data);
        } catch (error) {
            console.error("Error fetching enquiries:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleUpdateEnquiry = async (status) => {
        setUpdating(true);
        try {
            await updateEnquiry(userId, chatbot.id, selectedEnquiry.id, {
                status,
                admin_notes: adminNotes
            });
            setSelectedEnquiry(null);
            fetchEnquiries();
        } catch (error) {
            console.error("Error updating enquiry:", error);
        } finally {
            setUpdating(false);
        }
    };

    if (loading) return <div className="loading-small">Fetching enquiries...</div>;

    return (
        <div className="tab-content">
            <div className="tab-header">
                <h3>Enquiry Inbox: {chatbot.name}</h3>
                <p>Manage queries from visitors that your bot couldn't answer.</p>
            </div>

            <div className="enquiry-list">
                {enquiries.length === 0 ? (
                    <div className="empty-state">No enquiries yet.</div>
                ) : (
                    <table className="enquiry-table">
                        <thead>
                            <tr>
                                <th>Visitor</th>
                                <th>Contact</th>
                                <th>Query</th>
                                <th>Date</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {enquiries.map(enquiry => (
                                <tr key={enquiry.id}>
                                    <td>{enquiry.visitor_name}</td>
                                    <td>{enquiry.visitor_contact}</td>
                                    <td className="query-col">{enquiry.query_text}</td>
                                    <td>{new Date(enquiry.created_at).toLocaleDateString()}</td>
                                    <td>
                                        <span className={`badge ${enquiry.status}`}>
                                            {enquiry.status}
                                        </span>
                                    </td>
                                    <td>
                                        <button
                                            className="action-link"
                                            onClick={() => {
                                                setSelectedEnquiry(enquiry);
                                                setAdminNotes(enquiry.admin_notes || '');
                                            }}
                                        >
                                            View/Edit
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}
            </div>

            {selectedEnquiry && (
                <div className="modal-overlay">
                    <div className="modal-content">
                        <h4>Enquiry Details</h4>
                        <div className="detail-item">
                            <label>Query:</label>
                            <p>"{selectedEnquiry.query_text}"</p>
                        </div>
                        <div className="detail-item">
                            <label>Visitor:</label>
                            <p>{selectedEnquiry.visitor_name} ({selectedEnquiry.visitor_contact})</p>
                        </div>
                        <div className="detail-item">
                            <label>Admin Notes:</label>
                            <textarea
                                value={adminNotes}
                                onChange={(e) => setAdminNotes(e.target.value)}
                                placeholder="Add notes here..."
                            />
                        </div>
                        <div className="modal-actions">
                            <button
                                className="deploy-btn resolve"
                                onClick={() => handleUpdateEnquiry('resolved')}
                                disabled={updating}
                            >
                                Mark Resolved
                            </button>
                            <button
                                className="deploy-btn secondary"
                                onClick={() => handleUpdateEnquiry('pending')}
                                disabled={updating}
                            >
                                Save as Pending
                            </button>
                            <button
                                className="cancel-btn"
                                onClick={() => setSelectedEnquiry(null)}
                            >
                                Close
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default EnquiryInbox;
