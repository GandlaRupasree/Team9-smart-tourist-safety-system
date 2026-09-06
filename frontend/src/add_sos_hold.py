with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

def try_replace(content, old, new, label):
    if old in content:
        content = content.replace(old, new)
        print(f"OK: {label}")
    else:
        print(f"WARNING: {label} - anchor not found")
    return content

# 1. Add useRef to imports
old1 = "import { useState, useEffect } from 'react'"
new1 = "import { useState, useEffect, useRef } from 'react'"
content = try_replace(content, old1, new1, "useRef import")

# 2. Add hold-progress state right after sosError state
old2 = "  const [sosError, setSosError] = useState(null)"
new2 = """  const [sosError, setSosError] = useState(null)
  const [sosHoldProgress, setSosHoldProgress] = useState(0)
  const sosHoldTimerRef = useRef(null)"""
content = try_replace(content, old2, new2, "hold progress state")

# 3. Add hold start/end handlers right after triggerSOS's closing brace
old3 = """  const closeSosModal = () => {
    setSosOpen(false)
    setSosResult(null)
    setSosSituation('')
    setSosLocationNote('')
  }"""
new3 = """  const handleSosHoldStart = () => {
    if (sosLoading) return
    let progress = 0
    sosHoldTimerRef.current = setInterval(() => {
      progress += 100 / (3000 / 50)
      if (progress >= 100) {
        clearInterval(sosHoldTimerRef.current)
        sosHoldTimerRef.current = null
        setSosHoldProgress(0)
        triggerSOS()
        return
      }
      setSosHoldProgress(progress)
    }, 50)
  }

  const handleSosHoldEnd = () => {
    if (sosHoldTimerRef.current) {
      clearInterval(sosHoldTimerRef.current)
      sosHoldTimerRef.current = null
    }
    setSosHoldProgress(0)
  }

  const closeSosModal = () => {
    setSosOpen(false)
    setSosResult(null)
    setSosSituation('')
    setSosLocationNote('')
    handleSosHoldEnd()
  }"""
content = try_replace(content, old3, new3, "hold handlers")

# 4. Replace the click button with the press-and-hold button
old4 = """                  {sosError && <div className="status-message error">{sosError}</div>}
                  <button className="sos-send-btn" onClick={triggerSOS} disabled={sosLoading}>
                    {sosLoading ? "Sending Alert..." : "Send SOS Alert"}
                  </button>"""
new4 = """                  {sosError && <div className="status-message error">{sosError}</div>}
                  <div className="sos-hold-wrapper">
                    <button
                      className="sos-hold-btn"
                      onMouseDown={handleSosHoldStart}
                      onMouseUp={handleSosHoldEnd}
                      onMouseLeave={handleSosHoldEnd}
                      onTouchStart={handleSosHoldStart}
                      onTouchEnd={handleSosHoldEnd}
                      disabled={sosLoading}
                    >
                      <span className="sos-hold-fill" style={{ height: `${sosHoldProgress}%` }}></span>
                      <span className="sos-hold-label">{sosLoading ? "Sending..." : "SOS"}</span>
                    </button>
                    <p className="sos-hold-hint">Press and hold for 3 seconds to send an alert</p>
                  </div>"""
content = try_replace(content, old4, new4, "press-and-hold button")

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)
