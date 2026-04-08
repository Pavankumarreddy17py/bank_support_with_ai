import React, {useState} from 'react'

export default function Chat(){
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')

  const send = async () =>{
    if(!input) return
    setMessages([...messages, {from:'user', text: input}])
    setInput('')
    // TODO: call backend chatbot endpoint
    setMessages(prev => [...prev, {from:'bot', text: 'This is a placeholder response.'}])
  }

  return (
    <div className="max-w-xl bg-white rounded shadow p-4">
      <div className="h-64 overflow-y-auto mb-4 border p-2">
        {messages.map((m, i) => (
          <div key={i} className={m.from === 'user' ? 'text-right' : 'text-left'}>{m.text}</div>
        ))}
      </div>
      <div className="flex gap-2">
        <input className="flex-1 border p-2" value={input} onChange={e => setInput(e.target.value)} />
        <button className="bg-blue-600 text-white px-4 py-2 rounded" onClick={send}>Send</button>
      </div>
    </div>
  )
}
