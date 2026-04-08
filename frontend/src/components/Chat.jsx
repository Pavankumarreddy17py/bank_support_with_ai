import React, { useState, useEffect, useRef } from 'react';

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  const send = async () => {
    if (!input.trim() || isLoading) return;
    setMessages((prev) => [...prev, { from: 'user', text: input }]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/customer/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ customer_id: 'cust_123', message: input }),
      });
      const data = await response.json();
      setMessages((prev) => [...prev, { from: 'bot', text: data.response }]);
    } catch (err) {
      setMessages((prev) => [...prev, { from: 'bot', text: 'Server connection error.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full bg-white/90 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 overflow-hidden flex flex-col h-[600px]">
      {/* Header */}
      <div className="bg-blue-600/10 p-4 border-b border-gray-200/50 flex items-center gap-3">
        <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
        <span className="font-semibold text-gray-700">AI Support Agent</span>
      </div>

      {/* Messages */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto p-6 custom-scrollbar space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-400 mt-20">
            <p>Hello! How can I help with your transactions today?</p>
          </div>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.from === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in`}>
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
            <div className="bg-gray-200/50 p-3 rounded-xl text-xs text-gray-500">Processing...</div>
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="p-4 bg-gray-50/50 border-t border-gray-200/50">
        <div className="flex gap-2 bg-white p-2 rounded-2xl border border-gray-200 shadow-inner">
          <input 
            className="flex-1 px-4 py-2 focus:outline-none text-sm"
            placeholder="Type your banking query..."
            value={input} 
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && send()}
          />
          <button 
            className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-xl transition-all disabled:opacity-50"
            onClick={send}
            disabled={isLoading}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}