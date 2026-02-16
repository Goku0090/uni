/**
 * Real-time Project Updates - WebSocket Client
 * Handles live project status, activity feed, and notifications
 */

class RealtimeUpdates {
    constructor() {
        this.projectSocket = null;
        this.activitySocket = null;
        this.notificationSocket = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 3000;
    }

    /**
     * Initialize all WebSocket connections
     */
    init() {
        console.log('Initializing real-time updates...');
        
        const projectId = this.getProjectId();
        if (projectId) {
            this.connectToProjectUpdates(projectId);
        }
        
        this.connectToActivityFeed();
        this.connectToNotifications();
    }

    /**
     * Connect to project-specific updates
     */
    connectToProjectUpdates(projectId) {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/project/${projectId}/`;
        
        this.projectSocket = new WebSocket(wsUrl);
        
        this.projectSocket.onopen = () => {
            console.log(`Connected to project ${projectId} updates`);
            this.reconnectAttempts = 0;
            this.showNotification('Connected to project updates', 'success');
        };
        
        this.projectSocket.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                this.handleProjectMessage(data);
            } catch (error) {
                console.error('Error parsing project message:', error);
            }
        };
        
        this.projectSocket.onerror = (error) => {
            console.error('Project WebSocket error:', error);
            this.showNotification('Connection error. Retrying...', 'error');
        };
        
        this.projectSocket.onclose = () => {
            console.log('Disconnected from project updates');
            this.attemptReconnect(() => this.connectToProjectUpdates(projectId));
        };
    }

    /**
     * Connect to activity feed
     */
    connectToActivityFeed() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/activity-feed/`;
        
        this.activitySocket = new WebSocket(wsUrl);
        
        this.activitySocket.onopen = () => {
            console.log('Connected to activity feed');
        };
        
        this.activitySocket.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                this.handleActivityMessage(data);
            } catch (error) {
                console.error('Error parsing activity message:', error);
            }
        };
        
        this.activitySocket.onerror = (error) => {
            console.error('Activity WebSocket error:', error);
        };
        
        this.activitySocket.onclose = () => {
            console.log('Disconnected from activity feed');
            this.attemptReconnect(() => this.connectToActivityFeed());
        };
    }

    /**
     * Connect to notifications
     */
    connectToNotifications() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/notifications/`;
        
        this.notificationSocket = new WebSocket(wsUrl);
        
        this.notificationSocket.onopen = () => {
            console.log('Connected to notifications');
        };
        
        this.notificationSocket.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                this.handleNotificationMessage(data);
            } catch (error) {
                console.error('Error parsing notification message:', error);
            }
        };
        
        this.notificationSocket.onerror = (error) => {
            console.error('Notification WebSocket error:', error);
        };
        
        this.notificationSocket.onclose = () => {
            console.log('Disconnected from notifications');
            this.attemptReconnect(() => this.connectToNotifications());
        };
    }

    /**
     * Handle project update messages
     */
    handleProjectMessage(data) {
        const type = data.type;
        
        switch (type) {
            case 'project.initial_data':
                console.log('Project initial data:', data.data);
                this.updateProjectInfo(data.data);
                break;
                
            case 'project.status_update':
                this.onProjectStatusUpdate(data);
                break;
                
            case 'project.member_added':
                this.onMemberAdded(data);
                break;
                
            case 'project.comment_posted':
                this.onCommentPosted(data);
                break;
                
            case 'project.member_count':
                this.onMemberCountUpdate(data);
                break;
                
            case 'error':
                this.showNotification(data.message, 'error');
                break;
                
            default:
                console.log('Unknown message type:', type);
        }
    }

    /**
     * Handle activity feed messages
     */
    handleActivityMessage(data) {
        if (data.type === 'activity.update') {
            this.addActivityFeedItem(data);
        }
    }

    /**
     * Handle notification messages
     */
    handleNotificationMessage(data) {
        const type = data.type;
        
        switch (type) {
            case 'notification.received':
                this.showDesktopNotification(data);
                this.updateNotificationBadge(data);
                break;
                
            case 'notification.count':
                this.updateUnreadCount(data.unread_count);
                break;
                
            default:
                console.log('Unknown notification type:', type);
        }
    }

    /**
     * Project status update handler
     */
    onProjectStatusUpdate(data) {
        console.log('Project status updated:', data.status);
        
        // Update UI
        const statusElement = document.getElementById('project-status');
        if (statusElement) {
            statusElement.textContent = data.status;
            statusElement.className = `badge badge-${this.getStatusColor(data.status)}`;
        }
        
        // Show notification
        this.showNotification(
            `Project status changed to ${data.status}`,
            'info'
        );
        
        // Add to activity log
        this.addActivityLog({
            action: data.message || 'Status updated',
            actor: data.changed_by,
            timestamp: data.timestamp,
            icon: '⚡'
        });
    }

    /**
     * Member added handler
     */
    onMemberAdded(data) {
        console.log('Member added:', data.username);
        
        // Update members list
        this.addMemberToList({
            id: data.user_id,
            username: data.username,
            full_name: data.full_name
        });
        
        // Update member count
        this.updateMemberCount();
        
        // Show notification
        this.showNotification(
            `${data.full_name} joined the team!`,
            'success'
        );
        
        // Play sound
        this.playNotificationSound();
        
        // Add to activity log
        this.addActivityLog({
            action: `Joined the team`,
            actor: data.username,
            timestamp: data.timestamp,
            icon: '👥'
        });
    }

    /**
     * Comment posted handler
     */
    onCommentPosted(data) {
        console.log('Comment posted:', data.comment_id);
        
        // Add comment to feed
        this.addCommentToFeed({
            id: data.comment_id,
            author: data.author,
            text: data.text,
            timestamp: data.timestamp
        });
        
        // Update comment count
        this.updateCommentCount();
        
        // Show notification
        this.showNotification(
            `${data.author} commented on the project`,
            'info'
        );
    }

    /**
     * Member count update handler
     */
    onMemberCountUpdate(data) {
        console.log('Member count updated:', data.current_members);
        
        const element = document.getElementById('member-count');
        if (element) {
            element.textContent = `${data.current_members}/${data.required_members || '∞'}`;
        }
    }

    /**
     * Add activity feed item
     */
    addActivityFeedItem(data) {
        const feedContainer = document.getElementById('activity-feed');
        if (!feedContainer) return;
        
        const item = document.createElement('div');
        item.className = 'activity-item';
        item.innerHTML = `
            <div class="activity-icon">${data.icon}</div>
            <div class="activity-content">
                <p class="activity-action">${data.action}</p>
                <p class="activity-meta">
                    <strong>${data.actor}</strong> in <strong>${data.project_title}</strong>
                </p>
                <p class="activity-time">${this.formatTime(data.timestamp)}</p>
            </div>
        `;
        
        feedContainer.insertBefore(item, feedContainer.firstChild);
        
        // Remove old items if too many
        while (feedContainer.children.length > 50) {
            feedContainer.removeChild(feedContainer.lastChild);
        }
    }

    /**
     * Add activity log entry
     */
    addActivityLog(activity) {
        const logContainer = document.getElementById('activity-log');
        if (!logContainer) return;
        
        const entry = document.createElement('div');
        entry.className = 'log-entry';
        entry.innerHTML = `
            <span class="icon">${activity.icon}</span>
            <span class="action">${activity.action}</span>
            <span class="actor">by ${activity.actor}</span>
            <span class="time">${this.formatTime(activity.timestamp)}</span>
        `;
        
        logContainer.insertBefore(entry, logContainer.firstChild);
    }

    /**
     * Add member to members list
     */
    addMemberToList(member) {
        const membersList = document.getElementById('project-members');
        if (!membersList) return;
        
        // Check if member already exists
        if (document.getElementById(`member-${member.id}`)) return;
        
        const memberCard = document.createElement('div');
        memberCard.id = `member-${member.id}`;
        memberCard.className = 'member-card';
        memberCard.innerHTML = `
            <div class="member-avatar">👤</div>
            <div class="member-info">
                <p class="member-name">${member.full_name}</p>
                <p class="member-username">@${member.username}</p>
            </div>
        `;
        
        membersList.appendChild(memberCard);
    }

    /**
     * Add comment to feed
     */
    addCommentToFeed(comment) {
        const commentsFeed = document.getElementById('comments-feed');
        if (!commentsFeed) return;
        
        const commentEl = document.createElement('div');
        commentEl.className = 'comment-item';
        commentEl.innerHTML = `
            <div class="comment-header">
                <strong>${comment.author}</strong>
                <span class="comment-time">${this.formatTime(comment.timestamp)}</span>
            </div>
            <div class="comment-text">${this.escapeHtml(comment.text)}</div>
        `;
        
        commentsFeed.insertBefore(commentEl, commentsFeed.firstChild);
    }

    /**
     * Update project info
     */
    updateProjectInfo(projectData) {
        console.log('Updating project info:', projectData);
        
        // Update status
        const statusEl = document.getElementById('project-status');
        if (statusEl) {
            statusEl.textContent = projectData.status;
        }
        
        // Update member count
        const memberCountEl = document.getElementById('member-count');
        if (memberCountEl) {
            memberCountEl.textContent = projectData.members_count;
        }
    }

    /**
     * Update member count in UI
     */
    updateMemberCount() {
        // This would be called after member is added
        const countEl = document.getElementById('member-count');
        if (countEl) {
            const current = parseInt(countEl.textContent) || 0;
            countEl.textContent = current + 1;
        }
    }

    /**
     * Update comment count in UI
     */
    updateCommentCount() {
        const countEl = document.getElementById('comment-count');
        if (countEl) {
            const current = parseInt(countEl.textContent) || 0;
            countEl.textContent = current + 1;
        }
    }

    /**
     * Update unread notification count
     */
    updateUnreadCount(count) {
        const badge = document.getElementById('notification-badge');
        if (badge) {
            if (count > 0) {
                badge.textContent = count > 99 ? '99+' : count;
                badge.style.display = 'block';
            } else {
                badge.style.display = 'none';
            }
        }
    }

    /**
     * Update notification badge
     */
    updateNotificationBadge(data) {
        const badge = document.getElementById('notification-badge');
        if (badge) {
            const current = parseInt(badge.textContent) || 0;
            badge.textContent = (current + 1) > 99 ? '99+' : (current + 1);
            badge.style.display = 'block';
        }
    }

    /**
     * Show desktop notification
     */
    showDesktopNotification(data) {
        if ('Notification' in window && Notification.permission === 'granted') {
            const notification = new Notification(data.title, {
                body: data.message,
                tag: 'unisinq-notification',
                badge: '/static/images/logo.jpg',
                sound: data.sound ? '/static/sounds/notification.mp3' : undefined
            });
            
            notification.onclick = () => {
                window.focus();
                notification.close();
                
                // Navigate to related object if available
                if (data.related_object_id) {
                    window.location.href = `/project/${data.related_object_id}/`;
                }
            };
            
            // Auto-close after 5 seconds
            setTimeout(() => notification.close(), 5000);
        }
    }

    /**
     * Show toast notification
     */
    showNotification(message, type = 'info') {
        const container = document.getElementById('notification-container');
        if (!container) return;
        
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <span>${message}</span>
            <button class="toast-close">&times;</button>
        `;
        
        container.appendChild(toast);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            toast.remove();
        }, 5000);
        
        // Manual close button
        toast.querySelector('.toast-close').onclick = () => {
            toast.remove();
        };
    }

    /**
     * Play notification sound
     */
    playNotificationSound() {
        try {
            const audio = new Audio('/static/sounds/notification.mp3');
            audio.play().catch(error => {
                console.log('Could not play notification sound:', error);
            });
        } catch (error) {
            console.log('Notification sound error:', error);
        }
    }

    /**
     * Send project status update
     */
    updateProjectStatus(newStatus) {
        if (!this.projectSocket || this.projectSocket.readyState !== WebSocket.OPEN) {
            this.showNotification('Not connected to project. Please refresh.', 'error');
            return;
        }
        
        this.projectSocket.send(JSON.stringify({
            type: 'status.update',
            status: newStatus
        }));
        
        console.log('Sent status update:', newStatus);
    }

    /**
     * Add member to project
     */
    addMember(userId) {
        if (!this.projectSocket || this.projectSocket.readyState !== WebSocket.OPEN) {
            this.showNotification('Not connected to project. Please refresh.', 'error');
            return;
        }
        
        this.projectSocket.send(JSON.stringify({
            type: 'member.add',
            user_id: userId
        }));
        
        console.log('Sent member add request:', userId);
    }

    /**
     * Post comment
     */
    postComment(commentText) {
        if (!this.projectSocket || this.projectSocket.readyState !== WebSocket.OPEN) {
            this.showNotification('Not connected to project. Please refresh.', 'error');
            return;
        }
        
        this.projectSocket.send(JSON.stringify({
            type: 'comment.post',
            text: commentText
        }));
        
        console.log('Comment sent');
    }

    /**
     * Request desktop notification permission
     */
    requestNotificationPermission() {
        if ('Notification' in window && Notification.permission === 'default') {
            Notification.requestPermission().then(permission => {
                if (permission === 'granted') {
                    console.log('Desktop notifications enabled');
                }
            });
        }
    }

    /**
     * Attempt to reconnect to WebSocket
     */
    attemptReconnect(reconnectFn) {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
            
            console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
            setTimeout(reconnectFn, delay);
        } else {
            console.error('Max reconnection attempts reached');
            this.showNotification('Connection lost. Please refresh the page.', 'error');
        }
    }

    /**
     * Get project ID from current page
     */
    getProjectId() {
        // Extract from URL like /project/123/
        const match = window.location.pathname.match(/\/project\/(\d+)\//);
        return match ? match[1] : null;
    }

    /**
     * Get status color class
     */
    getStatusColor(status) {
        const colors = {
            'planning': 'info',
            'active': 'success',
            'recruiting': 'warning',
            'completed': 'dark',
            'paused': 'secondary'
        };
        return colors[status] || 'secondary';
    }

    /**
     * Format timestamp
     */
    formatTime(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diff = now - date;
        
        const seconds = Math.floor(diff / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);
        const days = Math.floor(hours / 24);
        
        if (seconds < 60) return 'just now';
        if (minutes < 60) return `${minutes}m ago`;
        if (hours < 24) return `${hours}h ago`;
        if (days < 7) return `${days}d ago`;
        
        return date.toLocaleDateString();
    }

    /**
     * Escape HTML to prevent XSS
     */
    escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    }

    /**
     * Disconnect all WebSockets
     */
    disconnect() {
        if (this.projectSocket) {
            this.projectSocket.close();
            this.projectSocket = null;
        }
        if (this.activitySocket) {
            this.activitySocket.close();
            this.activitySocket = null;
        }
        if (this.notificationSocket) {
            this.notificationSocket.close();
            this.notificationSocket = null;
        }
    }
}

// Initialize on page load
let realtimeUpdates;
document.addEventListener('DOMContentLoaded', () => {
    realtimeUpdates = new RealtimeUpdates();
    realtimeUpdates.init();
    realtimeUpdates.requestNotificationPermission();
});

// Clean up on page unload
window.addEventListener('beforeunload', () => {
    if (realtimeUpdates) {
        realtimeUpdates.disconnect();
    }
});
