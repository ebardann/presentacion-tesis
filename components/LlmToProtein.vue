<script setup lang="ts">
// El brinco: las herramientas de MI nacieron en LLMs y ahora se llevan a predictores de proteínas.
// Izquierda: LLM (un vector por token → siguiente palabra).
// Derecha: predictor de estructura (vector por residuo + pair L×L → coordenadas 3D).
const rnd = (i: number) => { const n = Math.sin(i * 12.9898 + 4.1) * 43758.5453; return n - Math.floor(n) }
const C = 15 // tamaño de celda

// ---------- LLM ----------
const toks = ['el', 'gato', 'come']
const lx = [95, 150, 205]
const vecs = lx.flatMap((x, t) => Array.from({ length: 6 }, (_, k) => ({ x: x - C / 2, y: 112 + k * C, o: 0.15 + 0.7 * rnd(t * 6 + k) })))

// ---------- proteína ----------
const res = ['M', 'K', 'T', 'V', 'L', 'E']
const GX = 790 - (res.length * C) / 2, GY = 104
const pair = res.flatMap((_, i) => res.map((_, j) => {
  const d = Math.abs(i - j)
  const hot = (i === 0 && j === 5) || (i === 5 && j === 0)
  return { x: GX + j * C, y: GY + i * C, o: hot ? 1 : d === 0 ? 0.75 : d === 1 ? 0.45 : 0.06 + 0.12 * rnd(i * 7 + j), hot }
}))
const single = res.map((r, i) => ({ r, x: GX + i * C, o: 0.2 + 0.6 * rnd(i + 40) }))

// ---------- el brinco ----------
const P0 = { x: 275, y: 170 }, P1 = { x: 470, y: 0 }, P2 = { x: 665, y: 170 }
const B = (t: number) => ({
  x: (1 - t) ** 2 * P0.x + 2 * t * (1 - t) * P1.x + t ** 2 * P2.x,
  y: (1 - t) ** 2 * P0.y + 2 * t * (1 - t) * P1.y + t ** 2 * P2.y,
})
const arc = `M${P0.x},${P0.y} Q${P1.x},${P1.y} ${P2.x},${P2.y}`
const tools = ['probes', 'patching', 'SAEs', 'circuitos'].map((s, i) => ({ s, ...B(0.14 + i * 0.24) }))
</script>

<template>
  <div class="l2p">
    <svg viewBox="0 0 960 290" class="fig" role="img" aria-label="las herramientas de interpretabilidad mecanística pasan de LLMs a predictores de estructura de proteínas">
      <defs>
        <marker id="l2p-a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--ink)" opacity=".5" /></marker>
        <marker id="l2p-b" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--accent)" /></marker>
      </defs>

      <!-- ===== LLM ===== -->
      <rect x="40" y="6" width="220" height="276" rx="10" class="panel" />
      <text x="150" y="30" class="hd" text-anchor="middle">LLM</text>
      <rect x="108" y="48" width="84" height="26" rx="13" class="chip out" />
      <text x="150" y="66" class="ct out" text-anchor="middle">pescado</text>
      <line x1="150" y1="106" x2="150" y2="80" class="ar" marker-end="url(#l2p-a)" />
      <rect v-for="(v, i) in vecs" :key="'v' + i" :x="v.x" :y="v.y" :width="C - 2" :height="C - 2" rx="2" class="cell" :style="{ opacity: v.o }" />
      <g v-for="(t, i) in toks" :key="t">
        <line :x1="lx[i]" y1="230" :x2="lx[i]" y2="206" class="ar" marker-end="url(#l2p-a)" />
        <rect :x="lx[i] - 26" y="236" width="52" height="24" rx="12" class="chip" />
        <text :x="lx[i]" y="253" class="ct" text-anchor="middle">{{ t }}</text>
      </g>

      <!-- ===== el brinco ===== -->
      <path :d="arc" class="arc" marker-end="url(#l2p-b)" />
      <circle r="5" class="pulse"><animateMotion dur="3.2s" repeatCount="indefinite" :path="arc" /></circle>
      <g v-for="(t, i) in tools" :key="t.s">
        <rect :x="t.x - 40" :y="t.y - 12" width="80" height="24" rx="4" class="tool" />
        <text :x="t.x" :y="t.y + 5" class="tt" text-anchor="middle">{{ t.s }}</text>
      </g>

      <!-- ===== proteína ===== -->
      <rect x="680" y="6" width="220" height="276" rx="10" class="panel hot" />
      <text x="790" y="30" class="hd hot" text-anchor="middle">proteínas</text>
      <!-- estructura 3D -->
      <path d="M738,78 C746,44 756,88 766,56 C774,32 784,84 794,54 C802,32 812,78 822,52 C830,34 838,62 846,44" class="fold" />
      <circle cx="738" cy="78" r="4" class="contact" />
      <circle cx="846" cy="44" r="4" class="contact" />
      <line x1="738" y1="78" x2="846" y2="44" class="cline" />
      <line x1="790" y1="100" x2="790" y2="86" class="ar" marker-end="url(#l2p-a)" />
      <!-- pair L×L -->
      <rect v-for="(p, i) in pair" :key="'p' + i" :x="p.x" :y="p.y" :width="C - 2" :height="C - 2" rx="2" :class="p.hot ? 'cell hotc' : 'cell'" :style="{ opacity: p.o }" />
      <!-- single -->
      <rect v-for="(s, i) in single" :key="'s' + i" :x="s.x" :y="GY + res.length * C + 6" :width="C - 2" :height="C - 2" rx="2" class="cell sg" :style="{ opacity: s.o }" />
      <g v-for="(s, i) in single" :key="'r' + i">
        <rect :x="s.x - 1" y="236" :width="C" height="24" rx="3" class="chip" />
        <text :x="s.x + C / 2 - 1" y="253" class="ct" text-anchor="middle">{{ s.r }}</text>
      </g>
    </svg>

    <div class="caps">
      <div><span>vector por token → <b>palabra</b></span></div>
      <div class="mid"><span>mismas herramientas · otro modelo</span></div>
      <div><span><b>pair L×L</b> → <b>geometría 3D</b></span></div>
    </div>

    <div class="path">
      <div v-for="(m, i) in [['ESM-2', 'InterPLM'], ['ESMFold', 'SAEFold'], ['Boltz-2', 'PairSAE'], ['AF3', 'AlphaInterp']]" :key="m[0]" class="m" :class="{ last: i === 3 }">
        <b>{{ m[0] }}</b><span>{{ m[1] }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.fig { width: 100%; height: auto; display: block; overflow: visible; color: var(--ink); }
.panel { fill: rgba(241, 236, 216, .02); stroke: var(--ink); stroke-opacity: .2; stroke-width: 1; }
.panel.hot { stroke: var(--accent); stroke-opacity: .55; fill: rgba(63, 217, 199, .03); }
.hd { fill: var(--ink); font-family: var(--font-mono); font-size: 14px; letter-spacing: .08em; opacity: .75; }
.hd.hot { fill: var(--accent); opacity: 1; }

.chip { fill: rgba(241, 236, 216, .05); stroke: var(--ink); stroke-opacity: .45; stroke-width: 1; }
.chip.out { stroke: var(--accent-2); stroke-opacity: 1; fill: rgba(143, 227, 106, .08); }
.ct { fill: var(--ink); font-family: var(--font-mono); font-size: 12px; }
.ct.out { fill: var(--accent-2); }
.ar { stroke: var(--ink); stroke-width: 1; opacity: .4; }

.cell { fill: var(--ink); }
.cell.sg { fill: var(--accent); }
.cell.hotc { fill: var(--sun); filter: drop-shadow(0 0 4px var(--sun)); }

.arc { fill: none; stroke: var(--accent); stroke-width: 2; stroke-dasharray: 6 6; animation: flow 1.2s linear infinite; }
.pulse { fill: var(--accent); filter: drop-shadow(0 0 6px var(--accent)); }
.tool { fill: var(--bg); stroke: var(--accent); stroke-width: 1.2; }
.tt { fill: var(--accent); font-family: var(--font-mono); font-size: 12px; }

.fold { fill: none; stroke: var(--accent); stroke-width: 3; stroke-linecap: round; filter: drop-shadow(0 0 4px var(--accent)); }
.contact { fill: var(--sun); filter: drop-shadow(0 0 4px var(--sun)); }
.cline { stroke: var(--sun); stroke-width: 1.2; stroke-dasharray: 3 3; opacity: .8; }

.caps { display: grid; grid-template-columns: 220fr 400fr 220fr; margin: .7rem 0 0; padding: 0 calc(100% * 40 / 960); font-family: var(--font-mono); font-size: .74rem; text-align: center; }
.caps span { opacity: .7; }
.caps .mid span { opacity: .5; }
.caps b { color: var(--accent); font-weight: 500; }

.path { display: flex; justify-content: center; gap: 0; margin-top: 1.3rem; font-family: var(--font-mono); }
.m { display: flex; flex-direction: column; align-items: center; gap: .15rem; padding: 0 1.4rem; position: relative; }
.m + .m::before { content: "→"; position: absolute; left: -.45rem; top: .05rem; opacity: .35; }
.m b { font-size: .85rem; font-weight: 500; color: var(--ink); opacity: .85; }
.m span { font-size: .66rem; opacity: .5; }
.m.last b { color: var(--accent); opacity: 1; }

@keyframes flow { to { stroke-dashoffset: -12; } }
</style>
