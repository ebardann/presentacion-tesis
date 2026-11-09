<script setup lang="ts">
// Tesis en tres pasos: AF3 congelado → intervenir una feature → cambio en coordenadas finales.
const N = 6, S = 10, C = 8
const grid = Array.from({ length: N * N }, (_, k) => ({ r: Math.floor(k / N), c: k % N }))
// hairpin: i y j se acercan en la estructura final
const top = [0, 1, 2, 3, 4].map(k => ({ x: 618 + k * 18, y: 52 }))
const bot = [4, 3, 2, 1, 0].map(k => ({ x: 618 + k * 18, y: 100 }))
const pts = [...top, { x: 708, y: 62 }, { x: 712, y: 76 }, { x: 708, y: 90 }, ...bot]
const path = 'M' + pts.map(p => `${p.x},${p.y}`).join(' L')
const I = top[1], J = bot[3]
</script>

<template>
  <svg class="ts" viewBox="0 0 900 128" role="img" aria-label="AF3 congelado, intervenir una feature, cambio en coordenadas finales">
    <defs>
      <marker id="ts-arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
        <path d="M0,0 L10,5 L0,10 z" class="ah" />
      </marker>
    </defs>

    <!-- 1 · AF3 congelado -->
    <g>
      <rect x="0" y="10" width="250" height="122" rx="6" class="card" />
      <text x="18" y="34" class="n">01</text>
      <text x="48" y="34" class="h">AF3 congelado</text>
      <g transform="translate(40,52)">
        <rect v-for="k in 4" :key="k" :x="(k - 1) * 40" y="8" width="30" height="36" rx="3" class="blk" />
        <line v-for="k in 3" :key="'w' + k" :x1="(k - 1) * 40 + 30" y1="26" :x2="k * 40" y2="26" class="wire" />
        <text x="75" y="58" class="sub" text-anchor="middle">pesos fijos · sólo forward passes</text>
      </g>
    </g>
    <line x1="256" y1="75" x2="318" y2="75" class="flow" marker-end="url(#ts-arr)" />

    <!-- 2 · una feature -->
    <g>
      <rect x="325" y="10" width="250" height="122" rx="6" class="card hot" />
      <text x="343" y="34" class="n">02</text>
      <text x="373" y="34" class="h">una feature</text>
      <rect v-for="g in grid" :key="g.r + '-' + g.c" :x="345 + g.c * S" :y="50 + g.r * S" :width="C" :height="C" rx="1.5"
        :class="g.r === 1 && g.c === 4 ? 'zij' : 'z'" />
      <text x="414" y="62" class="eq">h' = h + m⊙(h_src − h)</text>
      <text x="414" y="82" class="sub">patch · ablación · rescate</text>
      <text x="414" y="98" class="sub">capa · recycle · par (i, j)</text>
    </g>
    <line x1="581" y1="75" x2="643" y2="75" class="flow" marker-end="url(#ts-arr)" />

    <!-- 3 · coordenadas finales -->
    <g>
      <rect x="650" y="10" width="250" height="122" rx="6" class="card" />
      <text x="668" y="34" class="n">03</text>
      <text x="698" y="34" class="h">coordenadas finales</text>
      <path :d="path" class="bb" transform="translate(48,-4)" />
      <g transform="translate(48,-4)">
        <circle v-for="(p, k) in pts" :key="k" :cx="p.x" :cy="p.y" r="2.6" class="res" />
        <line :x1="I.x" :y1="I.y + 5" :x2="J.x" :y2="J.y - 5" class="d" />
        <circle :cx="I.x" :cy="I.y" r="5" class="hl" />
        <circle :cx="J.x" :cy="J.y" r="5" class="hl" />
      </g>
      <text x="790" y="70" class="sub">d(i, j) cambia</text>
      <text x="790" y="86" class="sub">resto intacto</text>
      <text x="668" y="116" class="sub">difusión → X · seeds fijas</text>
    </g>
  </svg>
</template>

<style scoped>
.ts { width: 100%; height: auto; display: block; color: var(--ink); overflow: visible; }
.card { fill: rgba(0, 0, 0, .25); stroke: var(--accent-soft); stroke-width: 1.2; }
.card.hot { stroke: var(--accent); }
.n { fill: var(--accent); font-family: var(--font-mono); font-size: 12px; font-weight: 500; letter-spacing: .06em; }
.h { fill: currentColor; font-family: var(--font-mono); font-size: 14px; }
.sub { fill: currentColor; font-family: var(--font-mono); font-size: 9.5px; opacity: .6; }
.eq { fill: var(--accent); font-family: var(--font-mono); font-size: 10px; }
.blk { fill: rgba(143, 227, 106, .08); stroke: var(--ink); stroke-width: 1; opacity: .5; }
.wire { stroke: var(--ink); stroke-width: 1; opacity: .4; }
.flow { stroke: var(--accent); stroke-width: 1.4; opacity: .7; }
.ah { fill: var(--accent); }
.z { fill: var(--ink); opacity: .12; }
.zij { fill: var(--sun); }
.bb { fill: none; stroke: var(--ink); stroke-width: 1.2; opacity: .35; stroke-linejoin: round; }
.res { fill: var(--ink); opacity: .55; }
.hl { fill: rgba(255, 194, 75, .25); stroke: var(--sun); stroke-width: 1.4; }
.d { stroke: var(--sun); stroke-width: 1.3; stroke-dasharray: 3 3; }
</style>
