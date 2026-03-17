import React from 'react'
import Navbar from './components/Navbar'
import HeroSection from './components/HeroSection'

export default function App() {
  return (
    <div className="min-h-screen bg-black font-sans">
      <Navbar />
      <HeroSection />
    </div>
  )
}
