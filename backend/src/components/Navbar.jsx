import { NavLink } from 'react-router-dom'

export default function Navbar() {
  return (
    <nav className="fixed top-0 w-full z-50 glass-header">
      <div className="flex justify-between items-center w-full px-8 py-6 max-w-screen-xl mx-auto">
        {/* Logo */}
        <NavLink to="/" className="text-xl font-black tracking-tighter text-black uppercase no-underline">
          VOX LOCAL
        </NavLink>

        {/* Links */}
        <div className="hidden md:flex items-center gap-8">
          <NavLink
            to="/"
            end
            className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}
          >
            Home
          </NavLink>
          <NavLink
            to="/manifesto"
            className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}
          >
            Manifesto
          </NavLink>
          <NavLink
            to="/integrations"
            className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}
          >
            Integrations
          </NavLink>
          <NavLink
            to="/privacy-policy"
            className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}
          >
            Privacy Policy
          </NavLink>
          <a href="#faq" className="nav-link">FAQ</a>
        </div>

        {/* CTA */}
        <button
          className="cta-gradient text-[#e2e2e2] px-6 py-2.5 text-[11px] font-black uppercase tracking-widest cursor-pointer"
          onClick={() => {
            const el = document.getElementById('email-input')
            if (el) {
              el.scrollIntoView({ behavior: 'smooth' })
              setTimeout(() => el.focus(), 500)
            }
          }}
        >
          Get Early Access
        </button>
      </div>
    </nav>
  )
}
