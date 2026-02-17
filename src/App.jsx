import React from 'react'
import ChatWindow from './components/Chatbot/ChatWindow'
import FlowEditor from './components/FlowEditor/FlowEditor'
import './App.css'

function App() {
  const isWidget = new URLSearchParams(window.location.search).get('mode') === 'widget';

  if (isWidget) {
    return <ChatWindow />;
  }

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
