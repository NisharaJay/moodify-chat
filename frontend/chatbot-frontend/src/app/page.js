"use client";
import { useState, useRef, useEffect } from "react";
import { Music, Send } from "lucide-react";

const quickMoods = [
  { label: "Happy", icon: "😊", query: "I feel happy" },
  { label: "Sad", icon: "😢", query: "I feel sad" },
  { label: "Energetic", icon: "⚡", query: "I feel energetic" },
  { label: "Calm", icon: "😌", query: "I feel calm" },
  { label: "Romantic", icon: "😍", query: "I feel romantic" },
];

export default function MoodifyChat() {
  const [messages, setMessages] = useState([{ type: "bot", text: "Hey there! 🎵 I'm Moodify, your personal music mood companion. Tell me how you're feeling, and I'll recommend the perfect songs for your vibe!", timestamp: new Date() }]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const endRef = useRef(null);

  useEffect(() => endRef.current?.scrollIntoView({ behavior: "smooth" }), [messages]);

  const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

  const sendMessage = async (text) => {
    if (!text.trim()) return;
    setMessages(prev => [...prev, { type: "user", text, timestamp: new Date() }]);
    setInput(""); setIsTyping(true);
    try {
      const data = await (await fetch(`${BACKEND_URL}/suggest`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ text }) })).json();
      setMessages(prev => [...prev, { type: "bot", text: data.text, songs: data.songs || [], timestamp: new Date() }]);
    } catch { setMessages(prev => [...prev, { type: "bot", text: "Oops! Something went wrong.", songs: [], timestamp: new Date() }]); }
    finally { setIsTyping(false); }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-950 to-black">
      <div className="container mx-auto px-4 py-5 max-w-4xl text-center">
        <div className="flex justify-center items-center gap-2 mb-1">
          <Music className="w-8 h-8 text-purple-300" />
          <h1 className="text-4xl font-bold text-white">Moodify</h1>
        </div>
        <p className="text-purple-300 mb-6">Your Personal Music Mood Companion</p>

        <div className="flex flex-wrap justify-center gap-2 mb-4">
          {quickMoods.map(m => (
            <button key={m.label} onClick={() => sendMessage(m.query)} className="bg-white/10 border border-white/20 rounded-full px-4 py-2 text-white hover:bg-white/20 transition-all">
              <span className="mr-1">{m.icon}</span>{m.label}
            </button>
          ))}
        </div>
        <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl overflow-hidden">
          <div className="h-[470px] overflow-y-auto p-4 space-y-3">
            {messages.map((msg, i) => (
              <div key={i} className={`flex ${msg.type==="user"?"justify-end":"justify-start"}`}>
                <div className="max-w-[80%]">
                  <div className={`rounded-xl p-3 ${msg.type==="user"?"bg-purple-500 text-white":"bg-white/20 text-white border border-white/30"}`}>
                    <p className="text-sm whitespace-pre-line">{msg.text}</p>
                    {msg.songs?.map((s,i)=>(
                      <a key={i} href={s.spotify_url} target="_blank" rel="noopener noreferrer" className="flex items-center gap-3 p-2 bg-white/10 rounded-lg hover:bg-white/20 transition-all">
                        {s.album_cover && <img src={s.album_cover} alt={s.title} className="w-20 h-auto rounded object-cover" />}
                        <div className="flex-1">
                          <p className="font-semibold text-sm">{s.title}</p>
                          <p className="text-xs text-purple-200">{s.artist}</p>
                          {s.preview_url && <audio controls src={s.preview_url} className="mt-1 w-full h-8" />}
                        </div>
                      </a>
                    ))}
                  </div>
                  <p className="text-xs text-purple-300 mt-1 px-2 flex justify-end">{msg.timestamp.toLocaleTimeString([], { hour:"2-digit", minute:"2-digit" })}</p>
                </div>
              </div>
            ))}
            {isTyping && <div className="flex justify-start"><div className="bg-white/20 rounded-xl p-3 flex gap-1">{[0,1,2].map(n=><div key={n} className="w-2 h-2 bg-purple-300 rounded-full animate-bounce" style={{animationDelay:`${n*0.2}s`}}/>)}</div></div>}
            <div ref={endRef} />
          </div>
          <div className="border-t border-white/20 p-3 bg-white/5 flex gap-2">
            <input type="text" value={input} onChange={e=>setInput(e.target.value)} onKeyPress={e=>e.key==="Enter"&&!e.shiftKey&&(e.preventDefault(),sendMessage(input))} placeholder="Tell me how you're feeling..." className="flex-1 bg-white/10 border border-white/20 rounded-xl px-4 py-2 text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-purple-400"/>
            <button onClick={()=>sendMessage(input)} className="bg-purple-500 hover:bg-purple-600 text-white rounded-xl px-4 py-2 transition-all"><Send className="w-5 h-5"/></button>
          </div>
        </div>
      </div>
    </div>
  );
}