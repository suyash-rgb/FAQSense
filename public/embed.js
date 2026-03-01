(function () {
    // 1. Detect environment and parameters
    const currentScript = document.currentScript || document.querySelector('script[src*="embed.js"]');
    const botId = currentScript ? (currentScript.getAttribute('data-id') || '1') : '1';

    // Auto-detect base URL from where the script is hosted
    let frontendBaseUrl = 'https://faqsense.netlify.app';
    if (currentScript && currentScript.src) {
        try {
            const url = new URL(currentScript.src);
            frontendBaseUrl = url.origin;
        } catch (e) { }
    }

    const appUrl = `${frontendBaseUrl}/?mode=widget&id=${botId}`;

    console.log("[FAQSense] Initializing Chatbot Widget...", { botId, appUrl });

    // 2. Create UI Elements
    function init() {
        // Prevent double initialization
        if (document.getElementById('faqsense-bubble')) return;

        // Inject Styles
        const style = document.createElement('style');
        style.textContent = `
            #faqsense-bubble {
                position: fixed;
                bottom: 24px;
                right: 24px;
                width: 60px;
                height: 60px;
                background: linear-gradient(135deg, #6366f1, #a855f7);
                border-radius: 50%;
                box-shadow: 0 8px 16px rgba(99, 102, 241, 0.4);
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 2147483647;
                transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            }
            #faqsense-bubble:hover {
                transform: scale(1.1);
            }
            #faqsense-bubble svg {
                width: 30px;
                height: 30px;
                fill: white;
            }
            #faqsense-iframe-container {
                position: fixed;
                bottom: 100px;
                right: 24px;
                width: 420px;
                height: 600px;
                z-index: 2147483646;
                border-radius: 20px;
                overflow: hidden;
                box-shadow: 0 12px 48px rgba(0,0,0,0.18);
                display: none;
                transition: all 0.3s ease;
                opacity: 0;
                transform: translateY(20px);
            }
            #faqsense-iframe-container.open {
                display: block;
                opacity: 1;
                transform: translateY(0);
            }
            #faqsense-iframe {
                width: 100%;
                height: 100%;
                border: none;
                background: transparent;
            }
            @media (max-width: 480px) {
                #faqsense-iframe-container {
                    width: calc(100% - 32px);
                    height: calc(100% - 120px);
                    bottom: 90px;
                    right: 16px;
                }
            }
        `;
        document.head.appendChild(style);

        // Create Widget Bubble
        const bubble = document.createElement('div');
        bubble.id = 'faqsense-bubble';
        bubble.innerHTML = `<svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H5.17L4 17.17V4h16v12z"/></svg>`;
        document.body.appendChild(bubble);

        // Create Iframe Container
        const container = document.createElement('div');
        container.id = 'faqsense-iframe-container';

        const iframe = document.createElement('iframe');
        iframe.id = 'faqsense-iframe';
        iframe.src = appUrl;
        iframe.setAttribute('allow', 'cross-origin-isolated');

        container.appendChild(iframe);
        document.body.appendChild(container);

        // 3. Logic
        let isOpen = false;

        function setChatState(open) {
            isOpen = open;
            if (isOpen) {
                container.classList.add('open');
                bubble.innerHTML = `<svg viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>`;
            } else {
                container.classList.remove('open');
                bubble.innerHTML = `<svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H5.17L4 17.17V4h16v12z"/></svg>`;
            }
        }

        bubble.addEventListener('click', () => {
            setChatState(!isOpen);
        });

        // Listen for close message from iframe
        window.addEventListener('message', (event) => {
            if (event.data && event.data.type === 'faqsense-toggle') {
                setChatState(event.data.isOpen);
            }
        });
    }

    // Initialize when DOM is ready
    if (document.readyState === 'complete') {
        init();
    } else {
        window.addEventListener('load', init);
    }
})();
