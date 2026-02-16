/**
 * MESSAGES UI MODULE
 * Handles all UI rendering and DOM manipulation
 * 
 * Features:
 * - Rendering conversations list
 * - Rendering message bubbles
 * - Modal management
 * - Notification display
 * - Real-time updates
 */

const MessagesUI = {
    /**
     * Render conversation list
     */
    renderConversations(conversations) {
        const container = document.getElementById('conversationList');
        
        if (!conversations || conversations.length === 0) {
            container.innerHTML = `
                <div class="p-8 text-center text-gray-400">
                    <i data-lucide="inbox" class="w-12 h-12 mx-auto mb-3 opacity-50"></i>
                    <p>No conversations yet</p>
                    <p class="text-sm mt-2">Start a new message to begin chatting</p>
                </div>
            `;
            lucide.createIcons();
            return;
        }

        container.innerHTML = conversations.map(conv => `
            <div class="conversation-card ${conv.is_active ? 'active' : ''} ${conv.unread_count > 0 ? 'unread' : ''}" 
                 onclick="selectConversation(${conv.id})">
                <div class="flex gap-3 relative">
                    <div class="avatar-glow">
                        ${conv.avatar_url ? `<img src="${conv.avatar_url}" alt="${conv.name}" class="w-full h-full rounded-full object-cover">` : conv.name.charAt(0).toUpperCase()}
                    </div>
                    ${conv.is_online ? '<div class="online-indicator"></div>' : ''}
                    
                    <div class="flex-1 min-w-0">
                        <div class="flex items-center justify-between gap-2">
                            <h3 class="font-semibold text-white truncate">${conv.name}</h3>
                            <span class="text-xs text-gray-400 flex-shrink-0">${this.formatTime(conv.last_message_time)}</span>
                        </div>
                        
                        <p class="text-sm text-gray-400 truncate">
                            ${conv.last_message_preview || 'No messages yet'}
                        </p>
                        
                        <div class="flex items-center justify-between mt-2">
                            <span class="text-xs text-gray-500">${conv.is_online ? 'Online' : 'Offline'}</span>
                            ${conv.unread_count > 0 ? `<span class="unread-badge">${conv.unread_count}</span>` : ''}
                        </div>
                    </div>
                </div>
            </div>
        `).join('');

        lucide.createIcons();
    },

    /**
     * Render messages in chat window
     */
    renderMessages(messages, userId) {
        const container = document.getElementById('messagesContainer');
        
        if (!messages || messages.length === 0) {
            container.innerHTML = `
                <div class="flex items-center justify-center h-full text-gray-400">
                    <div class="text-center">
                        <i data-lucide="message-circle" class="w-12 h-12 mx-auto mb-3 opacity-50"></i>
                        <p>No messages in this conversation</p>
                        <p class="text-sm mt-2">Start the conversation by sending a message</p>
                    </div>
                </div>
            `;
            return;
        }

        container.innerHTML = messages.map((msg, index) => {
            const isOwn = msg.sender_id === userId;
            const showAvatar = index === 0 || messages[index - 1].sender_id !== msg.sender_id;
            
            return `
                <div class="message-bubble ${isOwn ? 'own' : 'other'}" data-message-id="${msg.id}">
                    ${!isOwn && showAvatar ? `
                        <div class="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white text-xs font-bold flex-shrink-0">
                            ${msg.sender_name.charAt(0).toUpperCase()}
                        </div>
                    ` : '<div class="w-8"></div>'}
                    
                    <div class="flex flex-col ${isOwn ? 'items-end' : 'items-start'}">
                        ${!isOwn && msg.sender_name ? `
                            <span class="text-xs text-gray-400 px-2">${msg.sender_name}</span>
                        ` : ''}
                        
                        <div class="flex gap-1 items-end">
                            <div class="message-content">
                                ${msg.content}
                            </div>
                            
                            <div class="message-actions">
                                <button onclick="showMessageActions(${msg.id})" title="Options">⋮</button>
                            </div>
                        </div>
                        
                        <div class="message-time">
                            ${this.formatTime(msg.created_at)}
                            ${isOwn ? `
                                <span class="message-status">
                                    ${msg.is_read ? '<span class="check">✓✓</span>' : '<span>✓</span>'}
                                </span>
                            ` : ''}
                        </div>
                        
                        ${msg.reactions && msg.reactions.length > 0 ? `
                            <div class="flex gap-1 mt-2 text-sm">
                                ${msg.reactions.map(r => `<span title="${r.users.join(', ')}">${r.emoji}</span>`).join('')}
                            </div>
                        ` : ''}
                    </div>
                </div>
            `;
        }).join('');

        // Scroll to bottom
        setTimeout(() => {
            container.scrollTop = container.scrollHeight;
        }, 100);

        lucide.createIcons();
    },

    /**
     * Update chat header with conversation info
     */
    updateChatHeader(conversation) {
        const headerContent = document.getElementById('chatHeaderContent');
        const nameEl = document.getElementById('chatName');
        const statusEl = document.getElementById('chatStatus');

        headerContent.innerHTML = `
            <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold relative">
                ${conversation.avatar_url ? `<img src="${conversation.avatar_url}" alt="${conversation.name}" class="w-full h-full rounded-full object-cover">` : conversation.name.charAt(0).toUpperCase()}
                ${conversation.is_online ? '<div class="online-indicator absolute bottom-0 right-0"></div>' : ''}
            </div>
            <div>
                <h3 id="chatName" class="font-semibold text-white">${conversation.name}</h3>
                <p id="chatStatus" class="text-xs ${conversation.is_online ? 'text-green-500' : 'text-gray-400'}">
                    ${conversation.is_online ? 'Online' : conversation.last_seen ? `Last seen ${this.formatTime(conversation.last_seen)}` : 'Offline'}
                </p>
            </div>
        `;

        lucide.createIcons();
    },

    /**
     * Add a single message to the chat
     */
    addMessage(message, userId, position = 'bottom') {
        const container = document.getElementById('messagesContainer');
        const isOwn = message.sender_id === userId;

        if (container.querySelector('[data-message-id]') === null) {
            // Clear empty state
            container.innerHTML = '';
        }

        const messageHtml = `
            <div class="message-bubble ${isOwn ? 'own' : 'other'}" data-message-id="${message.id}">
                <div class="w-8"></div>
                <div class="flex flex-col ${isOwn ? 'items-end' : 'items-start'}">
                    <div class="flex gap-1 items-end">
                        <div class="message-content">
                            ${message.content}
                        </div>
                        <div class="message-actions">
                            <button onclick="showMessageActions(${message.id})" title="Options">⋮</button>
                        </div>
                    </div>
                    <div class="message-time">
                        ${this.formatTime(message.created_at)}
                        ${isOwn ? '<span class="message-status"><span>✓</span></span>' : ''}
                    </div>
                </div>
            </div>
        `;

        if (position === 'bottom') {
            container.insertAdjacentHTML('beforeend', messageHtml);
            container.scrollTop = container.scrollHeight;
        } else {
            container.insertAdjacentHTML('afterbegin', messageHtml);
        }

        lucide.createIcons();
    },

    /**
     * Show typing indicator
     */
    showTypingIndicator(name) {
        const indicator = document.getElementById('typingIndicator');
        if (indicator) {
            indicator.textContent = `${name} is typing...`;
            indicator.classList.remove('hidden');
        }
    },

    /**
     * Hide typing indicator
     */
    hideTypingIndicator() {
        const indicator = document.getElementById('typingIndicator');
        if (indicator) {
            indicator.classList.add('hidden');
        }
    },

    /**
     * Format timestamp for display
     */
    formatTime(timestamp) {
        if (!timestamp) return '';
        
        const date = new Date(timestamp);
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMs / 3600000);
        const diffDays = Math.floor(diffMs / 86400000);

        if (diffMins < 1) return 'just now';
        if (diffMins < 60) return `${diffMins}m ago`;
        if (diffHours < 24) return `${diffHours}h ago`;
        if (diffDays < 7) return `${diffDays}d ago`;
        
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    },

    /**
     * Show notification toast
     */
    showNotification(message, type = 'info', duration = 4000) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        
        const icons = {
            success: '✓',
            error: '✕',
            info: 'ℹ',
            warning: '⚠'
        };

        notification.innerHTML = `
            <span class="text-xl">${icons[type]}</span>
            <span class="flex-1">${message}</span>
            <button class="notification-close" onclick="this.parentElement.remove()">✕</button>
        `;

        document.body.appendChild(notification);

        if (duration > 0) {
            setTimeout(() => {
                notification.remove();
            }, duration);
        }
    },

    /**
     * Show modal dialog
     */
    showModal(title, content, actions = []) {
        const modal = document.createElement('div');
        modal.className = 'modal-overlay';
        
        const modalContent = document.createElement('div');
        modalContent.className = 'modal-content';
        
        modalContent.innerHTML = `
            <div class="modal-header">
                <h3>${title}</h3>
                <button class="modal-close" onclick="this.closest('.modal-overlay').remove()">
                    <i data-lucide="x" class="w-5 h-5"></i>
                </button>
            </div>
            <div class="modal-body">
                ${content}
            </div>
            ${actions.length > 0 ? `
                <div class="form-actions">
                    ${actions.map(action => `
                        <button class="btn-${action.type || 'primary'}" onclick="${action.onclick}">
                            ${action.label}
                        </button>
                    `).join('')}
                </div>
            ` : ''}
        `;

        modal.appendChild(modalContent);
        document.body.appendChild(modal);

        // Close on overlay click
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });

        lucide.createIcons();
        return modal;
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MessagesUI;
}
