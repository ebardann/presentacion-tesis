<script setup lang="ts">
// Interpretability gap (Barez et al., "Understanding AI from the Inside", §1):
// lo que los modelos hacen (capacidades) crece más rápido que lo que entendemos de cómo lo hacen.
const X0 = 70, X1 = 840, Y0 = 300, N = 80
const xs = Array.from({ length: N + 1 }, (_, k) => k / N)
const cap = (t: number) => Y0 - 30 - 235 * t ** 2.4 - 12 * t
const und = (t: number) => Y0 - 30 - 62 * t ** 0.9
const px = (t: number) => X0 + t * (X1 - X0)
const line = (f: (t: number) => number) => 'M' + xs.map(t => `${px(t).toFixed(1)},${f(t).toFixed(1)}`).join(' L')
const capD = line(cap)
const undD = line(und)
const gapD = capD + ' L' + [...xs].reverse().map(t => `${px(t).toFixed(1)},${und(t).toFixed(1)}`).join(' L') + ' Z'

// riesgos que aparecen a medida que la brecha crece
const risks = [
  { t: 0.72, k: 0.5, s: 'razonamiento\nno rastreable' },
  { t: 0.84, k: 0.5, s: 'engaño\nno detectado' },
  { t: 0.95, k: 0.5, s: 'garantías\nfrágiles' },
].map(r => ({ ...r, x: px(r.t), y: und(r.t) - (und(r.t) - cap(r.t)) * r.k, lines: r.s.split('\n') }))
const ae = { x: px(1) + 22, y1: cap(1), y2: und(1) }
</script>

<template>
  <svg viewBox="0 0 960 340" class="gap" role="img" aria-label="las capacidades crecen más rápido que la comprensión: la brecha de interpretabilidad">
    <defs>
      <linearGradient id="ig-fill" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stop-color="var(--coral)" stop-opacity="0" />
        <stop offset=".55" stop-color="var(--coral)" stop-opacity=".14" />
        <stop offset="1" stop-color="var(--coral)" stop-opacity=".32" />
      </linearGradient>
      <pattern id="ig-hatch" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
        <line x1="0" y1="0" x2="0" y2="9" stroke="var(--coral)" stroke-width="1" opacity=".22" />
      </pattern>
      <marker id="ig-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="var(--coral)" /></marker>
      <marker id="ig-x" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--ink)" opacity=".5" /></marker>
    </defs>

    <!-- ejes -->
    <line :x1="X0" :y1="Y0" :x2="X1 + 60" :y2="Y0" class="ax" marker-end="url(#ig-x)" />
    <line :x1="X0" :y1="Y0" :x2="X0" y2="18" class="ax" marker-end="url(#ig-x)" />
    <text :x="X1 + 60" :y="Y0 + 22" class="axl" text-anchor="end">escala del modelo →</text>

    <!-- brecha -->
    <path :d="gapD" fill="url(#ig-fill)" />
    <path :d="gapD" fill="url(#ig-hatch)" class="hatch" />

    <!-- curvas -->
    <path :d="capD" class="cap" />
    <path :d="undD" class="und" />
    <text :x="px(0.66)" :y="cap(0.66) - 14" class="lab l-cap" text-anchor="end">lo que hacen</text>
    <text :x="px(0.42)" :y="und(0.42) + 24" class="lab l-und">lo que entendemos</text>

    <!-- riesgos dentro de la brecha -->
    <g v-for="(r, i) in risks" :key="i" class="risk" :style="{ animationDelay: `${i * 0.6}s` }">
      <circle :cx="r.x" :cy="r.y - 12" r="3.5" />
      <text v-for="(l, j) in r.lines" :key="j" :x="r.x" :y="r.y + 8 + j * 13" text-anchor="middle">{{ l }}</text>
    </g>

    <!-- magnitud de la brecha -->
    <line :x1="ae.x" :y1="ae.y1 + 4" :x2="ae.x" :y2="ae.y2 - 4" class="span" marker-start="url(#ig-a)" marker-end="url(#ig-a)" />
    <text :x="ae.x + 14" :y="(ae.y1 + ae.y2) / 2 + 6" class="gl">gap</text>
  </svg>
</template>

<style scoped>
.gap { width: 100%; height: auto; display: block; overflow: visible; color: var(--ink); }
.ax { stroke: var(--ink); stroke-width: 1; opacity: .4; }
.axl { fill: var(--ink); font-family: var(--font-mono); font-size: 12px; opacity: .5; letter-spacing: .04em; }

.cap { fill: none; stroke: var(--sun); stroke-width: 3.2; stroke-linecap: round; filter: drop-shadow(0 0 6px var(--sun)); }
.und { fill: none; stroke: var(--teal); stroke-width: 3.2; stroke-linecap: round; filter: drop-shadow(0 0 6px var(--teal)); }
.lab { font-family: var(--font-mono); font-size: 16px; letter-spacing: .03em; }
.l-cap { fill: var(--sun); }
.l-und { fill: var(--teal); }

.hatch { animation: drift 6s linear infinite; }
.risk { fill: var(--coral); font-family: var(--font-mono); font-size: 11px; animation: breathe 3.6s ease-in-out infinite; }
.risk circle { filter: drop-shadow(0 0 4px var(--coral)); }

.span { stroke: var(--coral); stroke-width: 2; animation: breathe 2.4s ease-in-out infinite; }
.gl { fill: var(--coral); font-family: var(--font-mono); font-size: 17px; font-weight: 500; letter-spacing: .04em; }

@keyframes breathe { 0%, 100% { opacity: .55; } 50% { opacity: 1; } }
@keyframes drift { to { transform: translateX(-9px); } }
</style>
