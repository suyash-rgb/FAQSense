import React from 'react'
import ChatWindow from './components/Chatbot/ChatWindow'
import FlowEditor from './components/FlowEditor/FlowEditor'
import './App.css'

function App() {
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>FAQSense Dashboard</h1>
        <p>Manage your chatbot and visualize Q&A flows.</p>
      </header>

      <main className="app-content">
        <FlowEditor />
      </main>

      <ChatWindow />
    </div>
  )
}

export default App
