import { useState } from 'react'
import emailjs from '@emailjs/browser'
import AIPulseLine from '../components/AIPulseLine'
import SEO from '../components/SEO'

const WAVE_DELAYS = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]
const WAVE_HEIGHTS = ['h-4', 'h-7', 'h-10', 'h-6', 'h-12', 'h-8', 'h-5', 'h-9', 'h-11', 'h-6', 'h-4', 'h-7', 'h-3']

const features = [
  {
    id: 'feature-speed',
    icon: 'bolt',
    title: 'Zero Cloud Latency',
    description: 'Talk and get instant responses. No round-trips to remote servers means interaction happens at the speed of thought.',
  },
  {
    id: 'feature-privacy',
    icon: 'lock',
    title: 'Total Privacy',
    description: 'Runs entirely on your own hardware. Your conversations, documents, and identity never touch the public internet.',
  },
  {
    id: 'feature-files',
    icon: 'folder_open',
    title: 'Local File Integration',
    description: 'It natively searches documents and reads your PDFs. Turn your local knowledge base into an interactive dialogue.',
  },
]

const capabilities = [
  { id: 'cap-pdf', icon: 'description', title: 'PDF & Document Reading', description: 'Ask your assistant to read, summarize, or answer questions from any PDF or document on your local drive—instantly.' },
  { id: 'cap-files', icon: 'folder_managed', title: 'File System Navigation', description: 'Move files, create folders, and search across your entire system using natural language voice commands.' },
  { id: 'cap-tools', icon: 'build', title: 'Tool Integration', description: 'Connect with local apps and APIs. Open applications, run scripts, and automate workflows—all hands-free.' },
  { id: 'cap-memory', icon: 'history', title: 'Persistent Local Memory', description: 'Your assistant remembers context across conversations. All stored locally in an encrypted vector database you control.' },
]

function EarlyAccessForm({ inputId, btnClass = '', inputClass = '', placeholderClass = '' }) {
  const [email, setEmail] = useState('')
  const [done, setDone] = useState(false)
  const [error, setError] = useState(false)

  const handleSubmit = async () => {
    if (!email || !email.includes('@')) {
      setError(true)
      setTimeout(() => setError(false), 2000)
      return
    }
    
    try {
      // 1. Send data to SheetMonkey (for your Google Sheet)
      await fetch('https://api.sheetmonkey.io/form/cHsdnmiBFmbDHHmd2VA5eb', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          Email: email,
          Type: 'Early Access',
          Created: 'x-sheetmonkey-current-date-time',
        }),
      })

      // 2. Send the Welcome Email via EmailJS
      // Replace these three placeholders with your actual IDs from EmailJS
      await emailjs.send(
        'service_elp4fqk',   // e.g., 'service_xxxxx'
        'template_44tu7kh',  // e.g., 'template_xxxxx'
        { user_email: email }, // The variable in your template where the email goes
        'yKJap9suzamzpDGUG'  // e.g., 'xxxxx_xxxx_xxxxx'
      )
    } catch (e) {
      console.error('Submission error:', e)
    }
    setDone(true)
  }

  return (
    <div className="flex flex-col sm:flex-row gap-3 justify-center max-w-lg mx-auto">
      <input
        id={inputId}
        type="email"
        value={email}
        onChange={e => setEmail(e.target.value)}
        placeholder="Enter your email"
        disabled={done}
        className={`flex-1 ghost-border px-5 py-4 text-sm outline-none transition-all ${inputClass} ${error ? 'border-[#ba1a1a]!' : ''}`}
        aria-label="Email address"
      />
      <button
        onClick={handleSubmit}
        disabled={done}
        className={`${btnClass || 'cta-gradient text-[#e2e2e2]'} px-7 py-4 text-xs font-black uppercase tracking-[0.18em] whitespace-nowrap cursor-pointer disabled:opacity-70`}
      >
        {done ? "You're on the list!" : 'Get Early Access'}
      </button>
    </div>
  )
}

export default function Home() {
  const [communityVal, setCommunityVal] = useState('')
  const [communityDone, setCommunityDone] = useState(false)

  const handleCommunity = async () => {
    if (!communityVal.trim()) return
    try {
      await fetch('https://api.sheetmonkey.io/form/cHsdnmiBFmbDHHmd2VA5eb', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          Request: communityVal.trim(),
          Type: 'Community Request',
          Created: 'x-sheetmonkey-current-date-time',
        }),
      })
    } catch (e) {
      console.error('Sheetmonkey error:', e)
    }
    setCommunityDone(true)
    setTimeout(() => { setCommunityDone(false); setCommunityVal('') }, 3000)
  }

  return (
    <>
      <SEO title="Home" url="/" />
      {/* Hero */}
      <section className="pt-48 pb-32 px-6 text-center max-w-screen-xl mx-auto">
        <div className="mb-5 fade-up" style={{ animationDelay: '0.1s' }}>
          <span className="font-label font-semibold uppercase tracking-[0.22em] text-[10px] text-[#474747]">VOX LOCAL — LOCAL AI SERIES 01</span>
        </div>
        <h1
          className="font-headline font-black text-6xl md:text-8xl tracking-[-0.03em] leading-[0.92] text-black mb-8 fade-up"
          style={{ animationDelay: '0.25s' }}
        >
          Your Personal AI<br />
          Voice Agent.<br />
          <span className="text-[#c6c6c6]">100% Local.</span><br />
          Lightning Fast.
        </h1>
        <p
          className="text-[#474747] text-lg md:text-xl max-w-2xl mx-auto leading-relaxed mb-12 fade-up"
          style={{ animationDelay: '0.4s' }}
        >
          Experience a privacy-first AI assistant that manages your files, reads your PDFs, and talks back to you in real-time—all without your data ever leaving your machine.
        </p>

        <div className="fade-up" style={{ animationDelay: '0.55s' }}>
          <EarlyAccessForm inputId="email-input" inputClass="bg-white text-[#1a1c1c] placeholder:text-[#c6c6c6]" />
          <p className="mt-4 text-[10px] text-[#777] uppercase tracking-widest">No cloud. No tracking. No subscription.</p>
        </div>

        <AIPulseLine className="mt-16 mb-20 max-w-xs mx-auto" />

        {/* Waveform */}
        <div className="flex items-end justify-center gap-1.5 mb-4 h-12" aria-hidden="true">
          {WAVE_HEIGHTS.map((h, i) => (
            <div key={i} className={`wave-bar ${h}`} style={{ animationDelay: `${WAVE_DELAYS[i]}s` }} />
          ))}
        </div>
        <p className="text-[10px] text-[#777] uppercase tracking-[0.3em]">Real-time local voice processing</p>
      </section>

      {/* Community Request */}
      <section className="pb-32 px-6">
        <div className="max-w-2xl mx-auto">
          <div className="bg-white ghost-border p-8">
            <p className="font-label font-semibold uppercase tracking-[0.18em] text-[10px] text-[#474747] mb-5">COMMUNITY REQUEST</p>
            <div className="flex items-center gap-3">
              <input
                type="text"
                value={communityDone ? '✓ Thanks for your suggestion!' : communityVal}
                onChange={e => setCommunityVal(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handleCommunity()}
                disabled={communityDone}
                placeholder="What is the #1 task you want a local AI voice assistant to do for you?"
                className="flex-1 bg-transparent outline-none text-sm text-[#474747] placeholder:text-[#c6c6c6]/60"
                aria-label="Community feature request"
              />
              <button onClick={handleCommunity} className="text-[#474747] hover:text-black transition-colors cursor-pointer" aria-label="Submit request">
                <span className="material-symbols-outlined" style={{ fontSize: '20px' }}>arrow_forward</span>
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Feature Cards */}
      <section className="pb-40 px-6" aria-labelledby="features-heading">
        <div className="max-w-screen-xl mx-auto">
          <h2 id="features-heading" className="sr-only">Core Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {features.map(f => (
              <div key={f.id} className="feature-card p-10 bg-[#f3f3f3]">
                <div className="w-10 h-10 bg-white ghost-border flex items-center justify-center mb-8">
                  <span className="material-symbols-outlined text-black" style={{ fontSize: '20px' }}>{f.icon}</span>
                </div>
                <h3 className="font-label font-bold text-[11px] uppercase tracking-widest mb-4">{f.title}</h3>
                <p className="text-sm text-[#474747] leading-relaxed">{f.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-32 px-6 bg-white" aria-labelledby="hiw-heading">
        <div className="max-w-screen-xl mx-auto">
          <div className="mb-20">
            <span className="font-label font-semibold uppercase tracking-[0.22em] text-[10px] text-[#474747]">Architecture</span>
            <h2 id="hiw-heading" className="font-headline font-black text-4xl md:text-5xl tracking-tight mt-3">How It Works</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-16 items-center">
            <div className="space-y-10">
              {[
                { num: '01', title: 'Speak Naturally', body: 'Your voice is captured and processed entirely on-device using a Whisper-class speech-to-text model. No audio ever leaves your machine.' },
                { num: '02', title: 'Local Brain Processes', body: 'An optimized local LLM (Gemma, Mistral, or Llama) processes your request, searches your files, and crafts a response—all on your GPU or CPU.' },
                { num: '03', title: 'Instant Voice Reply', body: 'A local text-to-speech engine responds using a natural voice. Near-zero latency. Sounds like a conversation, not a tool.' },
              ].map((step, i) => (
                <div key={step.num}>
                  <div className="flex gap-6">
                    <div className="font-label font-bold text-[10px] tracking-widest text-[#777] pt-1">{step.num}</div>
                    <div>
                      <h3 className="font-bold text-sm uppercase tracking-widest mb-3">{step.title}</h3>
                      <p className="text-[#474747] text-sm leading-relaxed">{step.body}</p>
                    </div>
                  </div>
                  {i < 2 && <AIPulseLine className="mt-8" />}
                </div>
              ))}
            </div>
            {/* Diagram */}
            <div className="bg-[#eeeeee] p-10 space-y-4">
              {[
                { icon: 'mic', label: 'Voice Input', sub: 'Whisper STT — On Device' },
                { icon: 'memory', label: 'Local LLM', sub: 'Gemma / Mistral / Llama — GPU', dark: true },
                { icon: 'record_voice_over', label: 'Voice Output', sub: 'Local TTS — Zero Latency' },
              ].map((row, i) => (
                <div key={row.label}>
                  <div className={`ghost-border p-5 flex items-center gap-4 ${row.dark ? 'bg-black text-[#e2e2e2]' : 'bg-white'}`}>
                    <span className={`material-symbols-outlined ${row.dark ? 'text-[#e2e2e2]' : 'text-black'}`} style={{ fontSize: '18px' }}>{row.icon}</span>
                    <div>
                      <p className={`text-[10px] font-bold uppercase tracking-widest`}>{row.label}</p>
                      <p className={`text-xs mt-1 ${row.dark ? 'text-[#e2e2e2]/70' : 'text-[#474747]'}`}>{row.sub}</p>
                    </div>
                  </div>
                  {i < 2 && (
                    <div className="flex justify-center py-1">
                      <span className="material-symbols-outlined text-[#c6c6c6]" style={{ fontSize: '16px' }}>arrow_downward</span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Capabilities */}
      <section className="py-32 px-6" aria-labelledby="cap-heading">
        <div className="max-w-screen-xl mx-auto">
          <div className="mb-20">
            <span className="font-label font-semibold uppercase tracking-[0.22em] text-[10px] text-[#474747]">What It Can Do</span>
            <h2 id="cap-heading" className="font-headline font-black text-4xl md:text-5xl tracking-tight mt-3">Built for Power Users</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {capabilities.map(c => (
              <div key={c.id} className="feature-card p-8 bg-[#f3f3f3]">
                <span className="material-symbols-outlined text-black mb-5" style={{ fontSize: '28px' }}>{c.icon}</span>
                <h3 className="font-bold text-sm uppercase tracking-widest mb-3">{c.title}</h3>
                <p className="text-sm text-[#474747] leading-relaxed">{c.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-32 px-6 bg-black text-[#e2e2e2] text-center" aria-labelledby="final-cta-heading">
        <div className="max-w-2xl mx-auto">
          <span className="font-label font-semibold uppercase tracking-[0.22em] text-[10px] text-[#e2e2e2]/50 mb-5 inline-block">Join the Decentralized Future</span>
          <h2 id="final-cta-heading" className="font-headline font-black text-4xl md:text-6xl tracking-tight mb-8">
            Own Your AI.<br />Own Your Data.
          </h2>
          <p className="text-[#e2e2e2]/70 text-lg leading-relaxed mb-12">
            VOX LOCAL is currently in early access. Be the first to experience intelligence without compromise.
          </p>
          <EarlyAccessForm
            inputId="email-input-footer"
            inputClass="bg-white/10 border-white/20 text-[#e2e2e2] placeholder:text-[#e2e2e2]/40 focus:border-white/60"
            btnClass="bg-[#e2e2e2] text-black hover:opacity-85 transition-opacity"
          />
        </div>
      </section>
    </>
  )
}
