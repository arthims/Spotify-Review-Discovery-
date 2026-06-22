const chatFeed = document.getElementById('chatFeed');
const queryInput = document.getElementById('queryInput');
const chatForm = document.getElementById('chatForm');
const sendBtn = document.getElementById('sendBtn');
const typingIndicator = document.getElementById('typingIndicator');

// Initialize scroll
scrollToBottom();

function runExample(query) {
    queryInput.value = query;
    chatForm.dispatchEvent(new Event('submit'));
}

async function handleSend(e) {
    e.preventDefault();
    
    const queryText = queryInput.value.trim();
    if (!queryText) return;
    
    // Clear input and disable input elements during submit
    queryInput.value = '';
    setInputState(false);
    
    // Append User Message
    appendMessage(queryText, 'user');
    scrollToBottom();
    
    // Show typing loader
    showLoader(true);
    scrollToBottom();
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: queryText })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Hide loader
        showLoader(false);
        
        // Append Bot Response
        appendBotResponse(data);
        
    } catch (err) {
        console.error("API error:", err);
        showLoader(false);
        appendMessage("Sorry, I encountered an issue connecting to the backend server. Please verify the FastAPI service is running locally on port 8000.", 'bot', 'warning');
    } finally {
        setInputState(true);
        queryInput.focus();
        scrollToBottom();
    }
}

function setInputState(enabled) {
    queryInput.disabled = !enabled;
    sendBtn.disabled = !enabled;
}

function showLoader(show) {
    typingIndicator.style.display = show ? 'flex' : 'none';
}

function scrollToBottom() {
    chatFeed.scrollTop = chatFeed.scrollHeight;
}

function appendMessage(text, sender, type = 'normal') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = `message-bubble ${sender}-bubble`;
    
    if (type === 'refused') {
        bubbleDiv.classList.add('refused-bubble');
    } else if (type === 'warning') {
        bubbleDiv.classList.add('warning-bubble');
    }
    
    bubbleDiv.textContent = text;
    messageDiv.appendChild(bubbleDiv);
    chatFeed.appendChild(messageDiv);
    return messageDiv;
}

function appendBotResponse(data) {
    const sender = 'bot';
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = `message-bubble ${sender}-bubble`;
    
    // Add special styling classes depending on the response status
    if (data.status === 'refused') {
        bubbleDiv.classList.add('refused-bubble');
    } else if (data.status === 'warning') {
        bubbleDiv.classList.add('warning-bubble');
    }
    
    // Add core text
    const textNode = document.createElement('p');
    textNode.textContent = data.response;
    bubbleDiv.appendChild(textNode);
    
    // Add citation if provided (crucial requirement: do not attach if unknown)
    if (data.source_url) {
        const citationDiv = document.createElement('div');
        citationDiv.className = 'citation-card';
        
        const iconSpan = document.createElement('span');
        iconSpan.textContent = '🌐';
        citationDiv.appendChild(iconSpan);
        
        const link = document.createElement('a');
        link.className = 'citation-link';
        link.href = data.source_url;
        link.target = '_blank';
        
        // Show domain or friendly URL text
        let displayUrl = 'Official Source';
        try {
            const urlObj = new URL(data.source_url);
            displayUrl = urlObj.hostname + (urlObj.pathname.length > 1 ? urlObj.pathname.slice(0, 15) + '...' : '');
        } catch(e) {}
        
        link.textContent = displayUrl;
        citationDiv.appendChild(link);
        bubbleDiv.appendChild(citationDiv);
    }
    
    // Add footer if provided (mandatory "Last updated from sources" date or custom disclaimers)
    if (data.footer) {
        const footerSpan = document.createElement('span');
        footerSpan.className = 'bot-footer';
        footerSpan.textContent = data.footer;
        bubbleDiv.appendChild(footerSpan);
    }
    
    messageDiv.appendChild(bubbleDiv);
    chatFeed.appendChild(messageDiv);
}
