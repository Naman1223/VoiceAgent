/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      fontSize: {
        'hero': ['80px', { lineHeight: '1.05', letterSpacing: '-0.04em' }],
        'hero-sm': ['52px', { lineHeight: '1.1', letterSpacing: '-0.03em' }],
      },
      colors: {
        'glass-white': 'rgba(255,255,255,0.06)',
        'glass-border': 'rgba(255,255,255,0.10)',
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [],
}
