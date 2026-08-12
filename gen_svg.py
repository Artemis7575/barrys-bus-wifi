import math

W, H = 1200, 600
cx, cy = 600, 260  # sun / sunburst center

def ray_polygon(cx, cy, angle_deg, length, half_width_deg):
    a1 = math.radians(angle_deg - half_width_deg)
    a2 = math.radians(angle_deg + half_width_deg)
    x1 = cx + length * math.sin(a1)
    y1 = cy - length * math.cos(a1)
    x2 = cx + length * math.sin(a2)
    y2 = cy - length * math.cos(a2)
    return f"M{cx:.1f},{cy:.1f} L{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f} Z"

n_rays = 24
rays = []
for i in range(n_rays):
    angle = i * (360 / n_rays)
    color = "#ffe08a" if i % 2 == 0 else "#ffc95c"
    opacity = 0.35 if i % 2 == 0 else 0.22
    d = ray_polygon(cx, cy, angle, 520, 6.2)
    rays.append(f'<path d="{d}" fill="{color}" opacity="{opacity}"/>')
rays_svg = "\n    ".join(rays)

# road dashes
dashes = []
dash_y = 560
for i in range(-2, 14):
    x = i * 110 - 40
    dashes.append(f'<rect x="{x}" y="{dash_y}" width="60" height="10" rx="5" fill="#fdf3e3" opacity="0.9"/>')
dashes_svg = "\n    ".join(dashes)

# speed / motion lines behind bus
speed_lines = []
for i, (y, length) in enumerate([(430, 90), (455, 130), (480, 70), (505, 150)]):
    speed_lines.append(f'<rect x="{40-length}" y="{y}" width="{length}" height="10" rx="5" fill="#fdf3e3" opacity="0.55"/>')
speed_lines_svg = "\n    ".join(speed_lines)

# hills silhouette (simple layered)
hills = f"""
    <path d="M0,430 C150,370 300,410 480,380 C650,352 780,400 960,368 C1080,346 1150,378 1200,362 L1200,470 L0,470 Z" fill="#0f2f2c" opacity="0.9"/>
    <path d="M0,455 C180,410 360,445 560,420 C740,398 900,435 1080,412 C1140,404 1170,412 1200,408 L1200,470 L0,470 Z" fill="#0a2321"/>
"""

svg = f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="'Arial Black','Helvetica Neue',Arial,sans-serif">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0b3d3a"/>
      <stop offset="45%" stop-color="#1c5c53"/>
      <stop offset="75%" stop-color="#e8703a"/>
      <stop offset="100%" stop-color="#ff9143"/>
    </linearGradient>
    <radialGradient id="sunGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#fff3c4" stop-opacity="0.95"/>
      <stop offset="55%" stop-color="#ffce5c" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#ffce5c" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="busBody" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#fff8ec"/>
      <stop offset="100%" stop-color="#fde8c9"/>
    </linearGradient>
    <clipPath id="canvasClip"><rect x="0" y="0" width="{W}" height="{H}" rx="0"/></clipPath>
  </defs>

  <g clip-path="url(#canvasClip)">
    <rect x="0" y="0" width="{W}" height="{H}" fill="url(#sky)"/>

    <circle cx="{cx}" cy="{cy}" r="230" fill="url(#sunGlow)"/>

    <g>
    {rays_svg}
    </g>

    <circle cx="{cx}" cy="{cy}" r="92" fill="#ffd873" stroke="#ffe9ad" stroke-width="4"/>

    {hills}

    <!-- road -->
    <rect x="0" y="470" width="{W}" height="130" fill="#182422"/>
    <rect x="0" y="470" width="{W}" height="14" fill="#0e1a18"/>
    {dashes_svg}

    <!-- title banner -->
    <g transform="translate(600,92)">
      <text x="0" y="0" text-anchor="middle" font-size="86" fill="#fdf3e3" stroke="#16211f" stroke-width="6" paint-order="stroke" letter-spacing="2">BARRY'S BUS</text>
    </g>
    <g transform="translate(600,150)">
      <rect x="-260" y="-32" width="520" height="56" rx="28" fill="#ff5a36" stroke="#16211f" stroke-width="5"/>
      <text x="0" y="7" text-anchor="middle" font-size="30" fill="#fdf3e3" letter-spacing="3">FREE WI-FI ON BOARD</text>
    </g>

    <!-- speed lines -->
    {speed_lines_svg}

    <!-- BUS -->
    <g transform="translate(150,300)">
      <!-- shadow -->
      <ellipse cx="480" cy="270" rx="480" ry="26" fill="#0a1513" opacity="0.35"/>

      <!-- body -->
      <path d="M20,180
               L20,90
               Q20,55 60,50
               L130,42
               Q140,20 175,18
               L820,18
               Q860,18 875,50
               L920,70
               Q960,85 960,125
               L960,180
               Q960,205 935,205
               L45,205
               Q20,205 20,180 Z"
            fill="url(#busBody)" stroke="#16211f" stroke-width="7"/>

      <!-- coral stripe -->
      <path d="M20,150 L960,150 L960,180 Q960,205 935,205 L45,205 Q20,205 20,180 Z"
            fill="#ff5a36" stroke="#16211f" stroke-width="7"/>
      <!-- yellow accent stripe -->
      <rect x="20" y="150" width="940" height="14" fill="#ffc93c"/>

      <!-- windshield / front window -->
      <path d="M865,58 Q885,66 895,90 L905,128 L840,128 L840,50 Q855,52 865,58Z" fill="#bfe8e6" stroke="#16211f" stroke-width="6"/>

      <!-- side windows -->
      <g fill="#bfe8e6" stroke="#16211f" stroke-width="6">
        <rect x="150" y="55" width="95" height="70" rx="14"/>
        <rect x="265" y="55" width="95" height="70" rx="14"/>
        <rect x="380" y="55" width="95" height="70" rx="14"/>
        <rect x="495" y="55" width="95" height="70" rx="14"/>
        <rect x="610" y="55" width="95" height="70" rx="14"/>
        <rect x="725" y="55" width="95" height="70" rx="14"/>
      </g>

      <!-- door -->
      <rect x="60" y="70" width="60" height="110" rx="10" fill="#e7d6b3" stroke="#16211f" stroke-width="6"/>
      <line x1="90" y1="80" x2="90" y2="170" stroke="#16211f" stroke-width="4"/>

      <!-- headlight -->
      <circle cx="930" cy="150" r="14" fill="#ffe9a8" stroke="#16211f" stroke-width="5"/>

      <!-- bumper -->
      <rect x="940" y="175" width="35" height="26" rx="8" fill="#16211f"/>

      <!-- wordmark on side -->
      <text x="330" y="185" font-size="30" fill="#16211f" letter-spacing="1" font-weight="bold">BARRY'S BUS CO.</text>

      <!-- wheels -->
      <g>
        <circle cx="180" cy="215" r="46" fill="#16211f"/>
        <circle cx="180" cy="215" r="20" fill="#8a9a97"/>
        <circle cx="180" cy="215" r="7" fill="#16211f"/>

        <circle cx="800" cy="215" r="46" fill="#16211f"/>
        <circle cx="800" cy="215" r="20" fill="#8a9a97"/>
        <circle cx="800" cy="215" r="7" fill="#16211f"/>
      </g>
    </g>
  </g>
</svg>
'''

with open("/sessions/charming-keen-archimedes/mnt/outputs/assets/barrys-bus-hero.svg", "w") as f:
    f.write(svg)

print("wrote svg, length:", len(svg))
