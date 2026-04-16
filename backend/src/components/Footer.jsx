import { Link } from 'react-router-dom'

export default function Footer() {
  return (
    <footer className="w-full border-t border-[rgba(198,198,198,0.2)] bg-[#f9f9f9]">
      <div className="flex flex-col md:flex-row justify-between items-center w-full px-8 py-12 max-w-screen-xl mx-auto gap-4">
        <Link to="/" className="text-lg font-black text-black uppercase tracking-tighter no-underline">
          VOX LOCAL
        </Link>
        <div className="font-label font-medium uppercase text-[10px] tracking-widest text-neutral-500">
          © 2024 VOX LOCAL. NO CLOUD. NO TRACKING.
        </div>
        <div className="flex gap-6">
          <Link className="font-label font-medium uppercase text-[10px] tracking-widest text-neutral-500 hover:text-black transition-all no-underline" to="/privacy-policy">Privacy Policy</Link>
          <Link className="font-label font-medium uppercase text-[10px] tracking-widest text-neutral-500 hover:text-black transition-all no-underline" to="/integrations">Integrations</Link>
        </div>
      </div>
    </footer>
  )
}
