/**
 * MESSAGES HANDLERS MODULE
 * Handles user interactions and event listeners
 * 
 * Features:
 * - Message sending
 * - Conversation selection
 * - Modal management
 * - Real-time polling
 * - Search functionality
 */

let currentConversationId = null;
let currentUserId = null;
let pollInterval = null;
let typingTimeout = null;

/**
 * Initialize the messaging interface
 */
async function initializeMessaging() {
    try {
        // Get current user ID from the page
        currentUserId = parseInt(document.querySelector('[data-user-id]')?.dataset.userId || '0');
        
        if (!currentUserId) {
            MessagesUI.showNotification('User not authenticated', 'error');
            return;
        }

        // Load initial conversations
        await loadConversations();

        // Set up event listeners
        setupEventListeners();

        // Start polling for new messages
        startPolling();

        MessagesUI.showNotification('Messages loaded successfully', 'success', 2000);
    } catch (error) {
        MessagesUI.showNotification('Failed to initialize messaging: ' + error.message, 'error');
        console.error('Initialization error:', error);
    }
}

/**
 * Set up event listeners
 */
function setupEventListeners() {
    // Message input listeners
    const messageInput = document.getElementById('messageInput');
    if (messageInput) {
        // Send on Enter (but Shift+Enter for newline)
        messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        // Typing indicator
        messageInput.addEventListener('input', () => {
            if (currentConversationId) {
                MessagesAPI.setTypingStatus(currentConversationId, true);
                
                clearTimeout(typingTimeout);
                typingTimeout = setTimeout(() => {
                    MessagesAPI.setTypingStatus(currentConversationId, false);
                }, 3000);
            }
        });
    }

    // Search input
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            const query = e.target.value.trim();
            
            if (query.length > 2) {
                searchTimeout = setTimeout(() => {
                    performSearch(query);
                }, 300);
            }
        });

        searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                searchInput.value = '';
                searchInput.blur();
            }
        });
    }

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + K for search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            document.getElementById('searchInput')?.focus();
        }

        // Ctrl/Cmd + N for new message
        if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
            e.preventDefault();
            showNewMessageModal();
        }

        // Escape to close modals
        if (e.key === 'Escape') {
            closeAllModals();
        }
    });

    // Close menus when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('#settingsMenu') && !e.target.closest('[onclick*="toggleSettings"]')) {
            document.getElementById('settingsMenu')?.classList.add('hidden');
        }
    });
}

/**
 * Load all conversations
 */
async function loadConversations() {
    try {
        const response = await MessagesAPI.getConversations(1, 50);
        const conversations = response.results || response.conversations || [];
        MessagesUI.renderConversations(conversations);
    } catch (error) {
        MessagesUI.showNotification('Failed to load conversations', 'error');
        console.error('Load conversations error:', error);
    }
}

/**
 * Select a conversation
 */
async function selectConversation(conversationId) {
    try {
        currentConversationId = conversationId;

        // Update UI
        document.querySelectorAll('.conversation-card').forEach(card => {
            card.classList.remove('active');
        });
        event.currentTarget?.classList.add('active');

        // Hide sidebar on mobile
        const sidebar = document.getElementById('conversationsSidebar');
        if (sidebar && window.innerWidth < 640) {
            sidebar.classList.remove('active');
        }

        // Load messages
        await loadMessages(conversationId);

        // Mark as read
        await MessagesAPI.markConversationAsRead(conversationId);
    } catch (error) {
        MessagesUI.showNotification('Failed to load conversation', 'error');
        console.error('Select conversation error:', error);
    }
}

/**
 * Load messages for a conversation
 */
async function loadMessages(conversationId) {
    try {
        const response = await MessagesAPI.getMessages(conversationId, 1, 50);
        const messages = response.results || response.messages || [];
        
        MessagesUI.renderMessages(messages, currentUserId);

        // TODO: Update chat header with conversation info
        // MessagesUI.updateChatHeader(conversation);
    } catch (error) {
        MessagesUI.showNotification('Failed to load messages', 'error');
        console.error('Load messages error:', error);
    }
}

/**
 * Send a message
 */
async function sendMessage() {
    const input = document.getElementById('messageInput');
    const content = input.value.trim();

    if (!content) {
        MessagesUI.showNotification('Message cannot be empty', 'warning');
        return;
    }

    if (!currentConversationId) {
        MessagesUI.showNotification('Please select a conversation first', 'warning');
        return;
    }

    try {
        input.disabled = true;
        const response = await MessagesAPI.sendMessage(content, conversationId = currentConversationId);
        
        // Add message to UI
        MessagesUI.addMessage(response, currentUserId, 'bottom');

        // Clear input
        input.value = '';
        input.focus();

        // Hide typing indicator
        MessagesUI.hideTypingIndicator();
    } catch (error) {
        MessagesUI.showNotification('Failed to send message: ' + error.message, 'error');
        console.error('Send message error:', error);
    } finally {
        input.disabled = false;
    }
}

/**
 * Perform search
 */
async function performSearch(query) {
    try {
        const response = await MessagesAPI.searchMessages(query, currentConversationId);
        const results = response.results || [];

        if (results.length === 0) {
            MessagesUI.showNotification('No messages found', 'info', 2000);
            return;
        }

        // Show search results modal
        showSearchResultsModal(results, query);
    } catch (error) {
        MessagesUI.showNotification('Search failed: ' + error.message, 'error');
        console.error('Search error:', error);
    }
}

/**
 * Show search results in modal
 */
function showSearchResultsModal(results, query) {
    const content = `
        <div class="space-y-3">
            ${results.length > 0 ? results.map(result => `
                <div class="p-3 bg-gray-700 rounded-lg hover:bg-gray-600 transition cursor-pointer" onclick="selectConversation(${result.conversation_id})">
                    <div class="flex items-start gap-3">
                        <div class="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white text-xs font-bold flex-shrink-0">
                            ${result.sender_name.charAt(0).toUpperCase()}
                        </div>
                        <div class="flex-1 min-w-0">
                            <div class="font-medium text-white">${result.sender_name}</div>
                            <div class="text-sm text-gray-300 truncate">${result.content}</div>
                            <div class="text-xs text-gray-400 mt-1">${MessagesUI.formatTime(result.created_at)}</div>
                        </div>
                    </div>
                </div>
            `).join('') : `
                <div class="text-center py-8 text-gray-400">
                    <p>No messages found for "${query}"</p>
                </div>
            `}
        </div>
    `;

    MessagesUI.showModal('Search Results', content, [
        { label: 'Close', onclick: 'this.closest(".modal-overlay").remove()', type: 'secondary' }
    ]);
}

/**
 * Show new message modal
 */
async function showNewMessageModal() {
    try {
        const connections = await MessagesAPI.getConnections();
        const options = connections.map(conn => `
            <option value="${conn.id}">${conn.full_name || conn.username}</option>
        `).join('');

        const content = `
            <div class="modal-form">
                <div class="form-group">
                    <label>Select recipient</label>
                    <select id="recipientSelect" class="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <option value="">Choose a connection...</option>
                        ${options}
                    </select>
                </div>
                <div class="form-group">
                    <label>Message</label>
                    <textarea id="newMessageContent" placeholder="Type your message..." rows="4" class="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"></textarea>
                </div>
            </div>
        `;

        MessagesUI.showModal('New Message', content, [
            { label: 'Cancel', onclick: 'this.closest(".modal-overlay").remove()', type: 'secondary' },
            { label: 'Send', onclick: 'sendDirectMessage()', type: 'primary' }
        ]);

        // Focus on textarea
        setTimeout(() => {
            document.getElementById('newMessageContent')?.focus();
        }, 100);
    } catch (error) {
        MessagesUI.showNotification('Failed to load recipients', 'error');
        console.error('New message modal error:', error);
    }
}

/**
 * Send direct message from modal
 */
async function sendDirectMessage() {
    const recipientId = document.getElementById('recipientSelect')?.value;
    const content = document.getElementById('newMessageContent')?.value.trim();

    if (!recipientId) {
        MessagesUI.showNotification('Please select a recipient', 'warning');
        return;
    }

    if (!content) {
        MessagesUI.showNotification('Message cannot be empty', 'warning');
        return;
    }

    try {
        await MessagesAPI.sendMessage(content, recipientId);
        MessagesUI.showNotification('Message sent!', 'success', 2000);
        closeAllModals();
        await loadConversations();
    } catch (error) {
        MessagesUI.showNotification('Failed to send message', 'error');
        console.error('Send direct message error:', error);
    }
}

/**
 * Show group chat modal
 */
async function showGroupChatModal() {
    try {
        const connections = await MessagesAPI.getConnections();
        const options = connections.map(conn => `
            <label class="flex items-center gap-2">
                <input type="checkbox" value="${conn.id}" class="member-checkbox">
                <span>${conn.full_name || conn.username}</span>
            </label>
        `).join('');

        const content = `
            <div class="modal-form">
                <div class="form-group">
                    <label>Group name</label>
                    <input type="text" id="groupName" placeholder="e.g., Project Team" class="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500">
                </div>
                <div class="form-group">
                    <label>Select members</label>
                    <div class="space-y-2 max-h-40 overflow-y-auto">
                        ${options}
                    </div>
                </div>
            </div>
        `;

        MessagesUI.showModal('Create Group Chat', content, [
            { label: 'Cancel', onclick: 'this.closest(".modal-overlay").remove()', type: 'secondary' },
            { label: 'Create', onclick: 'createGroupChat()', type: 'primary' }
        ]);
    } catch (error) {
        MessagesUI.showNotification('Failed to load members', 'error');
        console.error('Group chat modal error:', error);
    }
}

/**
 * Create group chat
 */
async function createGroupChat() {
    const name = document.getElementById('groupName')?.value.trim();
    const selectedMembers = Array.from(document.querySelectorAll('.member-checkbox:checked')).map(cb => parseInt(cb.value));

    if (!name) {
        MessagesUI.showNotification('Please enter a group name', 'warning');
        return;
    }

    if (selectedMembers.length === 0) {
        MessagesUI.showNotification('Please select at least one member', 'warning');
        return;
    }

    try {
        await MessagesAPI.createChatRoom(name, selectedMembers);
        MessagesUI.showNotification('Group chat created!', 'success', 2000);
        closeAllModals();
        await loadConversations();
    } catch (error) {
        MessagesUI.showNotification('Failed to create group chat', 'error');
        console.error('Create group chat error:', error);
    }
}

/**
 * Toggle settings menu
 */
function toggleSettingsMenu() {
    const menu = document.getElementById('settingsMenu');
    menu?.classList.toggle('hidden');
}

/**
 * Toggle dark mode
 */
function toggleDarkMode() {
    const html = document.documentElement;
    const isDark = html.classList.contains('dark');
    
    if (isDark) {
        html.classList.remove('dark');
        localStorage.setItem('theme', 'light');
    } else {
        html.classList.add('dark');
        localStorage.setItem('theme', 'dark');
    }
    
    MessagesUI.showNotification(isDark ? 'Switched to light mode' : 'Switched to dark mode', 'info', 2000);
    toggleSettingsMenu();
}

/**
 * Toggle notifications
 */
function toggleNotifications() {
    MessagesUI.showNotification('Notification preferences updated', 'success', 2000);
    toggleSettingsMenu();
}

/**
 * Show keyboard shortcuts
 */
function showKeyboardShortcuts() {
    const content = `
        <div class="space-y-4">
            <div>
                <h4 class="font-medium text-white mb-3">Navigation</h4>
                <div class="space-y-2 text-sm">
                    <div class="flex justify-between">
                        <span class="text-gray-300">Search messages</span>
                        <kbd class="px-2 py-1 bg-gray-700 rounded">Ctrl + K</kbd>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-300">New message</span>
                        <kbd class="px-2 py-1 bg-gray-700 rounded">Ctrl + N</kbd>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-300">Close modals</span>
                        <kbd class="px-2 py-1 bg-gray-700 rounded">Esc</kbd>
                    </div>
                </div>
            </div>
            <div>
                <h4 class="font-medium text-white mb-3">Message Input</h4>
                <div class="space-y-2 text-sm">
                    <div class="flex justify-between">
                        <span class="text-gray-300">Send message</span>
                        <kbd class="px-2 py-1 bg-gray-700 rounded">Enter</kbd>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-300">New line</span>
                        <kbd class="px-2 py-1 bg-gray-700 rounded">Shift + Enter</kbd>
                    </div>
                </div>
            </div>
        </div>
    `;

    MessagesUI.showModal('Keyboard Shortcuts', content, [
        { label: 'Close', onclick: 'this.closest(".modal-overlay").remove()', type: 'secondary' }
    ]);
    toggleSettingsMenu();
}

/**
 * Attach file
 */
function attachFile() {
    const input = document.createElement('input');
    input.type = 'file';
    input.multiple = true;
    input.onchange = async (e) => {
        const files = Array.from(e.target.files);
        // TODO: Implement file upload
        MessagesUI.showNotification('File upload coming soon', 'info');
    };
    input.click();
}

/**
 * Show message actions menu
 */
function showMessageActions(messageId) {
    // TODO: Implement message actions (edit, delete, react)
    console.log('Show actions for message:', messageId);
}

/**
 * Toggle search
 */
function toggleSearch() {
    const searchInput = document.getElementById('searchInput');
    searchInput?.focus();
}

/**
 * Toggle mobile menu
 */
function toggleMobileMenu() {
    const sidebar = document.getElementById('conversationsSidebar');
    sidebar?.classList.toggle('active');
}

/**
 * Close all modals
 */
function closeAllModals() {
    document.querySelectorAll('.modal-overlay').forEach(modal => modal.remove());
}

/**
 * Start polling for new messages
 */
function startPolling() {
    pollInterval = setInterval(async () => {
        if (currentConversationId) {
            try {
                await loadMessages(currentConversationId);
            } catch (error) {
                console.error('Polling error:', error);
            }
        }
    }, 5000); // Poll every 5 seconds
}

/**
 * Stop polling
 */
function stopPolling() {
    if (pollInterval) {
        clearInterval(pollInterval);
        pollInterval = null;
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', initializeMessaging);

// Clean up on page unload
window.addEventListener('beforeunload', () => {
    stopPolling();
    MessagesAPI.setTypingStatus(currentConversationId, false);
});
