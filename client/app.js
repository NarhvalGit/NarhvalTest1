/**
 * OpenAI Chat Client - JavaScript
 *
 * Beheert de communicatie tussen de browser en de Flask server
 */

// Configuratie
const API_URL = 'http://localhost:5000';
const CHAT_ENDPOINT = `${API_URL}/api/chat`;
const STATUS_ENDPOINT = `${API_URL}/`;

// State
let isProcessing = false;

/**
 * Initialisatie bij laden van de pagina
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Chat client geïnitialiseerd');

    // Check server status
    checkServerStatus();

    // Enable Enter key to send (Shift+Enter for new line)
    const promptInput = document.getElementById('prompt-input');
    promptInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendPrompt();
        }
    });

    // Focus on input field
    promptInput.focus();
});

/**
 * Controleer of de server online is
 */
async function checkServerStatus() {
    try {
        const response = await fetch(STATUS_ENDPOINT, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const data = await response.json();
            updateStatus(true, 'Verbonden met server');
            console.log('✓ Server status:', data);

            if (!data.agent_initialized) {
                updateStatus(false, 'Server online maar OpenAI agent niet geïnitialiseerd');
                addSystemMessage('⚠️ Waarschuwing: OpenAI Agent niet geïnitialiseerd. Controleer OPENAI_API_KEY op de server.');
            }
        } else {
            updateStatus(false, 'Server antwoordt met error');
        }
    } catch (error) {
        updateStatus(false, 'Kan geen verbinding maken met server');
        console.error('✗ Server status check failed:', error);
    }
}

/**
 * Update status indicator
 */
function updateStatus(connected, message) {
    const statusIndicator = document.getElementById('status-indicator');
    const statusText = document.getElementById('status-text');

    if (connected) {
        statusIndicator.classList.add('connected');
        statusIndicator.classList.remove('disconnected');
    } else {
        statusIndicator.classList.add('disconnected');
        statusIndicator.classList.remove('connected');
    }

    statusText.textContent = message;
}

/**
 * Voeg een systeem bericht toe aan de chat
 */
function addSystemMessage(message) {
    const chatContainer = document.getElementById('chat-container');
    const welcomeMessage = chatContainer.querySelector('.welcome-message');

    if (welcomeMessage) {
        welcomeMessage.remove();
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = 'message error-message';
    messageDiv.innerHTML = `
        <div class="message-content">${escapeHtml(message)}</div>
    `;

    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

/**
 * Voeg een gebruikers bericht toe aan de chat
 */
function addUserMessage(message) {
    const chatContainer = document.getElementById('chat-container');
    const welcomeMessage = chatContainer.querySelector('.welcome-message');

    if (welcomeMessage) {
        welcomeMessage.remove();
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    messageDiv.innerHTML = `
        <div class="message-label">Jij</div>
        <div class="message-content">${escapeHtml(message)}</div>
    `;

    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

/**
 * Voeg een AI bericht toe aan de chat
 */
function addAIMessage(message, model) {
    const chatContainer = document.getElementById('chat-container');

    const messageDiv = document.createElement('div');
    messageDiv.className = 'message ai-message';
    messageDiv.innerHTML = `
        <div class="message-label">AI (${escapeHtml(model)})</div>
        <div class="message-content">${escapeHtml(message)}</div>
    `;

    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

/**
 * Voeg een error bericht toe aan de chat
 */
function addErrorMessage(message) {
    const chatContainer = document.getElementById('chat-container');

    const messageDiv = document.createElement('div');
    messageDiv.className = 'message error-message';
    messageDiv.innerHTML = `
        <div class="message-label">Error</div>
        <div class="message-content">${escapeHtml(message)}</div>
    `;

    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

/**
 * Escape HTML om XSS te voorkomen
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Toggle loading state van de verzend button
 */
function setLoadingState(loading) {
    const sendButton = document.getElementById('send-button');
    const buttonText = document.getElementById('button-text');
    const buttonLoader = document.getElementById('button-loader');

    if (loading) {
        sendButton.disabled = true;
        buttonText.classList.add('hidden');
        buttonLoader.classList.remove('hidden');
    } else {
        sendButton.disabled = false;
        buttonText.classList.remove('hidden');
        buttonLoader.classList.add('hidden');
    }
}

/**
 * Verstuur prompt naar de server
 */
async function sendPrompt() {
    // Voorkom meerdere gelijktijdige requests
    if (isProcessing) {
        console.log('⏳ Al bezig met verwerken...');
        return;
    }

    const promptInput = document.getElementById('prompt-input');
    const modelSelect = document.getElementById('model-select');

    const prompt = promptInput.value.trim();
    const model = modelSelect.value;

    // Validatie
    if (!prompt) {
        addErrorMessage('Voer eerst een prompt in!');
        return;
    }

    // Set state
    isProcessing = true;
    setLoadingState(true);

    // Voeg gebruikers bericht toe
    addUserMessage(prompt);

    // Clear input
    promptInput.value = '';

    console.log('📤 Versturen prompt naar server...');
    console.log('  Prompt:', prompt);
    console.log('  Model:', model);

    try {
        // Verstuur request naar server
        const response = await fetch(CHAT_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prompt: prompt,
                model: model
            })
        });

        console.log('📥 Response ontvangen:', response.status);

        // Parse response
        const data = await response.json();

        if (data.success) {
            // Toon AI response
            addAIMessage(data.response, data.model);
            console.log('✓ AI response toegevoegd aan chat');
        } else {
            // Toon error
            addErrorMessage(data.error || 'Onbekende fout opgetreden');
            console.error('✗ Server error:', data.error);
        }

    } catch (error) {
        console.error('✗ Fetch error:', error);
        addErrorMessage(`Verbindingsfout: ${error.message}`);
        updateStatus(false, 'Verbinding verloren');
    } finally {
        // Reset state
        isProcessing = false;
        setLoadingState(false);
        promptInput.focus();
    }
}

/**
 * Clear de chat (helper functie)
 */
function clearChat() {
    const chatContainer = document.getElementById('chat-container');
    chatContainer.innerHTML = `
        <div class="welcome-message">
            <p>👋 Chat gewist. Stel een vraag om te beginnen.</p>
        </div>
    `;
}

// Maak functies beschikbaar in global scope voor onclick handlers
window.sendPrompt = sendPrompt;
window.clearChat = clearChat;
