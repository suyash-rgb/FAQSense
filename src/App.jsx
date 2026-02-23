import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import {
  SignedIn,
  SignedOut,
  SignInButton,
  SignUpButton,
  UserButton,
  RedirectToSignIn
} from "@clerk/clerk-react";
import LandingPage from './pages/LandingPage'
import Dashboard from './pages/Dashboard'
import AuthPage from './pages/AuthPage'
import ChatWindow from './components/Chatbot/ChatWindow'
import './App.css'

function App() {
  const isWidget = new URLSearchParams(window.location.search).get('mode') === 'widget';

  if (isWidget) {
    return <ChatWindow forceOpen={true} height="100%" />;
  }

  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route
          path="/dashboard"
          element={
            <>
              <SignedIn>
                <Dashboard />
              </SignedIn>
              <SignedOut>
                <RedirectToSignIn />
              </SignedOut>
            </>
          }
        />
        <Route path="/login" element={<AuthPage type="login" />} />
        <Route path="/signup" element={<AuthPage type="signup" />} />
      </Routes>
    </Router>
  )
}

export default App
