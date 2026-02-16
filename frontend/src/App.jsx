import { useState, useEffect } from 'react'
import client from './api/client'
import './App.css'

function App() {
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchProjects()
  }, [])

  const fetchProjects = async () => {
    try {
      setLoading(true)
      const response = await client.get('/projects/')
      setProjects(response.data)
    } catch (err) {
      console.error('Error fetching projects:', err)
      setError('Failed to load projects')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="App">
      <header>
        <h1>🎓 UniSync</h1>
        <p>Student Collaboration Platform</p>
      </header>

      <main>
        {loading && <p className="loading">Loading projects...</p>}
        {error && <p className="error">{error}</p>}
        
        {!loading && projects.length === 0 && (
          <p className="empty">No projects found. Start creating one!</p>
        )}

        {!loading && projects.length > 0 && (
          <div className="projects-grid">
            <h2>Recent Projects ({projects.length})</h2>
            <div className="projects">
              {projects.map(project => (
                <div key={project.id} className="project-card">
                  <h3>{project.title}</h3>
                  <p className="description">{project.description}</p>
                  <div className="meta">
                    <span className="category">{project.category}</span>
                    <span className="owner">By {project.owner?.username || 'Unknown'}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>

      <footer>
        <p>Connected to: {import.meta.env.VITE_API_URL}</p>
      </footer>
    </div>
  )
}

export default App
