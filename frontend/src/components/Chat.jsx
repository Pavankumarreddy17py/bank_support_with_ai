import React, { useState, useEffect, useRef } from 'react';

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  // Ref for the scrollable container
  const scrollRef = useRef(null);

  // Automatically scroll to the bottom when messages or loading state changes
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTo({
        top: scrollRef.current.scrollHeight,
        behavior: 'smooth',
      });
    }
  }, [messages, isLoading]);

  const send = async () => {
    if (!input.trim() || isLoading) return;

    // Add user message to UI immediately
    const userMessage = { from: 'user', text: input.trim() };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/customer/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          customer_id: 'cust_123', 
          message: userMessage.text 
        }),
      });

      if (!response.ok) throw new Error('Backend unreachable');

      const data = await response.json();
      
      // Add Bot response to UI
      setMessages((prev) => [...prev, { from: 'bot', text: data.response }]);
    } catch (err) {
      console.error("Chat Error:", err);
      setMessages((prev) => [...prev, { from: 'bot', text: 'Error: Could not connect to the Bank AI server.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearChat = () => setMessages([]);

  return (
    <div className="w-full bg-white/90 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 overflow-hidden flex flex-col h-[600px]">
      
      {/* Header Area */}
      <div className="bg-blue-600/10 p-4 border-b border-gray-200/50 flex justify-between items-center">
        <div className="flex items-center gap-3">
          <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
          <span className="font-semibold text-gray-700">Bank Support AI</span>
        </div>
        <button 
          onClick={clearChat}
          className="text-xs text-gray-400 hover:text-red-500 transition-colors"
        >
          Clear Chat
        </button>
      </div>

      {/* Message List Area */}
      <div 
        ref={scrollRef} 
        className="flex-1 overflow-y-auto p-6 space-y-4 custom-scrollbar"
      >
        {messages.length === 0 && (
          <div className="text-center text-gray-400 mt-20 animate-fade-in">
            <div className="bg-blue-50 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">🏦</span>
            </div>
            <p className="text-sm">Ask about your transactions</p>
          </div>
        )}

        {messages.map((m, i) => (
          <div 
            key={i} 
            className={`flex ${m.from === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in`}
          >
            <div className={`max-w-[85%] p-4 rounded-2xl shadow-sm ${
              m.from === 'user' 
                ? 'bg-blue-600 text-white rounded-br-none' 
                : 'bg-white text-gray-800 border border-gray-100 rounded-bl-none'
            }`}>
              <p className="text-sm leading-relaxed">{m.text}</p>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start animate-pulse">
            <div className="bg-gray-200/50 p-3 rounded-xl text-xs text-gray-500 flex items-center gap-2">
              <div className="w-1 h-1 bg-gray-400 rounded-full animate-bounce"></div>
              <div className="w-1 h-1 bg-gray-400 rounded-full animate-bounce [animation-delay:0.2s]"></div>
              <div className="w-1 h-1 bg-gray-400 rounded-full animate-bounce [animation-delay:0.4s]"></div>
              Analyzing dataset...
            </div>
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="p-4 bg-gray-50/50 border-t border-gray-200/50">
        <div className="flex gap-2 bg-white p-2 rounded-2xl border border-gray-200 shadow-inner focus-within:ring-2 focus-within:ring-blue-500/50 transition-all">
          <input 
            className="flex-1 px-4 py-2 focus:outline-none text-sm bg-transparent"
            placeholder="Search transactions ..."
            value={input} 
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && send()}
            disabled={isLoading}
          />
          <button 
            className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-md active:scale-95"
            onClick={send}
            disabled={isLoading || !input.trim()}
          >
            {isLoading ? '...' : 'Send'}
          </button>
        </div>
      </div>
    </div>
  );
}