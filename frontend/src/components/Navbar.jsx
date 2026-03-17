import React from 'react'
import { motion } from 'framer-motion'

// Nav link component
const NavLink = ({ children }) => (
  <a
    href="#"
    className="text-sm text-white/60 hover:text-white transition-colors duration-200 cursor-pointer"
  >
    {children}
  </a>
)

export default function Navbar() {
  return (
    <motion.nav
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: 'easeOut' }}
      className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-8 py-4"
      style={{
        background: 'rgba(0,0,0,0.45)',
        backdropFilter: 'blur(20px)',
        WebkitBackdropFilter: 'blur(20px)',
        borderBottom: '1px solid rgba(255,255,255,0.07)',
      }}
    >
      {/* Logo */}
      <div className="flex items-center gap-2">
        {/* Synapse icon mark */}
        <div className="w-7 h-7 rounded-lg flex items-center justify-center"
          style={{ background: 'linear-gradient(135deg, #ffffff22, #ffffff08)', border: '1px solid rgba(255,255,255,0.15)' }}>
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="7" cy="7" r="2.5" fill="white" />
            <circle cx="7" cy="7" r="5.5" stroke="white" strokeWidth="1" strokeDasharray="2 2" />
          </svg>
        </div>
        <span className="font-medium tracking-tight text-white text-base select-none">
          Synapse
        </span>
      </div>

      {/* Center nav links */}
      <div className="hidden md:flex items-center gap-8">
        <NavLink>Product</NavLink>
        <NavLink>Solutions</NavLink>
        <NavLink>Pricing</NavLink>
        <NavLink>Docs</NavLink>
      </div>

      {/* CTA */}
      <motion.button
        whileHover={{ scale: 1.04 }}
        whileTap={{ scale: 0.97 }}
        id="nav-cta-voice-agent"
        className="btn-voice-agent px-4 py-2 rounded-full text-sm font-semibold transition-all duration-200 shadow-lg shadow-white/10"
        style={{
          background: 'linear-gradient(135deg, #ffffff 0%, #d0d0d0 60%, #909090 100%)',
          color: '#000',
        }}
      >
        Voice Agent
      </motion.button>
    </motion.nav>
  )
}
