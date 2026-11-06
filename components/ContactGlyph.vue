<script setup lang="ts">
// Hairpin esquemático: i y j lejos en secuencia, cerca en el espacio (coordenadas finales).
const top = [20, 45, 70, 95, 120, 145, 170].map(x => ({ x, y: 30 }))
const turn = [{ x: 192, y: 40 }, { x: 200, y: 60 }, { x: 192, y: 80 }]
const bot = [170, 145, 120, 95, 70, 45, 20].map(x => ({ x, y: 90 }))
const pts = [...top, ...turn, ...bot]
const path = 'M' + pts.map(p => `${p.x},${p.y}`).join(' L')
const I = top[2]
const J = bot[4]
</script>

<template>
  <div class="cg">
    <svg viewBox="0 0 260 112" role="img" aria-label="contacto entre residuos i y j en la estructura final">
      <path :d="path" class="bb" />
      <circle v-for="(p, k) in pts" :key="k" :cx="p.x" :cy="p.y" r="3.2" class="res" />
      <line :x1="I.x" :y1="I.y + 6" :x2="J.x" :y2="J.y - 6" class="d" />
      <circle :cx="I.x" :cy="I.y" r="6" class="hl" />
      <circle :cx="J.x" :cy="J.y" r="6" class="hl" />
      <text :x="I.x" :y="I.y - 11" class="lab" text-anchor="middle">i</text>
      <text :x="J.x" :y="J.y + 19" class="lab" text-anchor="middle">j</text>
      <text :x="I.x + 9" y="64" class="dl">d(i, j) &lt; τ</text>
      <text x="214" y="64" class="dim">N → C</text>
    </svg>
    <div class="cap">contacto en las <b>coordenadas finales</b> · Cβ, τ = 8 Å</div>
  </div>
</template>

<style scoped>
.cg { position: absolute !important; top: 2.2rem; right: 3rem; width: 230px; z-index: 2; }
svg { width: 100%; height: auto; display: block; overflow: visible; }
.bb { fill: none; stroke: var(--ink); stroke-width: 1.4; opacity: .35; stroke-linejoin: round; }
.res { fill: var(--ink); opacity: .55; }
.hl { fill: rgba(255, 194, 75, .25); stroke: var(--sun); stroke-width: 1.6; }
.d { stroke: var(--sun); stroke-width: 1.4; stroke-dasharray: 3 3; }
.lab { fill: var(--sun); font-family: var(--font-mono); font-size: 13px; font-weight: 500; }
.dl { fill: var(--sun); font-family: var(--font-mono); font-size: 11px; }
.dim { fill: var(--ink); font-family: var(--font-mono); font-size: 9px; opacity: .4; }
.cap { font-family: var(--font-mono); font-size: 10px; line-height: 1.35; opacity: .65; margin-top: .25rem; }
.cap b { font-weight: 500; }
</style>
