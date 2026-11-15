"""
Generate SVG and graphical assets for NEVO TECH website
"""
import os

os.makedirs("assets", exist_ok=True)

# 1. DevSync Project Preview SVG
devsync_svg = '''<svg width="600" height="400" viewBox="0 0 600 400" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="600" height="400" rx="12" fill="#0B132B"/>
  <!-- Top bar -->
  <rect width="600" height="38" fill="#1C2541"/>
  <circle cx="20" cy="19" r="6" fill="#FF5F56"/>
  <circle cx="38" cy="19" r="6" fill="#FFBD2E"/>
  <circle cx="56" cy="19" r="6" fill="#27C93F"/>
  <rect x="180" y="9" width="240" height="20" rx="10" fill="#0B132B" opacity="0.6"/>
  <text x="300" y="23" font-family="'Inter', sans-serif" font-size="10" fill="#89E3F5" text-anchor="middle">app.devsync.io/pipeline/main</text>
  
  <!-- Sidebar -->
  <rect x="0" y="38" width="130" height="362" fill="#111B33"/>
  <rect x="14" y="55" width="85" height="12" rx="4" fill="#3A506B"/>
  <rect x="14" y="80" width="102" height="10" rx="3" fill="#89E3F5" fill-opacity="0.3"/>
  <rect x="14" y="100" width="90" height="10" rx="3" fill="#3A506B" fill-opacity="0.5"/>
  <rect x="14" y="120" width="75" height="10" rx="3" fill="#3A506B" fill-opacity="0.5"/>
  <rect x="14" y="140" width="95" height="10" rx="3" fill="#3A506B" fill-opacity="0.5"/>
  <rect x="14" y="160" width="80" height="10" rx="3" fill="#3A506B" fill-opacity="0.5"/>

  <!-- Main Canvas / Graph -->
  <rect x="145" y="50" width="440" height="110" rx="8" fill="#152238" stroke="#3A506B" stroke-width="1"/>
  <text x="160" y="72" font-family="'Plus Jakarta Sans', sans-serif" font-size="12" font-weight="600" fill="#FFFFFF">Sprint Velocity &amp; Microservices Health</text>
  <text x="160" y="90" font-family="'Inter', sans-serif" font-size="10" fill="#89E3F5">99.98% Uptime · 24 Deployments Today</text>
  
  <!-- Area Sparkline -->
  <path d="M160 140 Q 210 110, 260 125 T 360 95 T 460 110 T 560 85 L 560 150 L 160 150 Z" fill="url(#sparkGrad)" opacity="0.4"/>
  <path d="M160 140 Q 210 110, 260 125 T 360 95 T 460 110 T 560 85" stroke="#89E3F5" stroke-width="2.5" fill="none"/>
  <circle cx="560" cy="85" r="4" fill="#89E3F5"/>

  <!-- Code / Service panels -->
  <rect x="145" y="172" width="210" height="210" rx="8" fill="#152238" stroke="#3A506B" stroke-width="1"/>
  <text x="160" y="195" font-family="'Inter', monospace" font-size="11" fill="#89E3F5">auth-service:v2.4.1</text>
  <rect x="160" y="210" width="180" height="8" rx="2" fill="#20304c"/>
  <rect x="160" y="225" width="140" height="8" rx="2" fill="#20304c"/>
  <rect x="160" y="240" width="165" height="8" rx="2" fill="#20304c"/>
  <rect x="160" y="260" width="100" height="24" rx="4" fill="#27C93F" fill-opacity="0.2"/>
  <text x="210" y="276" font-family="'Inter', sans-serif" font-size="10" fill="#27C93F" text-anchor="middle" font-weight="600">PASSED 42 TESTS</text>

  <rect x="370" y="172" width="215" height="210" rx="8" fill="#152238" stroke="#3A506B" stroke-width="1"/>
  <text x="385" y="195" font-family="'Inter', sans-serif" font-size="12" font-weight="600" fill="#FFFFFF">Active Contributors</text>
  <!-- Avatars row -->
  <circle cx="400" cy="225" r="14" fill="#89E3F5"/>
  <text x="400" y="229" font-family="'Inter', sans-serif" font-size="10" font-weight="bold" fill="#0B132B" text-anchor="middle">JD</text>
  <circle cx="435" cy="225" r="14" fill="#FFBD2E"/>
  <text x="435" y="229" font-family="'Inter', sans-serif" font-size="10" font-weight="bold" fill="#0B132B" text-anchor="middle">AM</text>
  <circle cx="470" cy="225" r="14" fill="#A8B9C5"/>
  <text x="470" y="229" font-family="'Inter', sans-serif" font-size="10" font-weight="bold" fill="#0B132B" text-anchor="middle">SK</text>

  <rect x="385" y="260" width="185" height="10" rx="5" fill="#20304c"/>
  <rect x="385" y="260" width="135" height="10" rx="5" fill="#89E3F5"/>
  <text x="385" y="290" font-family="'Inter', sans-serif" font-size="10" fill="#A8B9C5">Current Sprint: 74% Complete</text>

  <defs>
    <linearGradient id="sparkGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#89E3F5" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#89E3F5" stop-opacity="0.0"/>
    </linearGradient>
  </defs>
</svg>'''

# 2. Heavy Machinery Project Preview SVG
heavy_machinery_svg = '''<svg width="600" height="400" viewBox="0 0 600 400" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="600" height="400" rx="12" fill="#F8FAFC"/>
  <!-- Top bar -->
  <rect width="600" height="42" fill="#0F172A"/>
  <rect x="20" y="14" width="70" height="14" rx="3" fill="#F59E0B"/>
  <text x="55" y="25" font-family="'Plus Jakarta Sans', sans-serif" font-size="9" font-weight="800" fill="#0F172A" text-anchor="middle">TITAN B2B</text>
  <rect x="120" y="11" width="300" height="20" rx="4" fill="#1E293B"/>
  <text x="135" y="25" font-family="'Inter', sans-serif" font-size="10" fill="#94A3B8">🔍 Search excavators, cranes, CNC tooling...</text>
  <rect x="520" y="11" width="60" height="20" rx="4" fill="#3B82F6"/>
  <text x="550" y="24" font-family="'Inter', sans-serif" font-size="9" fill="#FFFFFF" text-anchor="middle" font-weight="600">RFQ (4)</text>

  <!-- Banner -->
  <rect x="20" y="55" width="560" height="100" rx="8" fill="#1E293B"/>
  <text x="40" y="88" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="700" fill="#FFFFFF">Global Industrial Marketplace</text>
  <text x="40" y="108" font-family="'Inter', sans-serif" font-size="11" fill="#CBD5E1">Over 14,000 Verified Equipment Manufacturers Worldwide</text>
  <rect x="40" y="122" width="120" height="24" rx="4" fill="#F59E0B"/>
  <text x="100" y="138" font-family="'Inter', sans-serif" font-size="10" font-weight="700" fill="#0F172A" text-anchor="middle">Request Instant RFQ</text>

  <!-- Cards Grid -->
  <!-- Card 1 -->
  <rect x="20" y="170" width="175" height="210" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
  <rect x="20" y="170" width="175" height="100" rx="8" fill="#E2E8F0"/>
  <path d="M50 240 L105 200 L165 240 Z" fill="#94A3B8"/>
  <circle cx="105" cy="205" r="14" fill="#F59E0B"/>
  <text x="32" y="290" font-family="'Plus Jakarta Sans', sans-serif" font-size="11" font-weight="700" fill="#0F172A">CAT 336 Excavator</text>
  <text x="32" y="306" font-family="'Inter', sans-serif" font-size="10" fill="#64748B">311 HP · 37.2 Tonnes</text>
  <text x="32" y="330" font-family="'Plus Jakarta Sans', sans-serif" font-size="13" font-weight="800" fill="#059669">$285,000</text>
  <rect x="32" y="344" width="151" height="24" rx="4" fill="#0F172A"/>
  <text x="107" y="359" font-family="'Inter', sans-serif" font-size="9" fill="#FFFFFF" text-anchor="middle" font-weight="600">Contact Supplier</text>

  <!-- Card 2 -->
  <rect x="212" y="170" width="175" height="210" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
  <rect x="212" y="170" width="175" height="100" rx="8" fill="#E2E8F0"/>
  <rect x="240" y="195" width="120" height="50" rx="4" fill="#64748B"/>
  <circle cx="300" cy="220" r="16" fill="#3B82F6"/>
  <text x="224" y="290" font-family="'Plus Jakarta Sans', sans-serif" font-size="11" font-weight="700" fill="#0F172A">Haas VF-4 CNC Mill</text>
  <text x="224" y="306" font-family="'Inter', sans-serif" font-size="10" fill="#64748B">5-Axis · High Precision</text>
  <text x="224" y="330" font-family="'Plus Jakarta Sans', sans-serif" font-size="13" font-weight="800" fill="#059669">$142,500</text>
  <rect x="224" y="344" width="151" height="24" rx="4" fill="#0F172A"/>
  <text x="299" y="359" font-family="'Inter', sans-serif" font-size="9" fill="#FFFFFF" text-anchor="middle" font-weight="600">Contact Supplier</text>

  <!-- Card 3 -->
  <rect x="405" y="170" width="175" height="210" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
  <rect x="405" y="170" width="175" height="100" rx="8" fill="#E2E8F0"/>
  <polygon points="492,185 530,245 455,245" fill="#475569"/>
  <circle cx="492" cy="215" r="12" fill="#E11D48"/>
  <text x="417" y="290" font-family="'Plus Jakarta Sans', sans-serif" font-size="11" font-weight="700" fill="#0F172A">Liebherr LTM Crane</text>
  <text x="417" y="306" font-family="'Inter', sans-serif" font-size="10" fill="#64748B">120 Ton · Telescopic</text>
  <text x="417" y="330" font-family="'Plus Jakarta Sans', sans-serif" font-size="13" font-weight="800" fill="#059669">$420,000</text>
  <rect x="417" y="344" width="151" height="24" rx="4" fill="#0F172A"/>
  <text x="492" y="359" font-family="'Inter', sans-serif" font-size="9" fill="#FFFFFF" text-anchor="middle" font-weight="600">Contact Supplier</text>
</svg>'''

# 3. College Portal Project Preview SVG
college_portal_svg = '''<svg width="600" height="400" viewBox="0 0 600 400" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="600" height="400" rx="12" fill="#F0F4F8"/>
  <!-- Top Nav -->
  <rect width="600" height="42" fill="#1E3A8A"/>
  <circle cx="25" cy="21" r="10" fill="#60A5FA"/>
  <text x="45" y="26" font-family="'Plus Jakarta Sans', sans-serif" font-size="11" font-weight="800" fill="#FFFFFF">APEX UNIVERSITY</text>
  <rect x="430" y="11" width="75" height="20" rx="10" fill="#3B82F6"/>
  <text x="467" y="24" font-family="'Inter', sans-serif" font-size="9" fill="#FFFFFF" text-anchor="middle">Admissions</text>
  <circle cx="530" cy="21" r="11" fill="#FFFFFF"/>
  <circle cx="560" cy="21" r="11" fill="#93C5FD"/>

  <!-- Hero inside portal -->
  <rect x="20" y="55" width="560" height="120" rx="8" fill="#2563EB"/>
  <text x="40" y="90" font-family="'Plus Jakarta Sans', sans-serif" font-size="18" font-weight="700" fill="#FFFFFF">Welcome back, Sarah Connor</text>
  <text x="40" y="112" font-family="'Inter', sans-serif" font-size="11" fill="#DBEAFE">B.Tech Computer Science &amp; AI · Semester 6 · GPA: 3.92</text>
  <rect x="40" y="130" width="130" height="26" rx="13" fill="#FFFFFF"/>
  <text x="105" y="146" font-family="'Inter', sans-serif" font-size="10" font-weight="700" fill="#1E3A8A" text-anchor="middle">Course Schedule →</text>

  <!-- 3 widget cards -->
  <rect x="20" y="190" width="175" height="190" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
  <text x="35" y="215" font-family="'Plus Jakarta Sans', sans-serif" font-size="11" font-weight="700" fill="#1E293B">Attendance Rate</text>
  <circle cx="107" cy="275" r="40" stroke="#E2E8F0" stroke-width="8" fill="none"/>
  <circle cx="107" cy="275" r="40" stroke="#10B981" stroke-width="8" stroke-dasharray="200" stroke-dashoffset="30" fill="none"/>
  <text x="107" y="280" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="800" fill="#0F172A" text-anchor="middle">94%</text>
  <text x="107" y="345" font-family="'Inter', sans-serif" font-size="9" fill="#64748B" text-anchor="middle">Minimum 75% required</text>

  <rect x="212" y="190" width="175" height="190" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
  <text x="227" y="215" font-family="'Plus Jakarta Sans', sans-serif" font-size="11" font-weight="700" fill="#1E293B">Upcoming Exams</text>
  <rect x="227" y="235" width="145" height="36" rx="4" fill="#F8FAFC" stroke="#E2E8F0"/>
  <text x="235" y="250" font-family="'Inter', sans-serif" font-size="10" font-weight="600" fill="#0F172A">Cloud Architecture</text>
  <text x="235" y="263" font-family="'Inter', sans-serif" font-size="8" fill="#DC2626">Nov 12 · Hall B-201</text>
  <rect x="227" y="280" width="145" height="36" rx="4" fill="#F8FAFC" stroke="#E2E8F0"/>
  <text x="235" y="295" font-family="'Inter', sans-serif" font-size="10" font-weight="600" fill="#0F172A">Deep Learning Lab</text>
  <text x="235" y="308" font-family="'Inter', sans-serif" font-size="8" fill="#2563EB">Nov 15 · Lab 4</text>

  <rect x="405" y="190" width="175" height="190" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
  <text x="420" y="215" font-family="'Plus Jakarta Sans', sans-serif" font-size="11" font-weight="700" fill="#1E293B">Financial Portal</text>
  <text x="420" y="240" font-family="'Inter', sans-serif" font-size="9" fill="#64748B">Tuition Fees Semester 6</text>
  <text x="420" y="265" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="800" fill="#10B981">PAID IN FULL</text>
  <rect x="420" y="285" width="145" height="24" rx="4" fill="#F1F5F9"/>
  <text x="492" y="300" font-family="'Inter', sans-serif" font-size="9" fill="#334155" text-anchor="middle">Download Tax Receipt</text>
</svg>'''

# 4. Modern Collaborative Office Visual SVG for "About NEVO TECH"
office_svg = '''<svg width="640" height="520" viewBox="0 0 640 520" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="wallGrad" x1="0" y1="0" x2="640" y2="520" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#181e29"/>
      <stop offset="100%" stop-color="#0a0d13"/>
    </linearGradient>
    <linearGradient id="logoGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="50%" stop-color="#89E3F5"/>
      <stop offset="100%" stop-color="#38BDF8"/>
    </linearGradient>
    <filter id="neonGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Background Office Architecture -->
  <rect width="640" height="520" rx="16" fill="url(#wallGrad)"/>
  
  <!-- Ceiling Light Tracks with Neon Ice Blue Glow -->
  <line x1="80" y1="40" x2="560" y2="40" stroke="#3A506B" stroke-width="3"/>
  <line x1="120" y1="40" x2="200" y2="40" stroke="#89E3F5" stroke-width="4" filter="url(#neonGlow)"/>
  <line x1="380" y1="40" x2="480" y2="40" stroke="#89E3F5" stroke-width="4" filter="url(#neonGlow)"/>

  <!-- Ambient Wall Lighting -->
  <ellipse cx="320" cy="180" rx="260" ry="140" fill="#89E3F5" fill-opacity="0.08"/>

  <!-- Feature Dark Wall with Illuminated "N" NEVO TECH Logo -->
  <rect x="180" y="90" width="280" height="150" rx="12" fill="#141923" stroke="#252D3D" stroke-width="2"/>
  
  <!-- Origami 3D Illuminated "N" Logo -->
  <g transform="translate(295, 120)">
    <!-- Left vertical bar -->
    <path d="M0 0 L14 -8 L14 48 L0 56 Z" fill="url(#logoGrad)" filter="url(#neonGlow)"/>
    <!-- Diagonal cross ribbon -->
    <path d="M14 -8 L40 38 L26 46 L0 0 Z" fill="#89E3F5" opacity="0.95"/>
    <!-- Right vertical bar -->
    <path d="M26 0 L40 -8 L40 48 L26 56 Z" fill="url(#logoGrad)" filter="url(#neonGlow)"/>
  </g>
  <text x="320" y="205" font-family="'Plus Jakarta Sans', sans-serif" font-size="14" font-weight="800" fill="#FFFFFF" text-anchor="middle" letter-spacing="3">NEVO TECH</text>
  <text x="320" y="222" font-family="'Inter', sans-serif" font-size="8" font-weight="600" fill="#89E3F5" text-anchor="middle" letter-spacing="4">INNOVATION HUB</text>

  <!-- Big Glass Conference Table in foreground -->
  <path d="M60 410 L580 410 L510 510 L130 510 Z" fill="#1E2837" stroke="#3A506B" stroke-width="1.5"/>
  <path d="M70 415 L570 415 L505 500 L135 500 Z" fill="#141E2C" opacity="0.7"/>

  <!-- Laptops on table with glowing screens -->
  <!-- Laptop 1 -->
  <rect x="180" y="420" width="70" height="42" rx="4" fill="#0B132B" stroke="#38BDF8" stroke-width="1.5" filter="url(#neonGlow)"/>
  <text x="215" y="444" font-family="'Inter', monospace" font-size="8" fill="#89E3F5" text-anchor="middle">&lt;code /&gt;</text>
  <!-- Laptop 2 -->
  <rect x="390" y="420" width="70" height="42" rx="4" fill="#0B132B" stroke="#89E3F5" stroke-width="1.5" filter="url(#neonGlow)"/>
  <text x="425" y="444" font-family="'Inter', monospace" font-size="8" fill="#89E3F5" text-anchor="middle">AI Pipeline</text>

  <!-- Silhouettes of Engineers & Consultants Collaborating -->
  <!-- Person 1 (Left) -->
  <circle cx="160" cy="310" r="22" fill="#222B3A"/>
  <path d="M120 400 C120 350, 150 335, 175 338 C195 340, 205 370, 200 400 Z" fill="#1D2433"/>

  <!-- Person 2 (Center left) -->
  <circle cx="270" cy="320" r="20" fill="#2A3547"/>
  <path d="M235 400 C235 355, 260 345, 280 348 C300 350, 310 380, 305 400 Z" fill="#222C3D"/>

  <!-- Person 3 (Right) -->
  <circle cx="475" cy="305" r="23" fill="#2A3547"/>
  <path d="M435 400 C435 350, 465 335, 490 338 C515 340, 525 375, 520 400 Z" fill="#1D2433"/>

  <!-- Indoor plant on right -->
  <path d="M570 340 Q 560 380, 580 430 Q 600 370, 570 340 Z" fill="#1E392B"/>
  <path d="M590 320 Q 580 360, 600 420 Q 620 360, 590 320 Z" fill="#284D3A"/>
  <rect x="575" y="430" width="30" height="35" rx="4" fill="#332219"/>

  <!-- Live interactive overlay badge -->
  <g transform="translate(30, 30)">
    <rect width="180" height="36" rx="18" fill="#111827" fill-opacity="0.8" stroke="#38BDF8" stroke-width="1"/>
    <circle cx="20" cy="18" r="6" fill="#10B981"/>
    <circle cx="20" cy="18" r="10" stroke="#10B981" stroke-width="1.5" opacity="0.6"/>
    <text x="36" y="22" font-family="'Inter', sans-serif" font-size="10" font-weight="600" fill="#F3F4F6">NEVO Headquarters · Active</text>
  </g>
</svg>'''

# 5. Rohan Mehta Client Avatar SVG
avatar_rohan_svg = '''<svg width="120" height="120" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="60" cy="60" r="58" fill="#1E293B" stroke="#89E3F5" stroke-width="3"/>
  <circle cx="60" cy="46" r="22" fill="#D97706"/>
  <!-- Hair & beard -->
  <path d="M38 42 C38 25, 82 25, 82 42 C82 32, 70 24, 60 24 C50 24, 38 32, 38 42 Z" fill="#1E1B18"/>
  <path d="M42 48 C42 66, 78 66, 78 48 C78 68, 42 68, 42 48 Z" fill="#1E1B18"/>
  <!-- Eyes -->
  <circle cx="52" cy="45" r="2.5" fill="#1E1B18"/>
  <circle cx="68" cy="45" r="2.5" fill="#1E1B18"/>
  <!-- Smile -->
  <path d="M54 54 Q 60 58, 66 54" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round"/>
  <!-- Shoulders / suit -->
  <path d="M22 108 C22 84, 40 76, 60 76 C80 76, 98 84, 98 108 Z" fill="#0F172A"/>
  <polygon points="60,76 52,95 68,95" fill="#89E3F5"/>
  <circle cx="92" cy="92" r="14" fill="#3B82F6" stroke="#FFFFFF" stroke-width="2"/>
  <text x="92" y="96" font-family="'Inter', sans-serif" font-size="10" font-weight="bold" fill="#FFFFFF" text-anchor="middle">✓</text>
</svg>'''

# Write files
with open("assets/project-devsync.svg", "w", encoding="utf-8") as f:
    f.write(devsync_svg)
with open("assets/project-heavymachinery.svg", "w", encoding="utf-8") as f:
    f.write(heavy_machinery_svg)
with open("assets/project-collegeportal.svg", "w", encoding="utf-8") as f:
    f.write(college_portal_svg)
with open("assets/office-render.svg", "w", encoding="utf-8") as f:
    f.write(office_svg)
with open("assets/client-rohan.svg", "w", encoding="utf-8") as f:
    f.write(avatar_rohan_svg)

print("SVG assets created successfully!")
