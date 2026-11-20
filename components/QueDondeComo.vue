<script setup lang="ts">
// Técnicas de interpretabilidad según la pregunta que responden (Barez et al., §2–3):
//   evaluación conductual → ¿qué? · atribución y sondeo → ¿dónde? · análisis mecanístico → ¿cómo?
const heat = [0.15, 0.85, 0.3, 0.1, 0.6, 0.2]
const act = [0.3, 0.5, 0.95, 0.4, 0.25, 0.6]
const L = [30, 80, 130].map(x => ({ x, ys: [28, 55, 82] }))
const hot = new Set(['0-1-0', '1-0-1'])
const net = L.slice(0, -1).flatMap((a, l) => a.ys.flatMap((y1, i) => L[l + 1].ys.map((y2, j) => ({
  x1: a.x, y1, x2: L[l + 1].x, y2, hot: hot.has(`${l}-${i}-${j}`),
}))))
const hotN = new Set(['0-1', '1-0', '2-1'])
// morph desde la slide anterior (BehavMech): caja negra → ¿qué?, caja abierta → ¿cómo?
const vtT = ['vt-beh-t', undefined, 'vt-mech-t']
const cols = [
  { q: '¿Qué?', cat: 'Evaluación conductual', chips: ['benchmarks', 'red-teaming', 'variar el input'], ev: 'salidas' },
  { q: '¿Dónde?', cat: 'Atribución y sondeo', chips: ['saliency · SHAP', 'integrated gradients', 'probes'], ev: 'correlación' },
  { q: '¿Cómo?', cat: 'Análisis mecanístico', chips: ['activation patching', 'ablación', 'circuitos'], ev: 'causa', hot: true },
]
</script>

<template>
  <div class="qdc">
    <div v-for="(c, k) in cols" :key="k" class="card" :class="{ hot: c.hot }">
      <div class="q">{{ c.q }}</div>
      <div class="cat" :style="{ viewTransitionName: vtT[k] }">{{ c.cat }}</div>

      <!-- ¿qué? caja negra -->
      <svg v-if="k === 0" viewBox="0 0 200 110" class="fig" style="view-transition-name: vt-beh">
        <rect x="6" y="42" width="34" height="24" rx="12" class="chip" /><text x="23" y="58" class="ct" text-anchor="middle">x</text>
        <line x1="42" y1="54" x2="68" y2="54" class="ar" />
        <rect x="70" y="22" width="60" height="64" rx="6" class="black" /><text x="100" y="64" class="qm" text-anchor="middle">?</text>
        <line x1="132" y1="54" x2="158" y2="54" class="ar" />
        <rect x="160" y="42" width="34" height="24" rx="12" class="chip out" /><text x="177" y="58" class="ct out" text-anchor="middle">y</text>
        <circle r="3.5" class="pulse"><animateMotion dur="2.4s" repeatCount="indefinite" path="M42,54 L68,54" /></circle>
        <circle r="3.5" class="pulse out"><animateMotion dur="2.4s" begin="1.2s" repeatCount="indefinite" path="M132,54 L158,54" /></circle>
      </svg>

      <!-- ¿dónde? atribución sobre el input + probe sobre una capa -->
      <svg v-else-if="k === 1" viewBox="0 0 200 110" class="fig">
        <text x="2" y="30" class="lb">capa ℓ</text>
        <rect v-for="(a, i) in act" :key="'a' + i" :x="46 + i * 24" y="18" width="20" height="18" rx="3" class="cell" :style="{ opacity: a }" />
        <circle cx="104" cy="27" r="15" class="lens" /><line x1="115" y1="38" x2="124" y2="47" class="lens-h" />
        <text x="198" y="60" class="lb hot" text-anchor="end">decodificable</text>
        <text x="2" y="92" class="lb">input</text>
        <rect v-for="(h, i) in heat" :key="'h' + i" :x="46 + i * 24" y="80" width="20" height="18" rx="3" class="heat" :style="{ opacity: 0.15 + h * 0.85 }" />
        <line v-for="i in 6" :key="'l' + i" :x1="56 + (i - 1) * 24" y1="78" :x2="56 + (i - 1) * 24" y2="40" class="ar dim" />
      </svg>

      <!-- ¿cómo? circuito + intervención -->
      <svg v-else viewBox="0 0 200 110" class="fig" style="view-transition-name: vt-mech">
        <line v-for="(e, i) in net" :key="i" v-bind="e" :class="e.hot ? 'eh' : 'e'" />
        <g v-for="(c2, l) in L" :key="l">
          <circle v-for="(y, j) in c2.ys" :key="j" :cx="c2.x" :cy="y" r="6" :class="hotN.has(`${l}-${j}`) ? 'nh' : 'n'" />
        </g>
        <circle cx="80" cy="28" r="9" class="patch" />
        <line x1="140" y1="55" x2="154" y2="55" class="ar" />
        <path d="M160,80 C168,30 178,84 186,40 C192,14 200,60 204,30" class="out-shape">
          <animate attributeName="d" values="M160,80 C168,30 178,84 186,40 C192,14 200,60 204,30;M160,80 C158,24 206,22 200,60 C196,86 172,76 182,46;M160,80 C168,30 178,84 186,40 C192,14 200,60 204,30" dur="4s" repeatCount="indefinite" />
        </path>
        <text x="80" y="104" class="lb hot" text-anchor="middle">intervenir</text>
      </svg>

      <div class="chips">
        <span v-for="t in c.chips" :key="t">{{ t }}</span>
      </div>
      <div class="ev">{{ c.ev }}</div>
    </div>

    <div class="axis">
      <span>Describir</span>
      <i />
      <span class="hot">Intervenir</span>
    </div>
  </div>
</template>

<style scoped>
.qdc { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.4rem; }
.card { border: 1px solid var(--accent-soft); border-radius: 8px; padding: 1rem 1.1rem .9rem; background: rgba(0, 0, 0, .22); display: flex; flex-direction: column; align-items: center; gap: .55rem; }
.card.hot { border-color: var(--accent); box-shadow: 0 0 22px var(--accent-soft); }
.q { font-size: 1.9rem; font-weight: 300; line-height: 1; color: var(--ink); }
.card.hot .q { color: var(--accent); }
.cat { font-family: var(--font-mono); font-size: .85rem; letter-spacing: .03em; opacity: .8; }
.fig { width: 100%; height: auto; display: block; overflow: visible; color: var(--ink); margin: .3rem 0; }
.chips { display: flex; flex-wrap: wrap; justify-content: center; gap: .35rem; }
.chips span { font-family: var(--font-mono); font-size: .68rem; padding: .18rem .55rem; border-radius: 999px; border: 1px solid var(--accent-soft); opacity: .85; }
.card.hot .chips span { border-color: var(--accent); color: var(--accent); opacity: 1; }
.ev { font-family: var(--font-mono); font-size: .66rem; letter-spacing: .1em; text-transform: uppercase; opacity: .45; margin-top: .1rem; }
.card.hot .ev { color: var(--accent); opacity: 1; }

.axis { grid-column: 1 / -1; display: flex; align-items: center; gap: .8rem; font-family: var(--font-mono); font-size: .8rem; margin-top: .2rem; }
.axis span { opacity: .55; }
.axis span.hot { color: var(--accent); opacity: 1; }
.axis i { flex: 1; height: 2px; background: linear-gradient(90deg, rgba(241, 236, 216, .15), var(--accent)); position: relative; }
.axis i::after { content: ""; position: absolute; right: -2px; top: -4px; border-left: 8px solid var(--accent); border-top: 5px solid transparent; border-bottom: 5px solid transparent; }

.chip { fill: rgba(241, 236, 216, .05); stroke: var(--ink); stroke-opacity: .5; }
.chip.out { stroke: var(--teal); stroke-opacity: 1; }
.ct { fill: var(--ink); font-family: var(--font-mono); font-size: 12px; }
.ct.out { fill: var(--teal); }
.ar { stroke: var(--ink); stroke-width: 1; opacity: .45; }
.ar.dim { opacity: .15; stroke-dasharray: 2 3; }
.black { fill: #020504; stroke: var(--ink); stroke-opacity: .35; }
.qm { fill: var(--ink); font-family: var(--font-mono); font-size: 28px; opacity: .3; }
.pulse { fill: var(--ink); }
.pulse.out { fill: var(--teal); }

.lb { fill: var(--ink); font-family: var(--font-mono); font-size: 10px; opacity: .5; }
.lb.hot { fill: var(--accent); opacity: 1; }
.cell { fill: var(--teal); }
.heat { fill: var(--coral); }
.lens { fill: rgba(255, 194, 75, .08); stroke: var(--accent); stroke-width: 1.6; }
.lens-h { stroke: var(--accent); stroke-width: 3; stroke-linecap: round; }

.e { stroke: var(--ink); stroke-width: .6; opacity: .15; }
.eh { stroke: var(--accent); stroke-width: 2; }
.n { fill: var(--bg); stroke: var(--ink); stroke-opacity: .45; }
.nh { fill: var(--accent); }
.patch { fill: none; stroke: var(--sun); stroke-width: 2; filter: drop-shadow(0 0 5px var(--sun)); animation: beat 1.8s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }
.out-shape { fill: none; stroke: var(--accent); stroke-width: 2.2; stroke-linecap: round; }
@keyframes beat { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.35); } }
</style>
