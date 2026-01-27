import { useState, useEffect } from 'react'
import { Routes, Route, useNavigate } from 'react-router-dom'
import { Layout } from './Main/Layout.jsx'
import { LoginForm } from './Auth/Login.jsx'
import { RegisterForm } from './Registration/RegisterForm.jsx'
import './App.css'


const Home = () => {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await fetch('/api/', {credentials: 'include', redirect: 'manual'})
        console.log("Response:", res)
        if (res.ok) {
          setData(await res.json())
          console.log("Data:", data)
        } else {
          navigate('/login')
        }
      } catch { 
        navigate('/login')
      } finally {
        setLoading(false)
      }
    }
    setLoading(true)
    fetchData()
  }, []);

  if (loading) {
    return <div>Loading...</div>
  }

  return (
    <div>
      <h1>Vite + React</h1>
    </div>
  )
}

const App = () => {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<LoginForm />} />
        <Route path="/register" element={<RegisterForm />} />
      </Routes>
    </Layout>
  )
}

export default App
