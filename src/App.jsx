import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import LandingPage from './pages/LandingPage'
import Dashboard from './pages/Dashboard'
import ChatWindow from './components/Chatbot/ChatWindow'
import './App.css'

function App() {
  const isWidget = new URLSearchParams(window.location.search).get('mode') === 'widget';

  if (isWidget) {
    return <ChatWindow />;
  }

  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Router>
  )
}

export default App
