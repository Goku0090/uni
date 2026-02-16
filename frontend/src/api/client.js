import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const client = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
client.interceptors.request.use(
  config => {
    // Get CSRF token if it exists
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value
    if (csrftoken) {
      config.headers['X-CSRFToken'] = csrftoken
    }
    return config
  },
  error => Promise.reject(error)
)

// Response interceptor
client.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      console.log('Unauthorized - redirect to login')
    }
    return Promise.reject(error)
  }
)

// API Methods
export const auth = {
  login: (email, password) => client.post('/login/', { email, password }),
  register: (email, password, full_name) => 
    client.post('/register/', { email, password, full_name }),
  logout: () => client.get('/logout/'),
  getProfile: () => client.get('/profile/'),
  updateProfile: (data) => client.put('/profile/', data),
}

export const projects = {
  list: () => client.get('/projects/'),
  get: (id) => client.get(`/projects/${id}/`),
  create: (data) => client.post('/projects/', data),
  update: (id, data) => client.put(`/projects/${id}/`, data),
  delete: (id) => client.delete(`/projects/${id}/`),
  like: (id) => client.post(`/projects/${id}/like/`),
  getComments: (id) => client.get(`/projects/${id}/comments/`),
  addComment: (id, content) => client.post(`/projects/${id}/comments/`, { content }),
}

export const messaging = {
  getChatRooms: () => client.get('/chat-rooms/'),
  createChatRoom: (name, members) => client.post('/chat-rooms/', { name, members }),
  getMessages: (roomId) => client.get(`/chat-rooms/${roomId}/messages/`),
  sendMessage: (roomId, content) => client.post('/messages/', { room: roomId, content }),
  directMessage: (userId) => client.post('/direct-message/', { user_id: userId }),
}

export const connections = {
  sendRequest: (userId) => client.post(`/connect/${userId}/`, {}),
  getConnections: () => client.get('/my-connections/'),
  acceptRequest: (connectionId) => client.post(`/accept-connection/${connectionId}/`, {}),
  rejectRequest: (connectionId) => client.post(`/reject-connection/${connectionId}/`, {}),
}

export const users = {
  getProfile: (username) => client.get(`/user/${username}/`),
  follow: (userId) => client.post(`/follow/${userId}/`, {}),
}

export default client
