(function () {
    const scriptUrl = 'http://localhost:5173/embed.js'; // Adjust for production
    const appUrl = 'http://localhost:5173?mode=widget';

    function init() {
        const container = document.getElementById('faqsense-chatbot');
        if (!container) return;

        // Create iframe to isolate styles and React environment
        const iframe = document.createElement('iframe');
        iframe.src = appUrl;
        iframe.style.position = 'fixed';
        iframe.style.bottom = '0';
        iframe.style.right = '0';
        iframe.style.width = '420px'; // Wide enough for the open window
        iframe.style.height = '600px';
        iframe.style.border = 'none';
        iframe.style.zIndex = '999999';
        iframe.style.backgroundColor = 'transparent';
        iframe.setAttribute('allowtransparency', 'true');

        container.appendChild(iframe);

        // Optional: communication between iframe and parent
        window.addEventListener('message', (event) => {
            if (event.origin !== new URL(appUrl).origin) return;
            // Handle events from the chatbot if needed
        });
    }

    if (document.readyState === 'complete') {
        init();
    } else {
        window.addEventListener('load', init);
    }
})();
