import React, { useEffect, useRef, memo } from 'react'
import Hls from 'hls.js'

/**
 * Memoized VideoPlayer component.
 * Covers the FULL section with object-fit: cover — no black bars.
 * Auto-detects .m3u8 → hls.js, else native <video>.
 * Proper cleanup on unmount.
 */
const VideoPlayer = memo(function VideoPlayer({ src }) {
  const videoRef = useRef(null)
  const hlsRef = useRef(null)

  useEffect(() => {
    const video = videoRef.current
    if (!video || !src) return

    const isHLS = src.includes('.m3u8')

    if (isHLS) {
      if (Hls.isSupported()) {
        const hls = new Hls({ enableWorker: true, lowLatencyMode: true })
        hlsRef.current = hls
        hls.loadSource(src)
        hls.attachMedia(video)
        hls.on(Hls.Events.MANIFEST_PARSED, () => {
          video.play().catch(() => {})
        })
      } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
        video.src = src
      }
    } else {
      video.src = src
      video.play().catch(() => {})
    }

    return () => {
      if (hlsRef.current) {
        hlsRef.current.destroy()
        hlsRef.current = null
      }
    }
  }, [src])

  return (
    /* Covers the entire parent absolutely — no black bars */
    <div className="absolute inset-0 z-0 pointer-events-none overflow-hidden">
      <video
        ref={videoRef}
        autoPlay
        muted
        loop
        playsInline
        className="w-full h-full object-cover"
        style={{ opacity: 1 }}
      />
      {/* Watermark cover — hides bottom-right logo baked into the video */}
      <div
        className="absolute bottom-0 right-0"
        style={{
          width: 180,
          height: 60,
          background: 'linear-gradient(to top left, #000 30%, transparent)',
          zIndex: 1,
        }}
      />
    </div>
  )
})

export default VideoPlayer
