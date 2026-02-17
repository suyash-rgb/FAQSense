import React from 'react'
import ChatWindow from './components/Chatbot/ChatWindow'
import './App.css'

function App() {
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>FAQSense Dashboard</h1>
        <p>Manage your chatbot and visualize Q&A flows.</p>
      </header>

      <main className="app-content">
        <div className="placeholder-content">
          <h2>Flow Editor coming soon...</h2>
          <p>The chatbot preview is in the bottom right corner.</p>
        </div>
      </main>

      <ChatWindow />
    </div>
  )
}

export default App
