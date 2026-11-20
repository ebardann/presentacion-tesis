<script setup lang="ts">
// Cuatro conceptos de MI como mini-ilustraciones: feature · superposición · circuito · intervención.

// 01 · feature: nube de activaciones alineada con una dirección
const O = { x: 28, y: 122 }
const dir = { x: 150, y: 38 }
const pts = Array.from({ length: 18 }, (_, i) => {
  const t = 0.15 + (i / 17) * 0.8
  const n = Math.sin(i * 12.9898) * 43758.5453
  const r = (n - Math.floor(n) - 0.5) * 26
  return { x: O.x + (dir.x - O.x) * t + r * 0.5, y: O.y + (dir.y - O.y) * t + r * 0.6 }
})

// 02 · superposición: 5 features en un espacio de 2 neuronas
const sup = ['var(--sun)', 'var(--teal)', 'var(--leaf)', 'var(--coral)', 'var(--ink)'].map((c, k) => {
  const a = -Math.PI / 2 + (k * 2 * Math.PI) / 5
  return { c, x2: 100 + Math.cos(a) * 52, y2: 78 + Math.sin(a) * 52 }
})

// 03 · circuito: red tenue con un subgrafo resaltado
const L = [0, 1, 2, 3].map(l => ({ x: 34 + l * 44, ys: [34, 64, 94, 124] }))
const hot = new Set(['0-1-2', '1-2-1', '2-1-1', '0-1-1', '1-1-1'])
const net = L.slice(0, -1).flatMap((a, l) => a.ys.flatMap((y1, i) => L[l + 1].ys.map((y2, j) => ({
  x1: a.x, y1, x2: L[l + 1].x, y2, hot: hot.has(`${l}-${i}-${j}`),
}))))
const hotN = new Set(['0-1', '1-1', '1-2', '2-1', '3-1'])

// 04 · intervención: reemplazar h cambia la estructura de salida
const shapeA = 'M128,112 C140,70 150,130 160,90 C168,60 178,110 186,70'
const shapeB = 'M128,112 C134,60 168,58 172,86 C176,112 140,112 150,84'
</script>

<template>
  <div class="mic4">
    <!-- 01 feature -->
    <figure>
      <svg viewBox="0 0 200 150">
        <defs>
          <marker id="mc-a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--accent)" /></marker>
        </defs>
        <line :x1="O.x" :y1="O.y" x2="188" :y2="O.y" class="ax" />
        <line :x1="O.x" :y1="O.y" :x2="O.x" y2="12" class="ax" />
        <circle v-for="(p, i) in pts" :key="i" :cx="p.x" :cy="p.y" r="3" class="pt" :style="{ animationDelay: `${i * 0.12}s` }" />
        <line :x1="O.x" :y1="O.y" :x2="dir.x" :y2="dir.y" class="dir" marker-end="url(#mc-a)" />
        <text :x="dir.x + 4" :y="dir.y - 6" class="tl">hélice α</text>
      </svg>
      <figcaption><b>feature</b><span>una dirección = una propiedad</span></figcaption>
    </figure>

    <!-- 02 superposición -->
    <figure>
      <svg viewBox="0 0 200 150">
        <line x1="40" y1="78" x2="160" y2="78" class="ax dash" />
        <line x1="100" y1="18" x2="100" y2="138" class="ax dash" />
        <text x="164" y="82" class="tl dim">n₁</text>
        <text x="104" y="16" class="tl dim">n₂</text>
        <g class="spin">
          <line v-for="(s, k) in sup" :key="k" x1="100" y1="78" :x2="s.x2" :y2="s.y2" :stroke="s.c" class="sv" />
          <circle v-for="(s, k) in sup" :key="'c' + k" :cx="s.x2" :cy="s.y2" r="4" :fill="s.c" />
        </g>
      </svg>
      <figcaption><b>superposición</b><span>5 features · 2 neuronas</span></figcaption>
    </figure>

    <!-- 03 circuito -->
    <figure>
      <svg viewBox="0 0 200 150">
        <line v-for="(e, i) in net" :key="i" v-bind="e" :class="e.hot ? 'eh' : 'e'" />
        <g v-for="(c, l) in L" :key="l">
          <circle v-for="(y, k) in c.ys" :key="k" :cx="c.x" :cy="y" r="5.5" :class="hotN.has(`${l}-${k}`) ? 'nh' : 'n'" />
        </g>
        <circle r="3" class="pulse"><animateMotion dur="2.4s" repeatCount="indefinite" path="M34,64 L78,94 L122,64 L166,64" /></circle>
        <circle r="3" class="pulse"><animateMotion dur="2.4s" begin="1.2s" repeatCount="indefinite" path="M34,64 L78,64 L122,64 L166,64" /></circle>
      </svg>
      <figcaption><b>circuito</b><span>el subgrafo que computa</span></figcaption>
    </figure>

    <!-- 04 intervención -->
    <figure>
      <svg viewBox="0 0 200 150">
        <defs>
          <marker id="mc-b" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--ink)" opacity=".5" /></marker>
        </defs>
        <circle cx="20" cy="92" r="7" class="n" />
        <line x1="29" y1="92" x2="52" y2="92" class="ar" marker-end="url(#mc-b)" />
        <rect x="56" y="76" width="36" height="32" rx="4" class="hbox" />
        <text x="74" y="97" class="tl hb" text-anchor="middle">h</text>
        <line x1="96" y1="92" x2="118" y2="92" class="ar" marker-end="url(#mc-b)" />
        <!-- fuente del patch -->
        <rect x="56" y="16" width="36" height="24" rx="4" class="src" />
        <text x="74" y="32" class="tl src-t" text-anchor="middle">h′</text>
        <line x1="74" y1="42" x2="74" y2="72" class="patch" />
        <!-- salida: la estructura cambia -->
        <path class="out" :d="shapeA">
          <animate attributeName="d" :values="`${shapeA};${shapeA};${shapeB};${shapeB};${shapeA}`" keyTimes="0;.35;.5;.85;1" dur="5s" repeatCount="indefinite" />
        </path>
      </svg>
      <figcaption><b>intervención</b><span>cambiar h → cambia el output</span></figcaption>
    </figure>
  </div>
</template>

<style scoped>
.mic4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.4rem; }
figure { margin: 0; display: flex; flex-direction: column; gap: .5rem; }
svg { width: 100%; height: auto; display: block; overflow: visible;
  border: 1px solid var(--accent-soft); border-radius: 6px; padding: .4rem; background: rgba(255,255,255,.015); }
figcaption { display: flex; flex-direction: column; gap: .1rem; font-family: var(--font-mono); }
figcaption b { color: var(--accent); font-weight: 500; font-size: .95rem; letter-spacing: .04em; }
figcaption span { font-size: .72rem; opacity: .7; }

.ax { stroke: var(--ink); stroke-width: 1; opacity: .35; }
.ax.dash { stroke-dasharray: 3 4; }
.tl { fill: var(--accent); font-family: var(--font-mono); font-size: 11px; }
.tl.dim { fill: var(--ink); opacity: .5; }
.pt { fill: var(--ink); opacity: .55; animation: blink 3s ease-in-out infinite; }
.dir { stroke: var(--accent); stroke-width: 2.2; filter: drop-shadow(0 0 4px var(--accent)); }

.sv { stroke-width: 2; opacity: .85; }
.spin { transform-origin: 100px 78px; animation: spin 24s linear infinite; }

.e { stroke: var(--ink); stroke-width: .6; opacity: .12; }
.eh { stroke: var(--accent); stroke-width: 2; opacity: .9; }
.n { fill: var(--bg); stroke: var(--ink); stroke-width: 1; opacity: .4; }
.nh { fill: var(--accent); stroke: var(--accent); filter: drop-shadow(0 0 4px var(--accent)); }
.pulse { fill: var(--ink); filter: drop-shadow(0 0 4px var(--ink)); }

.ar { stroke: var(--ink); stroke-width: 1; opacity: .5; }
.hbox { fill: var(--bg); stroke: var(--accent); stroke-width: 1.5; }
.hb { font-size: 14px; }
.src { fill: var(--accent-soft); stroke: var(--accent-2); stroke-width: 1; stroke-dasharray: 3 3; }
.src-t { fill: var(--accent-2); font-size: 12px; }
.patch { stroke: var(--accent-2); stroke-width: 1.5; stroke-dasharray: 4 4; animation: flow 1s linear infinite; }
.out { fill: none; stroke: var(--accent); stroke-width: 2.4; stroke-linecap: round; filter: drop-shadow(0 0 4px var(--accent)); }

@keyframes blink { 0%, 100% { opacity: .3; } 50% { opacity: .8; } }
@keyframes spin { to { transform: rotate(360deg); } }
@keyframes flow { to { stroke-dashoffset: -8; } }
</style>
