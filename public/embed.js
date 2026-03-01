(function () {
    // 1. UPDATE THIS: For local testing, use http://localhost:5173 
    // For netlify, keep it as faqsense.netlify.app
    const frontendBaseUrl = 'https://faqsense.netlify.app';

    const scriptUrl = `${frontendBaseUrl}/embed.js`;
    const appUrl = `${frontendBaseUrl}/?mode=widget`;

    console.log("[FAQSense] Initializing with App URL:", appUrl);

    function init() {
        const container = document.getElementById('faqsense-chatbot');
        if (!container) {
            console.error("[FAQSense] Container #faqsense-chatbot not found on this page!");
            return;
        }

        const currentScript = document.currentScript || document.querySelector('script[src*="embed.js"]');
        const botId = currentScript ? (currentScript.getAttribute('data-id') || '1') : '1';

        console.log("[FAQSense] Loading Bot ID:", botId);

        const iframe = document.createElement('iframe');
        iframe.src = `${appUrl}&id=${botId}`;

        // Premium styling
        iframe.style.position = 'fixed';
        iframe.style.bottom = '20px';
        iframe.style.right = '20px';
        iframe.style.width = '420px';
        iframe.style.height = '600px';
        iframe.style.border = 'none';
        iframe.style.zIndex = '999999';
        iframe.style.backgroundColor = 'transparent';

        // Ensure browser allows cross-document rendering
        iframe.setAttribute('allow', 'cross-origin-isolated');

        container.appendChild(iframe);
    }

    if (document.readyState === 'complete') {
        init();
    } else {
        window.addEventListener('load', init);
    }
})();
