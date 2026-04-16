import React from 'react'

// ─── Icons for each local AI tool ────────────────────────────────

const WhisperIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M19 10v2a7 7 0 0 1-14 0v-2M12 19v4M8 23h8" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
)

const LlamaIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="12" cy="12" r="3" fill="currentColor" opacity="0.9"/>
    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z" stroke="currentColor" strokeWidth="1.8"/>
    <path d="M12 6v2M12 16v2M6 12H8M16 12h2" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"/>
  </svg>
)

const KokoroIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M9 18V5l12-2v13" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
    <circle cx="6" cy="18" r="3" stroke="currentColor" strokeWidth="1.8"/>
    <circle cx="18" cy="16" r="3" stroke="currentColor" strokeWidth="1.8"/>
  </svg>
)

const tools = [
  { name: 'Faster Whisper', sub: 'Speech-to-Text', icon: <WhisperIcon /> },
  { name: 'Llama 3',        sub: 'Language Model', icon: <LlamaIcon />   },
  { name: 'Kokoro',         sub: 'Text-to-Speech', icon: <KokoroIcon />  },
]

export default function LogoMarquee() {
  return (
    <div className="w-full py-6 px-4">
      <p className="text-center text-xs text-white/30 uppercase tracking-widest mb-6 font-medium">
        Powered by
      </p>
      <div className="flex items-center justify-center gap-12 flex-wrap">
        {tools.map((tool) => (
          <div
            key={tool.name}
            className="flex items-center gap-3 group transition-opacity duration-300 hover:opacity-70"
            style={{ opacity: 0.45 }}
            title={tool.sub}
          >
            <div className="text-white">{tool.icon}</div>
            <div className="flex flex-col leading-tight">
              <span className="text-white text-sm font-semibold tracking-tight">{tool.name}</span>
              <span className="text-white/50 text-[10px] font-normal">{tool.sub}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
