import { useEffect, useState } from 'react'
import AIPulseLine from '../components/AIPulseLine'
import SEO from '../components/SEO'

const INITIAL_VOTES = [
  { id: 'notion',   icon: 'description',    name: 'Notion',             category: 'Productivity',     desc: 'Read and write Notion pages via voice',             votes: 312 },
  { id: 'obsidian', icon: 'edit_note',       name: 'Obsidian',           category: 'Knowledge Base',   desc: 'Search and create notes in your vault',             votes: 278 },
  { id: 'vscode',   icon: 'code',            name: 'VS Code',            category: 'Developer Tools',  desc: 'Write code and navigate repos with voice',          votes: 241 },
  { id: 'spotify',  icon: 'music_note',      name: 'Spotify / Local Music', category: 'Media',         desc: 'Control local playback and playlists',              votes: 198 },
  { id: 'calendar', icon: 'calendar_month',  name: 'Local Calendar',     category: 'Productivity',     desc: 'Schedule events and get reminders by voice',        votes: 167 },
  { id: 'browser',  icon: 'public',          name: 'Browser Control',    category: 'Automation',       desc: 'Open tabs, search, and navigate hands-free',        votes: 154 },
]

function VoteBoard() {
  const [items, setItems] = useState(INITIAL_VOTES)
  const [voted, setVoted] = useState(new Set())

  const handleVote = (id) => {
    if (voted.has(id)) return
    setVoted(prev => new Set(prev).add(id))
    setItems(prev =>
      [...prev.map(item => item.id === id ? { ...item, votes: item.votes + 1 } : item)]
        .sort((a, b) => b.votes - a.votes)
    )
  }

  const maxVotes = Math.max(...items.map(v => v.votes))

  return (
    <div className="space-y-3">
      {items.map((item, idx) => {
        const isVoted = voted.has(item.id)
        const pct = Math.round((item.votes / (maxVotes + 20)) * 100)
        return (
          <div
            key={item.id}
            className="bg-white ghost-border p-5 flex items-center gap-4 hover:bg-[#f3f3f3] transition-all"
          >
            <span className="font-label font-bold text-[10px] tracking-widest text-[#777] w-5">
              {String(idx + 1).padStart(2, '0')}
            </span>
            <span className="material-symbols-outlined text-black" style={{ fontSize: '18px' }}>{item.icon}</span>
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-3 mb-1">
                <p className="font-bold text-sm">{item.name}</p>
                <span className="text-[9px] font-semibold uppercase tracking-widest text-[#777] bg-[#eeeeee] px-2 py-0.5">
                  {item.category}
                </span>
              </div>
              <p className="text-xs text-[#474747]">{item.desc}</p>
              <div className="mt-2 h-0.5 bg-[#e8e8e8] overflow-hidden">
                <div
                  className="progress-bar h-full bg-black"
                  style={{ width: `${pct}%` }}
                />
              </div>
            </div>
            <button
              onClick={() => handleVote(item.id)}
              disabled={isVoted}
              className={`flex items-center gap-1.5 px-4 py-2 text-[10px] font-bold uppercase tracking-widest border transition-all cursor-pointer
                ${isVoted
                  ? 'bg-black text-[#e2e2e2] border-black'
                  : 'border-[rgba(198,198,198,0.4)] hover:border-black'
                }`}
              aria-label={`Vote for ${item.name}`}
            >
              {!isVoted && (
                <span className="material-symbols-outlined" style={{ fontSize: '13px' }}>keyboard_arrow_up</span>
              )}
              {item.votes}
            </button>
          </div>
        )
      })}
    </div>
  )
}

function SuggestionForm() {
  const [fields, setFields] = useState({ tool: '', type: '', useCase: '', email: '' })
  const [errors, setErrors] = useState({})
  const [submitted, setSubmitted] = useState(false)

  const set = (key) => (e) => setFields(f => ({ ...f, [key]: e.target.value }))

  const handleSubmit = (e) => {
    e.preventDefault()
    const errs = {}
    if (!fields.tool.trim())    errs.tool = true
    if (!fields.useCase.trim()) errs.useCase = true
    if (Object.keys(errs).length) { setErrors(errs); return }
    setSubmitted(true)
  }

  if (submitted) {
    return (
      <div className="bg-[#f3f3f3] p-10 text-center">
        <span className="material-symbols-outlined text-black mb-4" style={{ fontSize: '32px' }}>check_circle</span>
        <p className="font-bold text-sm uppercase tracking-widest mb-2">Suggestion received.</p>
        <p className="text-[#474747] text-xs">We review every submission. The most-voted integrations enter our next sprint.</p>
      </div>
    )
  }

  const inputBase = 'w-full bg-white ghost-border px-5 py-4 text-sm text-[#1a1c1c] placeholder:text-[#c6c6c6]/70 outline-none transition-all focus:border-black'
  const errBorder = 'border-[#ba1a1a]!'

  return (
    <form onSubmit={handleSubmit} noValidate className="space-y-8">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="space-y-2">
          <label htmlFor="tool-name" className="block text-[10px] font-semibold uppercase tracking-widest text-[#474747]">
            Tool or App Name
          </label>
          <input
            id="tool-name"
            type="text"
            value={fields.tool}
            onChange={set('tool')}
            placeholder="e.g. Notion, Slack, Obsidian"
            className={`${inputBase} ${errors.tool ? errBorder : ''}`}
          />
        </div>
        <div className="space-y-2">
          <label htmlFor="integration-type" className="block text-[10px] font-semibold uppercase tracking-widest text-[#474747]">
            Integration Type
          </label>
          <div className="relative">
            <select
              id="integration-type"
              value={fields.type}
              onChange={set('type')}
              className={`${inputBase} appearance-none`}
            >
              <option value="">Select a category</option>
              <option value="productivity">Productivity</option>
              <option value="file-management">File Management</option>
              <option value="communication">Communication</option>
              <option value="creative">Creative</option>
              <option value="developer">Developer Tools</option>
              <option value="other">Other</option>
            </select>
            <div className="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none">
              <span className="material-symbols-outlined text-[#777]" style={{ fontSize: '18px' }}>expand_more</span>
            </div>
          </div>
        </div>
      </div>

      <div className="space-y-2">
        <label htmlFor="use-case" className="block text-[10px] font-semibold uppercase tracking-widest text-[#474747]">
          How would you use this integration?
        </label>
        <textarea
          id="use-case"
          rows={5}
          value={fields.useCase}
          onChange={set('useCase')}
          placeholder="Describe your ideal workflow — e.g. 'I want to ask my assistant to create a new Notion page from my voice notes...'"
          className={`${inputBase} resize-none ${errors.useCase ? errBorder : ''}`}
        />
      </div>

      <div className="space-y-2">
        <label htmlFor="your-email" className="block text-[10px] font-semibold uppercase tracking-widest text-[#474747]">
          Your Email{' '}
          <span className="normal-case tracking-normal font-normal text-[#777]">(optional — get notified when it ships)</span>
        </label>
        <input
          id="your-email"
          type="email"
          value={fields.email}
          onChange={set('email')}
          placeholder="you@domain.com"
          className={inputBase}
        />
      </div>

      <div className="pt-4 flex flex-col items-center">
        <button
          type="submit"
          className="w-full md:w-auto md:min-w-[280px] cta-gradient text-[#e2e2e2] py-5 px-10 text-xs font-black uppercase tracking-[0.2em] cursor-pointer"
        >
          Submit Suggestion
        </button>
        <p className="mt-6 text-[10px] text-[#777] uppercase tracking-widest">
          Local-first. Privacy-focused. Community-driven.
        </p>
      </div>
    </form>
  )
}

const PRINCIPLES = [
  { icon: 'verified_user', title: 'Privacy Preserved', body: 'All suggested integrations must adhere to our local-first, zero-knowledge architectural standards.' },
  { icon: 'terminal',      title: 'Open Protocol',     body: 'We prioritize tools that offer robust APIs or local file access to ensure permanent user ownership.' },
  { icon: 'bolt',          title: 'Rapid Development', body: 'The most requested tools enter our 2-week sprint cycle for immediate architectural vetting.' },
]

export default function Integrations() {
  useEffect(() => { window.scrollTo(0, 0) }, [])

  return (
    <div className="pt-40 pb-24 px-6">
      <SEO title="Integrations" description="Suggest an integration or tool you want to see working with your local voice agent." url="/integrations" />
      <div className="max-w-3xl mx-auto">

        {/* Header */}
        <header className="text-center mb-20">
          <div className="inline-block mb-6 px-3 py-1.5 bg-[#eeeeee] text-[10px] font-bold uppercase tracking-[0.22em] fade-up">
            VOX LOCAL ECOSYSTEM
          </div>
          <h1 className="text-5xl md:text-7xl font-black tracking-[-0.03em] text-black mb-8 leading-[1.05] fade-up" style={{ animationDelay: '0.15s' }}>
            Help Us Build the<br />Future of Local AI
          </h1>
          <p className="text-[#474747] text-lg md:text-xl max-w-xl mx-auto font-medium leading-relaxed fade-up" style={{ animationDelay: '0.3s' }}>
            Suggest an integration or tool you want to see working with your local voice agent.
            We ship the most-requested ones first.
          </p>
        </header>

        <AIPulseLine className="mb-16" />

        {/* Suggestion Form */}
        <section className="mb-20" aria-labelledby="form-heading">
          <h2 id="form-heading" className="font-label font-semibold uppercase tracking-[0.18em] text-[10px] text-[#474747] mb-8">
            Submit a Suggestion
          </h2>
          <SuggestionForm />
        </section>

        <AIPulseLine className="mb-16" />

        {/* Community Voting */}
        <section className="mb-20" aria-labelledby="vote-heading">
          <div className="flex items-end justify-between mb-8">
            <div>
              <h2 id="vote-heading" className="font-label font-semibold uppercase tracking-[0.18em] text-[10px] text-[#474747]">
                Top Community Requests
              </h2>
              <p className="text-sm text-[#474747] mt-1">Vote for the integrations you need most.</p>
            </div>
            <span className="font-label font-semibold uppercase tracking-widest text-[10px] text-[#777]">Updated Weekly</span>
          </div>
          <VoteBoard />
        </section>

        <AIPulseLine className="mb-16" />

        {/* Principles */}
        <section aria-labelledby="principles-heading" className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <h2 id="principles-heading" className="sr-only">Our Integration Principles</h2>
          {PRINCIPLES.map(({ icon, title, body }) => (
            <div key={title} className="feature-card p-8 bg-[#f3f3f3]">
              <span className="material-symbols-outlined text-black mb-5" style={{ fontSize: '28px' }}>{icon}</span>
              <h3 className="text-[11px] font-bold uppercase tracking-widest mb-3">{title}</h3>
              <p className="text-sm text-[#474747] leading-relaxed">{body}</p>
            </div>
          ))}
        </section>

      </div>
    </div>
  )
}
