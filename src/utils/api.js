import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

const getHeaders = (userId) => {
    return userId ? { 'X-User-ID': userId } : {};
};

export const getChatbots = async (userId) => {
    const response = await api.get('/chatbots/', {
        headers: getHeaders(userId)
    });
    return response.data;
};

export const createChatbot = async (userId, name) => {
    const response = await api.post('/chatbots/', { name }, {
        headers: getHeaders(userId)
    });
    return response.data;
};

export const uploadKnowledgeBase = async (userId, chatbotId, file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post(`/chatbots/${chatbotId}/upload`, formData, {
        headers: {
            ...getHeaders(userId),
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

export const getChatbotData = async (userId, chatbotId) => {
    const response = await api.get(`/chatbots/${chatbotId}/data`, {
        headers: getHeaders(userId)
    });
    return response.data;
};

export const getEnquiries = async (userId, chatbotId) => {
    const response = await api.get(`/chatbots/${chatbotId}/enquiries`, {
        headers: getHeaders(userId)
    });
    return response.data;
};

export const updateEnquiry = async (userId, chatbotId, enquiryId, data) => {
    const response = await api.patch(`/chatbots/${chatbotId}/enquiries/${enquiryId}`, data, {
        headers: getHeaders(userId)
    });
    return response.data;
};

export const getTopFaqs = async (chatbotId) => {
    const response = await api.get(`/chatbots/${chatbotId}/top-faqs`);
    return response.data;
};

export const askQuestion = async (chatbotId, query, conversationId = null) => {
    const response = await api.post(`/chatbots/${chatbotId}/ask`, {
        question: query, // Backend expects 'question' based on faq.py/chatbots.py
        conversation_id: conversationId
    });
    return response.data;
};

export const submitEnquiry = async (chatbotId, enquiryData) => {
    const response = await api.post(`/chatbots/${chatbotId}/enquiries`, enquiryData);
    return response.data;
};

// Legacy for backward compatibility
export const sendMessage = async (message) => {
    return { text: `Please use askQuestion for real interaction. You said: ${message}` };
};
