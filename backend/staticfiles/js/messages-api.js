/**
 * MESSAGES API MODULE
 * Handles all API communication for the messaging system
 * 
 * Features:
 * - Message CRUD operations
 * - Conversation management
 * - Read status tracking
 * - Search functionality
 * - Error handling with retry logic
 */

const MessagesAPI = {
    // Configuration
    baseUrl: '/api/messages',
    timeout: 10000,
    maxRetries: 3,
    
    /**
     * Get CSRF token from DOM (meta tag or cookie)
     */
    getCsrfToken() {
        // Try meta tag first (preferred)
        const meta = document.querySelector('meta[name="csrf-token"]');
        if (meta) {
            return meta.getAttribute('content');
        }

        // Fall back to cookie
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },

    /**
     * Generic fetch wrapper with error handling
     */
    async fetch(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCsrfToken(),
            ...options.headers
        };

        const fetchOptions = {
            ...options,
            headers
        };

        let lastError;
        for (let attempt = 0; attempt < this.maxRetries; attempt++) {
            try {
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), this.timeout);

                const response = await fetch(url, {
                    ...fetchOptions,
                    signal: controller.signal
                });

                clearTimeout(timeoutId);

                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }

                return await response.json();
            } catch (error) {
                lastError = error;
                if (attempt < this.maxRetries - 1) {
                    // Exponential backoff
                    await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt) * 1000));
                }
            }
        }

        throw lastError;
    },

    /**
     * Load all conversations for current user
     */
    async getConversations(page = 1, limit = 20) {
        try {
            const data = await this.fetch(`/?page=${page}&limit=${limit}`);
            return data;
        } catch (error) {
            console.error('Failed to load conversations:', error);
            throw error;
        }
    },

    /**
     * Get messages for a specific conversation
     */
    async getMessages(conversationId, page = 1, limit = 50) {
        try {
            const data = await this.fetch(`/${conversationId}/?page=${page}&limit=${limit}`);
            return data;
        } catch (error) {
            console.error('Failed to load messages:', error);
            throw error;
        }
    },

    /**
     * Send a new message
     */
    async sendMessage(content, recipientId = null, chatRoomId = null, files = []) {
        try {
            const payload = {
                content,
                ...(recipientId && { receiver_id: recipientId }),
                ...(chatRoomId && { chat_room_id: chatRoomId }),
                ...(files.length && { files })
            };

            const data = await this.fetch('/', {
                method: 'POST',
                body: JSON.stringify(payload)
            });

            return data;
        } catch (error) {
            console.error('Failed to send message:', error);
            throw error;
        }
    },

    /**
     * Mark a message as read
     */
    async markAsRead(messageId) {
        try {
            const data = await this.fetch(`/${messageId}/read/`, {
                method: 'POST'
            });
            return data;
        } catch (error) {
            console.error('Failed to mark message as read:', error);
            throw error;
        }
    },

    /**
     * Mark all messages in conversation as read
     */
    async markConversationAsRead(conversationId) {
        try {
            const data = await this.fetch(`/${conversationId}/read-all/`, {
                method: 'POST'
            });
            return data;
        } catch (error) {
            console.error('Failed to mark conversation as read:', error);
            throw error;
        }
    },

    /**
     * Search messages
     */
    async searchMessages(query, conversationId = null) {
        try {
            let endpoint = `/search/?q=${encodeURIComponent(query)}`;
            if (conversationId) {
                endpoint += `&conversation_id=${conversationId}`;
            }

            const data = await this.fetch(endpoint);
            return data;
        } catch (error) {
            console.error('Failed to search messages:', error);
            throw error;
        }
    },

    /**
     * Get chat rooms (group chats)
     */
    async getChatRooms(page = 1, limit = 20) {
        try {
            const data = await this.fetch(`/../chat-rooms/?page=${page}&limit=${limit}`);
            return data;
        } catch (error) {
            console.error('Failed to load chat rooms:', error);
            throw error;
        }
    },

    /**
     * Create a new chat room (group chat)
     */
    async createChatRoom(name, members, description = '') {
        try {
            const data = await this.fetch('/../chat-rooms/', {
                method: 'POST',
                body: JSON.stringify({
                    name,
                    members,
                    description,
                    chat_type: 'group'
                })
            });
            return data;
        } catch (error) {
            console.error('Failed to create chat room:', error);
            throw error;
        }
    },

    /**
     * Add member to chat room
     */
    async addMemberToChatRoom(chatRoomId, userId) {
        try {
            const data = await this.fetch(`/../chat-rooms/${chatRoomId}/members/`, {
                method: 'POST',
                body: JSON.stringify({
                    user_id: userId
                })
            });
            return data;
        } catch (error) {
            console.error('Failed to add member to chat room:', error);
            throw error;
        }
    },

    /**
     * Remove member from chat room
     */
    async removeMemberFromChatRoom(chatRoomId, userId) {
        try {
            const data = await this.fetch(`/../chat-rooms/${chatRoomId}/members/${userId}/`, {
                method: 'DELETE'
            });
            return data;
        } catch (error) {
            console.error('Failed to remove member from chat room:', error);
            throw error;
        }
    },

    /**
     * Delete a message
     */
    async deleteMessage(messageId) {
        try {
            const data = await this.fetch(`/${messageId}/`, {
                method: 'DELETE'
            });
            return data;
        } catch (error) {
            console.error('Failed to delete message:', error);
            throw error;
        }
    },

    /**
     * Edit a message
     */
    async editMessage(messageId, content) {
        try {
            const data = await this.fetch(`/${messageId}/`, {
                method: 'PUT',
                body: JSON.stringify({ content })
            });
            return data;
        } catch (error) {
            console.error('Failed to edit message:', error);
            throw error;
        }
    },

    /**
     * React to a message (emoji)
     */
    async addReaction(messageId, reaction) {
        try {
            const data = await this.fetch(`/${messageId}/react/`, {
                method: 'POST',
                body: JSON.stringify({ reaction })
            });
            return data;
        } catch (error) {
            console.error('Failed to add reaction:', error);
            throw error;
        }
    },

    /**
     * Get message reactions
     */
    async getReactions(messageId) {
        try {
            const data = await this.fetch(`/${messageId}/reactions/`);
            return data;
        } catch (error) {
            console.error('Failed to load reactions:', error);
            throw error;
        }
    },

    /**
     * Upload file for message
     */
    async uploadFile(file) {
        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch(`${this.baseUrl}/upload/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: formData
            });

            if (!response.ok) {
                throw new Error(`Upload failed: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Failed to upload file:', error);
            throw error;
        }
    },

    /**
     * Get user connections (for recipient selection)
     */
    async getConnections() {
        try {
            const response = await fetch('/accounts/connections/');
            if (!response.ok) {
                throw new Error('Failed to load connections');
            }
            return await response.json();
        } catch (error) {
            console.error('Failed to load connections:', error);
            throw error;
        }
    },

    /**
     * Set typing status
     */
    async setTypingStatus(conversationId, isTyping = true) {
        try {
            const data = await this.fetch(`/${conversationId}/typing/`, {
                method: 'POST',
                body: JSON.stringify({ is_typing: isTyping })
            });
            return data;
        } catch (error) {
            console.error('Failed to set typing status:', error);
            // Don't throw - typing status is non-critical
        }
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MessagesAPI;
}
