<script setup lang="ts">
// Behavioural vs. mechanistic interpretability (Barez et al., §4.1).
// Izquierda: caja negra, sólo pares (x, f(x)). Derecha: la misma f, abierta: activaciones y el camino que computa y.
const rows = [80, 130, 180]
const OFF = 480 // desplazamiento del panel derecho

// red interna (panel derecho)
const L = [630, 670, 710, 750].map(x => ({ x, ys: [82, 114, 146, 178] }))
const hotE = new Set(['0-1-2', '1-2-1', '2-1-1'])
const net = L.slice(0, -1).flatMap((a, l) => a.ys.flatMap((y1, i) => L[l + 1].ys.map((y2, j) => ({
  x1: a.x, y1, x2: L[l + 1].x, y2, hot: hotE.has(`${l}-${i}-${j}`),
}))))
const hotN = new Set(['0-1', '1-2', '2-1', '3-1'])
const mechPath = `M${OFF + 50},130 L630,114 L670,146 L710,114 L750,114 L${OFF + 334},130`
</script>

<template>
  <div class="bm">
    <svg viewBox="0 24 900 188" class="fig" role="img" aria-label="interpretabilidad conductual: caja negra con pares entrada-salida; mecanística: la caja abierta con el camino interno">
      <defs>
        <marker id="bm-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--ink)" opacity=".45" /></marker>
      </defs>

      <!-- ===== behavioural ===== -->
      <g>
        <g v-for="(y, i) in rows" :key="'bx' + i">
          <rect x="10" :y="y - 13" width="36" height="26" rx="13" class="chip" />
          <text x="28" :y="y + 5" class="ct" text-anchor="middle">x{{ ['₁', '₂', '₃'][i] }}</text>
          <line x1="50" :y1="y" x2="124" y2="130" class="ar" marker-end="url(#bm-a)" />
          <line x1="296" y1="130" :x2="370" :y2="y" class="ar" marker-end="url(#bm-a)" />
          <rect x="374" :y="y - 13" width="36" height="26" rx="13" class="chip out" />
          <text x="392" :y="y + 5" class="ct out" text-anchor="middle">y{{ ['₁', '₂', '₃'][i] }}</text>
        </g>
        <rect x="130" y="56" width="160" height="148" rx="8" class="black" />
        <text x="210" y="148" class="q" text-anchor="middle">?</text>
        <circle r="4" class="pulse"><animateMotion dur="2.8s" repeatCount="indefinite" keyPoints="0;1" keyTimes="0;1" path="M50,80 L128,130" /><animate attributeName="opacity" values="1;1;0" keyTimes="0;.85;1" dur="2.8s" repeatCount="indefinite" /></circle>
        <circle r="4" class="pulse out"><animateMotion dur="2.8s" begin="1.4s" repeatCount="indefinite" path="M298,130 L370,180" /><animate attributeName="opacity" values="0;1;1" keyTimes="0;.15;1" dur="2.8s" begin="1.4s" repeatCount="indefinite" /></circle>
      </g>

      <!-- divisor -->
      <line x1="450" y1="30" x2="450" y2="210" class="div" />

      <!-- ===== mechanistic ===== -->
      <g>
        <g v-for="(y, i) in rows" :key="'mx' + i">
          <rect :x="OFF + 10" :y="y - 13" width="36" height="26" rx="13" class="chip" />
          <text :x="OFF + 28" :y="y + 5" class="ct" text-anchor="middle">x{{ ['₁', '₂', '₃'][i] }}</text>
          <rect :x="OFF + 374" :y="y - 13" width="36" height="26" rx="13" class="chip out" />
          <text :x="OFF + 392" :y="y + 5" class="ct out" text-anchor="middle">y{{ ['₁', '₂', '₃'][i] }}</text>
        </g>
        <line v-for="(y, i) in rows" :key="'mi' + i" :x1="OFF + 50" :y1="y" :x2="OFF + 124" y2="130" class="ar" marker-end="url(#bm-a)" />
        <line v-for="(y, i) in rows" :key="'mo' + i" :x1="OFF + 296" y1="130" :x2="OFF + 370" :y2="y" class="ar" marker-end="url(#bm-a)" />
        <rect :x="OFF + 130" y="56" width="160" height="148" rx="8" class="glass" />
        <line v-for="(e, i) in net" :key="i" v-bind="e" :class="e.hot ? 'eh' : 'e'" />
        <g v-for="(c, l) in L" :key="l">
          <circle v-for="(y, k) in c.ys" :key="k" :cx="c.x" :cy="y" r="6" :class="hotN.has(`${l}-${k}`) ? 'nh' : 'n'" />
        </g>
        <!-- lupa -->
        <circle cx="670" cy="146" r="17" class="lens" />
        <line x1="682" y1="158" x2="694" y2="170" class="lens-h" />
        <circle r="4" class="pulse hot"><animateMotion dur="2.8s" repeatCount="indefinite" :path="mechPath" /></circle>
      </g>
    </svg>

    <div class="caps">
      <div><b>conductual</b><span>caja negra · sólo pares (x, f(x)) → <i>qué</i> hace</span></div>
      <div><b class="hot">mecanística</b><span>caja abierta · el cómputo interno → <i>cómo</i> lo hace</span></div>
    </div>
  </div>
</template>

<style scoped>
.fig { width: 100%; height: auto; display: block; overflow: visible; color: var(--ink); }
.chip { fill: rgba(241, 236, 216, .06); stroke: var(--ink); stroke-width: 1; opacity: .7; }
.chip.out { stroke: var(--accent-2); fill: rgba(63, 217, 199, .08); opacity: 1; }
.ct { fill: var(--ink); font-family: var(--font-mono); font-size: 12px; }
.ct.out { fill: var(--accent-2); }
.ar { stroke: var(--ink); stroke-width: 1; opacity: .4; }

.black { fill: #020504; stroke: var(--ink); stroke-width: 1; stroke-opacity: .35; }
.q { fill: var(--ink); font-family: var(--font-mono); font-size: 52px; opacity: .25; }

.glass { fill: rgba(255, 194, 75, .04); stroke: var(--accent); stroke-width: 1.4; stroke-dasharray: 5 4; }
.e { stroke: var(--ink); stroke-width: .6; opacity: .14; }
.eh { stroke: var(--accent); stroke-width: 2.2; opacity: .95; }
.n { fill: var(--bg); stroke: var(--ink); stroke-width: 1; opacity: .45; }
.nh { fill: var(--accent); stroke: var(--accent); filter: drop-shadow(0 0 5px var(--accent)); }
.lens { fill: none; stroke: var(--ink); stroke-width: 2; opacity: .8; }
.lens-h { stroke: var(--ink); stroke-width: 3.5; stroke-linecap: round; opacity: .8; }

.pulse { fill: var(--ink); filter: drop-shadow(0 0 4px var(--ink)); }
.pulse.out { fill: var(--accent-2); filter: drop-shadow(0 0 4px var(--accent-2)); }
.pulse.hot { fill: var(--accent); filter: drop-shadow(0 0 6px var(--accent)); }
.div { stroke: var(--accent-soft); stroke-width: 1; stroke-dasharray: 2 5; }

.caps { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: .9rem; font-family: var(--font-mono); text-align: center; }
.caps div { display: flex; flex-direction: column; gap: .35rem; }
.caps b { font-size: 1.1rem; font-weight: 500; letter-spacing: .05em; color: var(--ink); opacity: .85; }
.caps b.hot { color: var(--accent); opacity: 1; }
.caps span { font-size: .78rem; opacity: .65; }
.caps i { font-style: normal; color: var(--accent); }
</style>
