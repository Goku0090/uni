/**
 * API Utilities for UniSinq
 * Handles common API calls and AJAX requests
 */

// Get CSRF token from cookies
function getCookie(name) {
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
}

const csrftoken = getCookie('csrftoken');

/**
 * Send connection request
 */
function sendConnectionRequest(userId, buttonElement) {
    fetch(`/connect/${userId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            buttonElement.disabled = true;
            buttonElement.textContent = 'Request Sent';
            buttonElement.classList.add('btn-secondary');
            buttonElement.classList.remove('btn-primary');
            showNotification('Connection request sent!', 'success');
        } else {
            showNotification(data.message || 'Failed to send request', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('An error occurred', 'error');
    });
}

/**
 * Accept connection request
 */
function acceptConnection(connectionId, containerElement) {
    fetch(`/accept-connection/${connectionId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            containerElement.innerHTML = '<p class="text-success">Connection accepted!</p>';
            showNotification('Connection accepted!', 'success');
        } else {
            showNotification(data.message || 'Failed to accept', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('An error occurred', 'error');
    });
}

/**
 * Reject connection request
 */
function rejectConnection(connectionId, containerElement) {
    fetch(`/reject-connection/${connectionId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            containerElement.innerHTML = '<p class="text-muted">Connection rejected</p>';
            showNotification('Connection rejected', 'info');
        } else {
            showNotification(data.message || 'Failed to reject', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('An error occurred', 'error');
    });
}

/**
 * Like a project
 */
function likeProject(projectId, buttonElement) {
    fetch(`/like-project/${projectId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (data.liked) {
                buttonElement.classList.add('liked');
                buttonElement.innerHTML = '<i class="fas fa-heart"></i> Unlike';
                showNotification('Project liked!', 'success');
            } else {
                buttonElement.classList.remove('liked');
                buttonElement.innerHTML = '<i class="far fa-heart"></i> Like';
                showNotification('Project unliked', 'info');
            }
        } else {
            showNotification(data.message || 'Failed to like project', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('An error occurred', 'error');
    });
}

/**
 * Mark notification as read
 */
function markNotificationRead(notificationId) {
    fetch(`/notification/${notificationId}/read/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Reload notifications
            location.reload();
        }
    })
    .catch(error => console.error('Error:', error));
}

/**
 * Show notification toast
 */
function showNotification(message, type = 'info') {
    // Check if using Bootstrap Toast or custom notification
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
    alertDiv.setAttribute('role', 'alert');
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.notification-container') || document.body;
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

/**
 * Fetch and update user stats
 */
function updateUserStats(userId) {
    fetch(`/api/user/${userId}/stats/`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('projects-count').textContent = data.projects_created;
            document.getElementById('connections-count').textContent = data.connections_made;
            document.getElementById('likes-count').textContent = data.likes_received;
        })
        .catch(error => console.error('Error:', error));
}

/**
 * Load more messages (pagination)
 */
function loadMoreMessages(userId, page) {
    fetch(`/chat/${userId}/?page=${page}`)
        .then(response => response.text())
        .then(html => {
            // Parse and append new messages
            const parser = new DOMParser();
            const newDoc = parser.parseFromString(html, 'text/html');
            const newMessages = newDoc.querySelectorAll('.message');
            const messageContainer = document.querySelector('.messages-container');
            
            newMessages.forEach(msg => {
                messageContainer.appendChild(msg);
            });
        })
        .catch(error => console.error('Error:', error));
}

/**
 * Delete message (admin only)
 */
function deleteMessage(messageId) {
    if (confirm('Are you sure you want to delete this message?')) {
        fetch(`/message/${messageId}/delete/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.querySelector(`[data-message-id="${messageId}"]`).remove();
                showNotification('Message deleted', 'success');
            } else {
                showNotification(data.message || 'Failed to delete', 'error');
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

/**
 * React to message with emoji
 */
function addReaction(messageId, emoji) {
    fetch(`/message/${messageId}/react/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ reaction: emoji }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update reaction display
            const reactionContainer = document.querySelector(`[data-message-id="${messageId}"] .reactions`);
            reactionContainer.innerHTML = data.reactions_html;
        }
    })
    .catch(error => console.error('Error:', error));
}

/**
 * Initialize WebSocket for real-time messaging
 */
function initializeWebSocket(roomName) {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const ws = new WebSocket(
        protocol + '//' + window.location.host + '/ws/chat/' + roomName + '/'
    );

    ws.onopen = function(e) {
        console.log('WebSocket connection established');
    };

    ws.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if (data.type === 'chat_message') {
            // Display new message
            const messageEl = createMessageElement(data);
            document.querySelector('.messages-container').appendChild(messageEl);
        } else if (data.type === 'user_typing') {
            // Show typing indicator
            showTypingIndicator(data.username);
        }
    };

    ws.onclose = function(e) {
        console.log('WebSocket connection closed');
    };

    ws.onerror = function(e) {
        console.error('WebSocket error:', e);
    };

    return ws;
}

/**
 * Create message element for real-time display
 */
function createMessageElement(data) {
    const div = document.createElement('div');
    div.className = `message ${data.sender_id === userId ? 'sent' : 'received'}`;
    div.setAttribute('data-message-id', data.id);
    div.innerHTML = `
        <div class="message-content">
            <p>${escapeHtml(data.content)}</p>
            <small class="text-muted">${data.timestamp}</small>
        </div>
    `;
    return div;
}

/**
 * Show typing indicator
 */
function showTypingIndicator(username) {
    const typingDiv = document.querySelector('.typing-indicator');
    if (typingDiv) {
        typingDiv.textContent = `${username} is typing...`;
        typingDiv.style.display = 'block';
        
        // Hide after 3 seconds
        setTimeout(() => {
            typingDiv.style.display = 'none';
        }, 3000);
    }
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Format timestamp to readable format
 */
function formatTime(timestamp) {
    const date = new Date(timestamp);
    const today = new Date();
    
    if (date.toDateString() === today.toDateString()) {
        return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    } else {
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    }
}

/**
 * Send typing indicator
 */
function sendTypingIndicator(ws) {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({
            type: 'typing',
        }));
    }
}

// Export functions for use in templates
window.apiUtils = {
    sendConnectionRequest,
    acceptConnection,
    rejectConnection,
    likeProject,
    markNotificationRead,
    showNotification,
    updateUserStats,
    loadMoreMessages,
    deleteMessage,
    addReaction,
    initializeWebSocket,
    createMessageElement,
    showTypingIndicator,
    escapeHtml,
    formatTime,
    sendTypingIndicator,
};
