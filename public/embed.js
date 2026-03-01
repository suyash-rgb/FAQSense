(function () {
    // 1. UPDATE THIS: Use your FRONTEND URL (e.g., https://faqsense.netlify.app)
    // DO NOT use the onrender.com Backend URL here.
    const frontendBaseUrl = 'https://faqsense.netlify.app';

    const scriptUrl = `${frontendBaseUrl}/embed.js`;
    const appUrl = `${frontendBaseUrl}/?mode=widget`;

    function init() {
        const container = document.getElementById('faqsense-chatbot');
        if (!container) return;

        // 2. Extract chatbotId from the script tag's data-id attribute (e.g., data-id="5")
        const currentScript = document.currentScript || document.querySelector('script[src*="embed.js"]');
        const botId = currentScript ? (currentScript.getAttribute('data-id') || '1') : '1';

        const iframe = document.createElement('iframe');
        // 3. Pass the bot ID to the React app via URL params
        iframe.src = `${appUrl}&id=${botId}`;

        iframe.style.position = 'fixed';
        iframe.style.bottom = '20px';
        iframe.style.right = '20px';
        iframe.style.width = '420px';
        iframe.style.height = '600px';
        iframe.style.border = 'none';
        iframe.style.zIndex = '999999';
        iframe.style.backgroundColor = 'transparent';
        iframe.setAttribute('allowtransparency', 'true');

        container.appendChild(iframe);
    }

    if (document.readyState === 'complete') {
        init();
    } else {
        window.addEventListener('load', init);
    }
})();
