import React from 'react'
import Chat from './components/Chat'

export default function App(){
  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <h1 className="text-2xl font-bold mb-4">Bank Support AI</h1>
      <Chat />
    </div>
  )
}
