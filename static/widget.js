(function () {
    // 1. Get configuration from script tag
    const script = document.currentScript;
    const botId = script.getAttribute('data-bot-id') || '1';
    const baseUrl = 'http://localhost:5173'; // Your frontend URL

    // 2. Create styles for the bubble and iframe
    const style = document.createElement('style');
    style.innerHTML = `
        #faqsense-bubble {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, #6366f1, #a855f7);
            box-shadow: 0 4px 12px rgba(99,102,241,0.4);
            cursor: pointer;
            z-index: 999998;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        #faqsense-bubble:hover { transform: scale(1.1); }
        #faqsense-bubble svg { width: 30px; height: 30px; fill: white; }

        #faqsense-container {
            position: fixed;
            bottom: 90px;
            right: 20px;
            width: 380px;
            height: 600px;
            max-height: 80vh;
            background: white;
            border-radius: 16px;
            box-shadow: 0 12px 24px rgba(0,0,0,0.15);
            z-index: 999999;
            display: none;
            overflow: hidden;
            border: 1px solid #e2e8f0;
        }
        #faqsense-container.open { display: block; }

        #faqsense-iframe {
            width: 100%;
            height: 100%;
            border: none;
        }
    `;
    document.head.appendChild(style);

    // 3. Create bubble
    const bubble = document.createElement('div');
    bubble.id = 'faqsense-bubble';
    bubble.innerHTML = `<svg viewBox="0 0 24 24"><path d="M20,2H4C2.9,2,2,2.9,2,4v18l4-4h14c1.1,0,2-0.9,2-2V4C22,2.9,21.1,2,20,2z"/></svg>`;
    document.body.appendChild(bubble);

    // 4. Create container/iframe
    const container = document.createElement('div');
    container.id = 'faqsense-container';
    container.innerHTML = `<iframe id="faqsense-iframe" src="${baseUrl}/?mode=widget&id=${botId}"></iframe>`;
    document.body.appendChild(container);

    // 5. Toggle logic
    let isOpen = false;
    bubble.onclick = function () {
        isOpen = !isOpen;
        if (isOpen) {
            container.classList.add('open');
        } else {
            container.classList.remove('open');
        }
    };
})();
