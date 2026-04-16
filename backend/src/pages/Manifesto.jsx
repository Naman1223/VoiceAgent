import { useEffect, useRef } from 'react'
import { Link } from 'react-router-dom'
import AIPulseLine from '../components/AIPulseLine'
import SEO from '../components/SEO'

function ScrollSection({ children, className = '' }) {
  const ref = useRef(null)
  useEffect(() => {
    const el = ref.current
    if (!el) return
    const obs = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) el.classList.add('visible') },
      { threshold: 0.1 }
    )
    obs.observe(el)
    return () => obs.disconnect()
  }, [])
  return (
    <section ref={ref} className={`scroll-section ${className}`}>
      {children}
    </section>
  )
}

export default function Manifesto() {
  useEffect(() => { window.scrollTo(0, 0) }, [])

  return (
    <div className="pt-36 pb-24 px-6">
      <SEO title="Manifesto" description="The Local-First Manifesto. Computation is a private act. The future of artificial intelligence is not in the cloud—it is in your hands." url="/manifesto" />
      <article className="max-w-[700px] mx-auto">

        {/* Header */}
        <header className="mb-24">
          <div className="mb-4">
            <span className="font-label font-semibold uppercase tracking-[0.2em] text-[10px] text-[#474747]">
              VOX LOCAL SERIES 01
            </span>
          </div>
          <h1 className="font-headline font-black text-6xl md:text-8xl tracking-[-0.03em] leading-[0.9] text-black mb-8">
            The Local-First<br />Manifesto
          </h1>
          <div className="h-1 w-24 bg-black mb-12" />
          <p className="text-xl md:text-2xl font-medium text-[#474747] leading-relaxed italic">
            Computation is a private act. The future of artificial intelligence is not in the cloud—it is in your hands.
          </p>
        </header>

        <AIPulseLine className="mb-24" />

        {/* Section 1: Privacy */}
        <ScrollSection className="mb-32">
          <div className="flex items-center gap-4 mb-6">
            <span className="material-symbols-outlined text-black">lock</span>
            <h2 className="font-headline font-bold text-2xl uppercase tracking-tight">Privacy as a Human Right</h2>
          </div>
          <div className="space-y-6 text-[#474747] leading-8 text-lg">
            <p>
              In the current digital landscape, every interaction with an AI agent is a transaction of personal data.
              When your voice and thoughts are processed in the cloud, you are no longer the user; you are the training data.
            </p>
            <p>
              <span className="text-black font-bold">VOX LOCAL</span> rejects the centralized surveillance model. We believe that privacy is not a feature—it is
              a foundational requirement for trust. By ensuring that your data never leaves your physical machine, we
              eliminate the risk of server-side breaches, corporate harvesting, and unauthorized surveillance.
            </p>
            <div className="bg-[#eeeeee] p-8 border-l-4 border-black mt-8">
              <p className="font-medium text-[#1a1c1c] italic">
                "The only data that is truly secure is the data that never leaves its source."
              </p>
            </div>
          </div>
        </ScrollSection>

        <AIPulseLine className="mb-32" />

        {/* Section 2: Speed */}
        <ScrollSection className="mb-32">
          <div className="flex items-center gap-4 mb-6">
            <span className="material-symbols-outlined text-black">bolt</span>
            <h2 className="font-headline font-bold text-2xl uppercase tracking-tight">Speed is Sovereignty</h2>
          </div>
          <div className="space-y-6 text-[#474747] leading-8 text-lg">
            <p>
              Latency is the enemy of thought. Every millisecond spent waiting for a packet to return from a data center
              is a micro-interruption in your cognitive flow.
            </p>
            <p>
              Local processing operates at the speed of silicon. By running optimized models directly on your hardware,
              VOX LOCAL provides a near-zero latency response. This makes the AI feel less like a tool and more like an
              extension of your own mind.
            </p>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8">
              {[
                { stat: '<50ms', label: 'Response Time' },
                { stat: '0', label: 'API Calls' },
                { stat: '100%', label: 'Local' },
                { stat: '∞', label: 'Offline Use' },
              ].map(({ stat, label }) => (
                <div key={label} className="bg-[#f3f3f3] p-5 text-center">
                  <p className="font-black text-3xl tracking-tighter">{stat}</p>
                  <p className="text-[10px] font-semibold uppercase tracking-widest text-[#474747] mt-2">{label}</p>
                </div>
              ))}
            </div>
          </div>
        </ScrollSection>

        <AIPulseLine className="mb-32" />

        {/* Section 3: Ownership */}
        <ScrollSection className="mb-32">
          <div className="flex items-center gap-4 mb-6">
            <span className="material-symbols-outlined text-black">folder_shared</span>
            <h2 className="font-headline font-bold text-2xl uppercase tracking-tight">Total Data Ownership</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            {[
              { title: 'Your Models', body: 'Fine-tuned weights stay on your drive. You choose how your agent evolves.' },
              { title: 'Your Logs', body: 'History is yours to clear, encrypt, or store offline. We have no access.' },
              { title: 'Your Conversations', body: 'Every dialogue is stored in a local encrypted vector store. Full delete, anytime.' },
              { title: 'Your Identity', body: 'No account required. No email. No tracking pixel. You are anonymous by design.' },
            ].map(({ title, body }) => (
              <div key={title} className="bg-[#f3f3f3] p-6">
                <h3 className="font-bold text-sm uppercase tracking-widest mb-3">{title}</h3>
                <p className="text-sm text-[#474747] leading-relaxed">{body}</p>
              </div>
            ))}
          </div>
          <p className="text-[#474747] leading-8 text-lg">
            Ownership is not partial. You own the software, you own the weights, and you own the output.
            In a world of "AI-as-a-Service," we provide "AI-as-a-Utility."
          </p>
        </ScrollSection>

        <AIPulseLine className="mb-32" />

        {/* Section 4: Technical Edge */}
        <ScrollSection className="mb-32">
          <div className="flex items-center gap-4 mb-6">
            <span className="material-symbols-outlined text-black">memory</span>
            <h2 className="font-headline font-bold text-2xl uppercase tracking-tight">The Technical Edge</h2>
          </div>
          <p className="text-[#474747] leading-8 text-lg mb-12">
            The hardware in your pocket and on your desk has reached a critical tipping point. Modern GPUs and dedicated
            Neural Processing Units (NPUs) are now capable of running state-of-the-art language models with incredible
            efficiency. We leverage this dormant power to bring high-performance intelligence to your local environment,
            requiring no external API calls and no subscription fees.
          </p>
          {/* Hardware Visual */}
          <div className="aspect-video bg-[#e2e2e2] flex items-center justify-center overflow-hidden relative">
            <div className="z-10 text-center px-12">
              <span className="font-label font-bold text-[10px] tracking-[0.4em] uppercase opacity-40">
                Local Hardware Execution
              </span>
              <div className="mt-8 flex gap-3 justify-center items-end h-16">
                {[40, 60, 50, 80, 100, 70, 55, 40].map((h, i) => (
                  <div key={i} className="w-1.5 bg-black" style={{ height: `${h}%`, opacity: h / 100 }} />
                ))}
              </div>
              <p className="mt-6 text-[10px] font-semibold uppercase tracking-widest text-[#474747]">GPU / NPU — Your Machine</p>
            </div>
          </div>
        </ScrollSection>

        {/* Article footer CTA */}
        <footer className="mt-40 pt-12 border-t border-[rgba(198,198,198,0.2)] text-center">
          <p className="font-headline font-bold text-xl mb-2">Join the Decentralized Future.</p>
          <p className="text-[#474747] text-sm mb-8">Run your AI. Keep your data. Own your intelligence.</p>
          <Link to="/">
            <button className="cta-gradient text-[#e2e2e2] px-12 py-4 text-xs font-bold uppercase tracking-[0.2em] cursor-pointer">
              Get Early Access
            </button>
          </Link>
        </footer>

      </article>
    </div>
  )
}
