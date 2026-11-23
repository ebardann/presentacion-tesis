<script setup lang="ts">
// Si entendiéramos AlphaFold por completo: la caja abierta al centro y cuatro implicaciones alrededor.
const left = [
  { k: 'prec', t: 'Precisión', q: 'predecir mejor', d: 'saber por qué falla una predicción y corregir la causa: MSA, templates o el modelo' },
  { k: 'ctrl', t: 'Control', q: 'dirigir la predicción', d: 'cambiar un contacto o pedir un estado alternativo a propósito, no por azar' },
]
const right = [
  { k: 'drug', t: 'Diseño de fármacos', q: 'mejores candidatos', d: 'saber qué sostiene una pose proteína–ligando antes de sintetizar y probar' },
  { k: 'disc', t: 'Descubrimiento', q: 'aprender del modelo', d: 'reglas geométricas que aprendió → hipótesis biológicas para verificar' },
]
// red dentro de la caja: 3 capas, una vía resaltada
const layers = [0, 1, 2, 3].map(l => [0, 1, 2].map(r => ({ x: 404 + l * 50, y: 132 + r * 34 })))
const path = [[0, 2], [1, 1], [2, 0], [3, 1]]
const edges = layers.slice(0, -1).flatMap((col, l) => col.flatMap((a, i) => layers[l + 1].map((b, j) => ({ a, b, hot: path[l][1] === i && path[l + 1][1] === j }))))
</script>

<template>
  <div class="imp">
    <div class="side">
      <div v-for="c in left" :key="c.k" class="card">
        <svg class="ico" viewBox="0 0 40 40" aria-hidden="true">
          <template v-if="c.k === 'prec'">
            <!-- diana -->
            <circle cx="20" cy="20" r="15" class="soft" /><circle cx="20" cy="20" r="9.5" />
            <circle cx="20" cy="20" r="3.5" class="hot" />
            <line x1="34" y1="6" x2="22.5" y2="17.5" class="hot-s" />
          </template>
          <template v-else>
            <path d="M5,32 C12,8 18,8 20,20 S30,34 35,10" class="bb" />
            <circle cx="10" cy="20" r="2.6" class="hot" /><circle cx="29" cy="24" r="2.6" class="hot" />
            <path d="M14,20 L25,23" class="hot-s" marker-end="url(#imp-a)" />
          </template>
        </svg>
        <div><div class="t">{{ c.t }}</div><div class="q">{{ c.q }}</div><div class="d">{{ c.d }}</div></div>
      </div>
    </div>

    <svg viewBox="300 40 360 280" class="core" role="img" aria-label="AlphaFold 3 abierto: una vía interna resaltada conecta la entrada con la estructura">
      <defs>
        <marker id="imp-a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--leaf)" /></marker>
      </defs>
      <!-- rayos hacia las cuatro implicaciones -->
      <line v-for="(p, i) in [[370, 120, 300, 90], [370, 220, 300, 260], [590, 120, 660, 90], [590, 220, 660, 260]]" :key="'s' + i"
        :x1="p[0]" :y1="p[1]" :x2="p[2]" :y2="p[3]" class="spoke" />
      <!-- caja abierta -->
      <rect x="370" y="104" width="220" height="132" rx="8" class="box" />
      <path d="M370,104 L392,64 L612,64 L590,104" class="lid" />
      <text x="480" y="94" class="lbl" text-anchor="middle">AF3 · caja abierta</text>
      <line v-for="(e, i) in edges" :key="'e' + i" :x1="e.a.x" :y1="e.a.y" :x2="e.b.x" :y2="e.b.y" :class="e.hot ? 'edge hot-e' : 'edge'" />
      <template v-for="(col, l) in layers" :key="'l' + l">
        <circle v-for="(n, r) in col" :key="r" :cx="n.x" :cy="n.y" r="5" :class="path[l][1] === r ? 'node on' : 'node'" />
      </template>
      <circle r="4" class="pulse"><animateMotion dur="2.4s" repeatCount="indefinite"
        :path="'M' + path.map(([l, r]) => `${layers[l][r].x},${layers[l][r].y}`).join(' L')" /></circle>
      <text x="380" y="262" class="io">MSA · secuencia</text>
      <text x="580" y="262" class="io" text-anchor="end">→ estructura 3D</text>
      <text x="480" y="300" class="cap" text-anchor="middle">cada predicción con su porqué</text>
    </svg>

    <div class="side">
      <div v-for="c in right" :key="c.k" class="card">
        <svg class="ico" viewBox="0 0 40 40" aria-hidden="true">
          <template v-if="c.k === 'drug'">
            <!-- molécula (ligando) entrando a un bolsillo -->
            <path d="M4,10 L4,34 L36,34 L36,10 M4,10 C12,10 12,24 20,24 C28,24 28,10 36,10" class="soft" />
            <line x1="14" y1="12" x2="20" y2="18" class="hot-s" /><line x1="20" y1="18" x2="26" y2="12" class="hot-s" />
            <circle cx="14" cy="12" r="2.4" class="hot" /><circle cx="20" cy="18" r="2.4" class="hot" /><circle cx="26" cy="12" r="2.4" class="hot" />
          </template>
          <template v-else>
            <circle cx="20" cy="17" r="9" /><line x1="16" y1="30" x2="24" y2="30" /><line x1="17" y1="34" x2="23" y2="34" />
            <circle cx="20" cy="17" r="3" class="hot" />
          </template>
        </svg>
        <div><div class="t">{{ c.t }}</div><div class="q">{{ c.q }}</div><div class="d">{{ c.d }}</div></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.imp { display: grid; grid-template-columns: 1fr 1.15fr 1fr; align-items: center; gap: .6rem; }
.side { display: flex; flex-direction: column; gap: 1.1rem; }
.card { display: flex; gap: .8rem; align-items: flex-start; border: 1px solid rgba(143, 227, 106, .22); border-left: 2px solid var(--leaf);
  border-radius: 6px; padding: .7rem .85rem; background: linear-gradient(90deg, rgba(143, 227, 106, .07), rgba(0, 0, 0, .25) 60%); }
.ico { width: 2.1rem; height: 2.1rem; flex: 0 0 auto; overflow: visible; }
.ico line, .ico circle, .ico rect, .ico path { fill: none; stroke: var(--ink); stroke-width: 1.3; opacity: .7; }
.ico .soft { opacity: .3; }
.ico .bb { stroke-linecap: round; }
.ico .hot { fill: var(--leaf); stroke: var(--leaf); opacity: 1; }
.ico .hot-s { stroke: var(--leaf); stroke-width: 1.6; opacity: 1; stroke-linecap: round; }
.t { font-size: 1.05rem; font-weight: 400; line-height: 1.2; }
.q { font-family: var(--font-mono); font-size: .7rem; color: var(--leaf); margin-top: .15rem; }
.d { font-size: .72rem; line-height: 1.4; opacity: .65; margin-top: .35rem; font-weight: 300; }

.core { width: 100%; height: auto; overflow: visible; color: var(--ink); }
.spoke { stroke: var(--leaf); stroke-width: 1.2; stroke-dasharray: 4 4; opacity: .55; animation: flow 1.4s linear infinite; }
.box { fill: rgba(143, 227, 106, .04); stroke: var(--leaf); stroke-width: 1.4; filter: drop-shadow(0 0 10px rgba(143, 227, 106, .25)); }
.lid { fill: rgba(143, 227, 106, .06); stroke: var(--leaf); stroke-width: 1.2; stroke-opacity: .5; stroke-dasharray: 3 3; }
.lbl { fill: var(--leaf); font-family: var(--font-mono); font-size: 11px; letter-spacing: .06em; }
.edge { stroke: var(--ink); stroke-width: .8; opacity: .14; }
.edge.hot-e { stroke: var(--sun); stroke-width: 2; opacity: .95; filter: drop-shadow(0 0 3px var(--sun)); }
.node { fill: var(--bg); stroke: var(--ink); stroke-width: 1.1; opacity: .5; }
.node.on { fill: var(--sun); stroke: var(--sun); opacity: 1; }
.pulse { fill: #fff; filter: drop-shadow(0 0 5px var(--sun)); }
.io { fill: var(--ink); font-family: var(--font-mono); font-size: 10px; opacity: .55; }
.cap { fill: var(--leaf); font-family: var(--font-mono); font-size: 12px; }

@keyframes flow { to { stroke-dashoffset: -16; } }
@media (prefers-reduced-motion: reduce) { .spoke { animation: none; } }
</style>
