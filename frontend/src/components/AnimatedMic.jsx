import React from 'react'
import { motion } from 'framer-motion'

/**
 * AnimatedMic — pulsing microphone orb for the hero center.
 * Three concentric rings animate outward on loop.
 * The center button can be wired to a click handler for recording.
 */
export default function AnimatedMic({ onClick, isActive = false }) {
  const ringVariants = {
    animate: (i) => ({
      scale: [1, 1.6 + i * 0.3],
      opacity: [0.35, 0],
      transition: {
        duration: 2.2,
        delay: i * 0.55,
        repeat: Infinity,
        ease: 'easeOut',
      },
    }),
  }

  return (
    <div className="flex flex-col items-center gap-6">
      {/* Mic orb with pulse rings */}
      <div className="relative flex items-center justify-center">
        {/* Pulse rings */}
        {[0, 1, 2].map((i) => (
          <motion.div
            key={i}
            custom={i}
            variants={ringVariants}
            animate="animate"
            className="absolute rounded-full"
            style={{
              width: 84,
              height: 84,
              background: isActive
                ? 'radial-gradient(circle, rgba(99,102,241,0.4), rgba(99,102,241,0))'
                : 'radial-gradient(circle, rgba(255,255,255,0.3), rgba(255,255,255,0))',
              border: isActive
                ? '1px solid rgba(99,102,241,0.5)'
                : '1px solid rgba(255,255,255,0.25)',
            }}
          />
        ))}

        {/* Core mic button */}
        <motion.button
          id="hero-animated-mic"
          onClick={onClick}
          whileHover={{ scale: 1.08 }}
          whileTap={{ scale: 0.93 }}
          className="relative z-10 flex items-center justify-center rounded-full cursor-pointer focus:outline-none"
          style={{
            width: 84,
            height: 84,
            background: isActive
              ? 'linear-gradient(135deg, #6366f1, #4f46e5)'
              : 'rgba(255,255,255,0.10)',
            backdropFilter: 'blur(14px)',
            WebkitBackdropFilter: 'blur(14px)',
            border: isActive
              ? '1.5px solid rgba(129,140,248,0.7)'
              : '1.5px solid rgba(255,255,255,0.28)',
            boxShadow: isActive
              ? '0 0 40px rgba(99,102,241,0.5), inset 0 0 20px rgba(99,102,241,0.1)'
              : '0 0 32px rgba(255,255,255,0.08), inset 0 0 16px rgba(255,255,255,0.04)',
          }}
        >
          <svg
            width="28"
            height="28"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className="text-white"
          >
            <path
              d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d="M19 10v2a7 7 0 0 1-14 0v-2M12 19v4M8 23h8"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </motion.button>
      </div>

      <p className="text-white/40 text-xs tracking-widest uppercase font-medium">
        {isActive ? 'Listening…' : 'Tap to speak'}
      </p>
    </div>
  )
}
