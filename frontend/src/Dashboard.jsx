import { useState } from 'react'
import {
  LayoutDashboard, Compass, MapPin, ListChecks, TrendingUp, ShieldCheck,
  Navigation, PhoneCall, FileWarning, MessageCircle, Bell, Calendar,
  User, Settings, HelpCircle, LogOut, ChevronRight, Sun, Users, Car
} from 'lucide-react'
import './Dashboard.css'

const NAV_ITEMS = [
  { label: 'Dashboard', icon: LayoutDashboard },
  { label: 'Explore Places', icon: Compass },
  { label: 'Plan Your Trip', icon: MapPin },
  { label: 'My Itinerary', icon: ListChecks },
  { label: 'Crowd Prediction', icon: TrendingUp },
  { label: 'Safety Zones', icon: ShieldCheck },
  { label: 'Live Tracking', icon: Navigation },
  { label: 'SOS Assistance', icon: PhoneCall },
  { label: 'Report Incident', icon: FileWarning },
  { label: 'Smart Assistant', icon: MessageCircle },
  { label: 'Alerts & Notifications', icon: Bell, badge: 2 },
  { label: 'My Bookings', icon: Calendar },
]

const FOOTER_NAV_ITEMS = [
  { label: 'Profile', icon: User },
  { label: 'Settings', icon: Settings },
  { label: 'Help & Support', icon: HelpCircle },
  { label: 'Logout', icon: LogOut },
]

const POPULAR_DESTINATIONS = [
  { name: 'Mysore Palace', category: 'Historical', rating: 4.7, distance: '2.1 km away', safety: 92, crowd: 'Moderate' },
  { name: 'Brindavan Gardens', category: 'Nature', rating: 4.6, distance: '12.3 km away', safety: 88, crowd: 'Low' },
  { name: 'Chamundi Hills', category: 'Religious', rating: 4.6, distance: '13.7 km away', safety: 90, crowd: 'Moderate' },
  { name: 'Karanji Lake', category: 'Nature', rating: 4.4, distance: '3.4 km away', safety: 85, crowd: 'Low' },
]

const ITINERARY_STOPS = [
  { time: '08:00 AM', name: 'Mysore Palace', meta: '2.1 km', crowd: 'Low Crowd', crowdLevel: 'low' },
  { time: '10:00 AM', name: 'Chamundi Hills', meta: '13.7 km', crowd: 'Moderate Crowd', crowdLevel: 'moderate' },
  { time: '01:00 PM', name: 'Brindavan Gardens', meta: '13.3 km', crowd: 'Moderate Crowd', crowdLevel: 'moderate' },
  { time: '05:00 PM', name: "St. Philomena's Church", meta: '3.4 km', crowd: 'Low Crowd', crowdLevel: 'low' },
]

const CROWD_POINTS = [12, 18, 22, 35, 48, 60, 52, 40, 30, 20]
const CROWD_LABELS = ['6AM', '8AM', '10AM', '12PM', '2PM', '4PM', '6PM', '8PM']

const SAFETY_ALERTS = [
  { level: 'caution', title: 'Heavy traffic expected near Mysore Palace', time: 'Today, 10:00 AM' },
  { level: 'info', title: 'Weather is clear in your area', time: 'Today, 09:30 AM' },
  { level: 'high', title: 'Avoid restricted area due to an event', time: 'Today, 08:45 AM' },
]

function CrowdChart() {
  const width = 320
  const height = 120
  const max = Math.max(...CROWD_POINTS)
  const stepX = width / (CROWD_POINTS.length - 1)

  const points = CROWD_POINTS.map((val, i) => {
    const x = i * stepX
    const y = height - (val / max) * (height - 20) - 10
    return `${x},${y}`
  }).join(' ')

  const areaPoints = `0,${height} ${points} ${width},${height}`

  return (
    <svg viewBox={`0 0 ${width} ${height}`} className="crowd-chart-svg">
      <defs>
        <linearGradient id="crowdFill" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#14b8a6" stopOpacity="0.35" />
          <stop offset="100%" stopColor="#14b8a6" stopOpacity="0" />
        </linearGradient>
      </defs>
      <polygon points={areaPoints} fill="url(#crowdFill)" />
      <polyline points={points} fill="none" stroke="#0d9488" strokeWidth="2.5" strokeLinejoin="round" strokeLinecap="round" />
    </svg>
  )
}

export default function Dashboard() {
  const [activeNav, setActiveNav] = useState('Dashboard')

  return (
    <div className="dash-shell">
      <aside className="dash-sidebar">
        <div className="dash-brand">
          <div className="dash-brand-icon">TS</div>
          <span>TourSafe</span>
        </div>

        <nav className="dash-nav">
          {NAV_ITEMS.map(({ label, icon: Icon, badge }) => (
            <button
              key={label}
              className={`dash-nav-item ${activeNav === label ? 'dash-nav-item-active' : ''}`}
              onClick={() => setActiveNav(label)}
            >
              <Icon size={18} />
              <span>{label}</span>
              {badge && <span className="dash-nav-badge">{badge}</span>}
            </button>
          ))}
        </nav>

        <div className="dash-nav dash-nav-footer">
          {FOOTER_NAV_ITEMS.map(({ label, icon: Icon }) => (
            <button key={label} className="dash-nav-item">
              <Icon size={18} />
              <span>{label}</span>
            </button>
          ))}
        </div>

        <div className="dash-sidebar-cta">
          <p>Travel Safe, Explore More</p>
          <span>AI-powered safety insights on every trip</span>
        </div>
      </aside>

      <main className="dash-main">
        <div className="dash-status-row">
          <div className="dash-status-card dash-status-safe">
            <div className="dash-status-icon"><ShieldCheck size={20} /></div>
            <div className="dash-status-body">
              <span className="dash-status-label">Safety Status</span>
              <strong>Safe</strong>
              <p>You are currently in a safe zone</p>
              <a href="#">View Details <ChevronRight size={14} /></a>
            </div>
          </div>

          <div className="dash-status-card dash-status-crowd">
            <div className="dash-status-icon"><Users size={20} /></div>
            <div className="dash-status-body">
              <span className="dash-status-label">Crowd Level</span>
              <strong>Moderate</strong>
              <p>At your selected destination</p>
              <a href="#">View Prediction <ChevronRight size={14} /></a>
            </div>
          </div>

          <div className="dash-status-card dash-status-weather">
            <div className="dash-status-icon"><Sun size={20} /></div>
            <div className="dash-status-body">
              <span className="dash-status-label">Weather</span>
              <strong>26°C</strong>
              <p>Partly Cloudy</p>
              <a href="#">View Forecast <ChevronRight size={14} /></a>
            </div>
          </div>

          <div className="dash-status-card dash-status-emergency">
            <div className="dash-status-icon"><PhoneCall size={20} /></div>
            <div className="dash-status-body">
              <span className="dash-status-label">Emergency</span>
              <strong>SOS</strong>
              <p>Need help? We are here for you</p>
              <a href="#">Send SOS <ChevronRight size={14} /></a>
            </div>
          </div>
        </div>

        <div className="dash-grid-2">
          <section className="dash-panel">
            <div className="dash-panel-header">
              <h2>Popular Destinations</h2>
              <a href="#">View All</a>
            </div>
            <div className="dash-destinations-row">
              {POPULAR_DESTINATIONS.map((d) => (
                <div key={d.name} className="dash-dest-card">
                  <div className="dash-dest-thumb" style={{ background: `linear-gradient(135deg, #14b8a6, #0f766e)` }}>
                    <span>{d.category}</span>
                  </div>
                  <div className="dash-dest-body">
                    <h4>{d.name}</h4>
                    <div className="dash-dest-meta">
                      <span className="dash-dest-rating">★ {d.rating}</span>
                      <span>{d.distance}</span>
                    </div>
                    <div className="dash-dest-tags">
                      <span className="dash-tag dash-tag-safe">Safety {d.safety}/100</span>
                      <span className={`dash-tag ${d.crowd === 'Low' ? 'dash-tag-low' : 'dash-tag-moderate'}`}>{d.crowd}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </section>

          <section className="dash-panel">
            <div className="dash-panel-header">
              <h2>Live Map &amp; Safety Zones</h2>
              <div className="dash-legend">
                <span><i className="dash-dot dash-dot-safe"></i>Safe</span>
                <span><i className="dash-dot dash-dot-caution"></i>Caution</span>
                <span><i className="dash-dot dash-dot-danger"></i>Danger</span>
              </div>
            </div>
            <div className="dash-map-placeholder">
              <div className="dash-map-zone dash-map-zone-safe" style={{ top: '38%', left: '30%' }}></div>
              <div className="dash-map-zone dash-map-zone-caution" style={{ top: '22%', left: '68%' }}></div>
              <div className="dash-map-zone dash-map-zone-danger" style={{ top: '62%', left: '72%' }}></div>
              <div className="dash-map-pin" style={{ top: '42%', left: '34%' }}></div>
            </div>
            <div className="dash-map-footer">
              <ShieldCheck size={16} />
              <div>
                <strong>You are in a Safe Zone</strong>
                <span>Mysore Palace Area</span>
              </div>
              <a href="#">View Full Map</a>
            </div>
          </section>
        </div>

        <div className="dash-grid-2">
          <section className="dash-panel">
            <div className="dash-panel-header">
              <h2>Today's Itinerary</h2>
              <a href="#">View Full Itinerary</a>
            </div>
            <div className="dash-timeline">
              {ITINERARY_STOPS.map((stop, i) => (
                <div key={i} className="dash-timeline-item">
                  <div className="dash-timeline-time">{stop.time}</div>
                  <div className={`dash-timeline-dot dash-timeline-dot-${stop.crowdLevel}`}></div>
                  <div className="dash-timeline-body">
                    <strong>{stop.name}</strong>
                    <span>{stop.meta} &middot; <em className={`dash-crowd-${stop.crowdLevel}`}>{stop.crowd}</em></span>
                  </div>
                </div>
              ))}
            </div>
            <div className="dash-timeline-summary">
              <span><ListChecks size={14} /> 4</span>
              <span><MapPin size={14} /> 31.5 km</span>
              <span>7.5 hrs</span>
              <span><Car size={14} /> Car</span>
            </div>
          </section>

          <section className="dash-panel">
            <div className="dash-panel-header">
              <h2>Crowd Prediction (Today)</h2>
              <a href="#">View Calendar</a>
            </div>
            <div className="dash-chart-wrap">
              <CrowdChart />
              <div className="dash-chart-labels">
                {CROWD_LABELS.map(l => <span key={l}>{l}</span>)}
              </div>
            </div>
            <div className="dash-chart-footer">
              <div>
                <span className="dash-chart-footer-label">Crowd Level</span>
                <strong>Moderate 52%</strong>
              </div>
              <div>
                <span className="dash-chart-footer-label">Recommended Time</span>
                <strong>9:00 - 11:00 AM</strong>
              </div>
            </div>
          </section>
        </div>

        <section className="dash-panel">
          <div className="dash-panel-header">
            <h2>Safety Alerts</h2>
            <a href="#">View All</a>
          </div>
          <div className="dash-alerts-list">
            {SAFETY_ALERTS.map((a, i) => (
              <div key={i} className={`dash-alert-item dash-alert-${a.level}`}>
                <div className="dash-alert-icon">
                  {a.level === 'high' ? '⚠' : a.level === 'caution' ? '⚠' : 'ℹ'}
                </div>
                <div className="dash-alert-body">
                  <strong>{a.title}</strong>
                  <span>{a.time}</span>
                </div>
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  )
}
