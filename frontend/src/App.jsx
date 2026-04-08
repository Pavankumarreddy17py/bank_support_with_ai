import React from 'react'
import Chat from './components/Chat'

export default function App(){
  return (
    <div 
      className="min-h-screen flex flex-col items-center justify-center p-6 bg-cover bg-center bg-no-repeat"
      style={{ 
        backgroundImage: `url('https://images.unsplash.com/photo-1620714223084-8fcacc6dfd8d?q=80&w=2071&auto=format&fit=crop')`,
        backgroundColor: 'rgba(0,0,0,0.5)',
        backgroundBlendMode: 'overlay'
      }}
    >
      <div className="w-full max-w-4xl flex flex-col md:flex-row gap-8 items-start animate-fade-in">
        {/* Left Side: Branding / Info */}
        <div className="text-white md:w-1/3 pt-10">
          <h1 className="text-4xl font-bold mb-4">Bank Support AI</h1>
          <p className="text-gray-200 text-lg">
            Securely managing your transactions with real-time fraud detection powered by AI.
          </p>
          <div className="mt-8 p-4 bg-white/10 backdrop-blur-md rounded-lg border border-white/20">
            <p className="text-sm font-semibold">Active Customers:</p>
            <p className="text-xs opacity-70">1 million+</p>
          </div>
        </div>

        {/* Right Side: Chat Interface */}
        <div className="md:w-2/3 w-full">
          <Chat />
        </div>
      </div>
    </div>
  )
}