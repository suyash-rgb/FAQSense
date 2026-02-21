import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import {
  SignedIn,
  SignedOut,
  SignInButton,
  SignUpButton,
  UserButton,
} from "@clerk/clerk-react";
import LandingPage from './pages/LandingPage'
import Dashboard from './pages/Dashboard'
import AuthPage from './pages/AuthPage'
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
        <Route path="/login" element={<AuthPage type="login" />} />
        <Route path="/signup" element={<AuthPage type="signup" />} />
      </Routes>
    </Router>
  )
}

export default App
