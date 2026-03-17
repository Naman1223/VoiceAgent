import React, { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import VideoPlayer from './VideoPlayer'
import LogoMarquee from './LogoMarquee'
import AnimatedMic from './AnimatedMic'

// ─── Fade-up variant helper ───────────────────────────────────────
const fadeUp = (delay = 0) => ({
  initial: { opacity: 0, y: 28 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.65, delay, ease: [0.22, 1, 0.36, 1] },
})

// ─── Chat send icon ───────────────────────────────────────────────
const SendIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M22 2L11 13M22 2L15 22l-4-9-9-4 20-7z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
)

// ─── ChatBox ─────────────────────────────────────────────────────
function ChatBox() {
  const [messages, setMessages] = useState([
    { id: 1, role: 'agent', text: 'Hi! I\'m your Synapse voice agent. How can I help you today?' },
  ])
  const [input, setInput] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isTyping])

  const handleSend = () => {
    const trimmed = input.trim()
    if (!trimmed) return

    const userMsg = { id: Date.now(), role: 'user', text: trimmed }
    setMessages((prev) => [...prev, userMsg])
    setInput('')
    setIsTyping(true)

    // Simulate agent thinking
    setTimeout(() => {
      setIsTyping(false)
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          role: 'agent',
          text: 'Got it! Processing your request… Use the mic for voice input.',
        },
      ])
    }, 1400)
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <motion.div
      {...fadeUp(0.45)}
      className="w-full max-w-lg mx-auto flex flex-col rounded-2xl overflow-hidden"
      style={{
        background: 'rgba(255,255,255,0.05)',
        backdropFilter: 'blur(24px)',
        WebkitBackdropFilter: 'blur(24px)',
        border: '1px solid rgba(255,255,255,0.10)',
        boxShadow: '0 24px 64px rgba(0,0,0,0.5)',
        height: 260,
      }}
    >
      {/* Message list */}
      <div className="flex-1 overflow-y-auto px-4 py-4 flex flex-col gap-3" style={{ scrollbarWidth: 'none' }}>
        <AnimatePresence initial={false}>
          {messages.map((msg) => (
            <motion.div
              key={msg.id}
              initial={{ opacity: 0, y: 10, scale: 0.97 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ duration: 0.28, ease: 'easeOut' }}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className="max-w-[80%] px-3.5 py-2 rounded-2xl text-sm leading-relaxed"
                style={
                  msg.role === 'user'
                    ? {
                        background: 'rgba(255,255,255,0.15)',
                        color: '#fff',
                        border: '1px solid rgba(255,255,255,0.18)',
                        borderBottomRightRadius: 6,
                      }
                    : {
                        background: 'rgba(255,255,255,0.07)',
                        color: 'rgba(255,255,255,0.80)',
                        border: '1px solid rgba(255,255,255,0.09)',
                        borderBottomLeftRadius: 6,
                      }
                }
              >
                {msg.text}
              </div>
            </motion.div>
          ))}

          {/* Typing indicator */}
          {isTyping && (
            <motion.div
              key="typing"
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="flex justify-start"
            >
              <div
                className="px-4 py-2.5 rounded-2xl flex items-center gap-1"
                style={{
                  background: 'rgba(255,255,255,0.07)',
                  border: '1px solid rgba(255,255,255,0.09)',
                  borderBottomLeftRadius: 6,
                }}
              >
                {[0, 1, 2].map((i) => (
                  <motion.span
                    key={i}
                    className="block w-1.5 h-1.5 rounded-full bg-white/50"
                    animate={{ opacity: [0.3, 1, 0.3] }}
                    transition={{ duration: 1, delay: i * 0.2, repeat: Infinity }}
                  />
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
        <div ref={bottomRef} />
      </div>

      {/* Divider */}
      <div style={{ height: 1, background: 'rgba(255,255,255,0.07)' }} />

      {/* Input bar */}
      <div className="flex items-center gap-3 px-4 py-3">
        <input
          id="chat-input"
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask anything…"
          className="flex-1 bg-transparent text-white/90 text-sm placeholder-white/30 outline-none"
        />
        <motion.button
          id="chat-send-btn"
          onClick={handleSend}
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          disabled={!input.trim()}
          className="flex items-center justify-center w-8 h-8 rounded-full text-white transition-all duration-200 disabled:opacity-30"
          style={{
            background: input.trim()
              ? 'rgba(255,255,255,0.18)'
              : 'rgba(255,255,255,0.06)',
            border: '1px solid rgba(255,255,255,0.15)',
          }}
        >
          <SendIcon />
        </motion.button>
      </div>
    </motion.div>
  )
}

// ─── Hero Section ─────────────────────────────────────────────────
export default function HeroSection() {
  const [micActive, setMicActive] = useState(false)

  return (
    <section
      className="relative min-h-screen w-full bg-black overflow-hidden flex flex-col"
      style={{ backgroundColor: '#000000' }}
    >
      {/* ── Full-bleed background video ── */}
      <VideoPlayer src="/video/bg.mp4" />

      {/* ── Very subtle dark vignette at edges to keep text readable ── */}
      <div
        className="absolute inset-0 z-0 pointer-events-none"
        style={{
          background:
            'radial-gradient(ellipse 120% 80% at 50% 50%, transparent 30%, rgba(0,0,0,0.55) 100%)',
        }}
      />

      {/* ── Hero Content ── */}
      <div className="relative z-10 flex flex-col items-center justify-center flex-1 pt-28 pb-10 px-4 text-center gap-10">

        {/* Headline */}
        <motion.div {...fadeUp(0)} className="flex flex-col items-center gap-4">
          <motion.h1
            className="hero-headline text-white max-w-4xl mx-auto"
            style={{
              background: 'linear-gradient(180deg, #ffffff 0%, rgba(255,255,255,0.72) 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text',
            }}
          >
            Your Personal<br />Local AI Assistant
          </motion.h1>

          <motion.p
            {...fadeUp(0.15)}
            className="text-white/50 text-lg max-w-xl mx-auto leading-relaxed"
          >
            No Data Leaks — your task done locally.
          </motion.p>
        </motion.div>

        {/* Animated Mic — center of page */}
        <motion.div {...fadeUp(0.3)}>
          <AnimatedMic
            isActive={micActive}
            onClick={() => setMicActive((v) => !v)}
          />
        </motion.div>

        {/* Chat Box — replaces Chat button */}
        <ChatBox />
      </div>

      {/* ── Logo Marquee ── */}
      <motion.div
        {...fadeUp(0.6)}
        className="relative z-10 mt-auto"
        style={{ borderTop: '1px solid rgba(255,255,255,0.06)' }}
      >
        <LogoMarquee />
      </motion.div>

      {/* ── GitHub button — covers video watermark at bottom-right ── */}
      <a
        href="https://github.com/Naman1223/VoiceAgent"
        target="_blank"
        rel="noopener noreferrer"
        id="github-watermark-btn"
        className="absolute bottom-0 right-0 z-20 flex items-center gap-2 px-4 py-3 transition-opacity duration-200 hover:opacity-100"
        style={{
          width: 210,
          height: 72,
          background: 'linear-gradient(135deg, rgba(0,0,0,0.92) 60%, rgba(20,20,20,0.80))',
          backdropFilter: 'blur(8px)',
          WebkitBackdropFilter: 'blur(8px)',
          borderTop: '1px solid rgba(255,255,255,0.08)',
          borderLeft: '1px solid rgba(255,255,255,0.08)',
          borderTopLeftRadius: 12,
          opacity: 0.85,
        }}
      >
        {/* GitHub SVG */}
        <svg width="22" height="22" viewBox="0 0 24 24" fill="white" xmlns="http://www.w3.org/2000/svg" style={{ flexShrink: 0 }}>
          <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/>
        </svg>
        <div className="flex flex-col leading-tight">
          <span className="text-white text-xs font-semibold tracking-tight">View on GitHub</span>
          <span className="text-white/45 text-[10px]">Naman1223 / VoiceAgent</span>
        </div>
      </a>
    </section>
  )
}
