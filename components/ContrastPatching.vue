<script setup lang="ts">
// Contrast pairs + activation patching (ejemplo clásico en LLMs):
// "Michael Jordan juega al deporte de" vs "Tom Brady juega al deporte de".
// Se copia la activación del token del nombre (capa ℓ) de la corrida MJ a la corrida TB:
// el contexto compartido ("deportes", "español") queda controlado; sólo cambia "qué deporte".
const ctx = ['juega', 'al', 'deporte', 'de']
const NX = 120, NW = 128, TW = 66, GAP = 6
const tx = (k: number) => NX + NW + GAP + k * (TW + GAP)          // x de los tokens de contexto
const OUTX = tx(4) + 40
const rows = [
  { y: 38, tag: 'A · source', name: 'Michael Jordan', out: 'baloncesto', kind: 'a' },
  { y: 108, tag: 'B · target', name: 'Tom Brady', out: 'fútbol americano', kind: 'b' },
  { y: 178, tag: 'B + patch', name: 'Tom Brady', out: 'baloncesto', kind: 'p' },
]
const CELL = { w: 26, h: 12, dy: 20 }   // activación en la capa ℓ, bajo cada token
const ncx = NX + NW / 2
</script>

<template>
  <svg class="cp" viewBox="0 0 900 206" role="img" aria-label="contrast pair Michael Jordan / Tom Brady y patch de la activación del nombre">
    <defs>
      <marker id="cp-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="currentColor" /></marker>
      <marker id="cp-t" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" class="f-teal" /></marker>
    </defs>

    <!-- anotaciones arriba -->
    <text :x="ncx" y="10" class="ann hot" text-anchor="middle">lo único que cambia</text>
    <text :x="(tx(0) + tx(3) + TW) / 2 + 20" y="10" class="ann" text-anchor="middle">idéntico en ambos → controla «deportes», «español»</text>
    <line :x1="tx(0)" y1="16" :x2="tx(3) + TW" y2="16" class="brace" />

    <g v-for="r in rows" :key="r.tag">
      <text x="0" :y="r.y + 4" class="tag" :class="'t-' + r.kind">{{ r.tag }}</text>
      <!-- token del nombre -->
      <rect :x="NX" :y="r.y - 13" :width="NW" height="26" rx="4" class="tok name" :class="r.kind === 'a' ? 'na' : 'nb'" />
      <text :x="ncx" :y="r.y + 5" class="tt" text-anchor="middle">{{ r.name }}</text>
      <!-- contexto -->
      <g v-for="(c, k) in ctx" :key="c">
        <rect :x="tx(k)" :y="r.y - 13" :width="TW" height="26" rx="4" class="tok" />
        <text :x="tx(k) + TW / 2" :y="r.y + 5" class="tt" text-anchor="middle">{{ c }}</text>
      </g>
      <!-- activaciones en la capa ℓ -->
      <text v-if="r.kind === 'a'" :x="tx(3) + TW + 8" :y="r.y + CELL.dy + 10" class="ell">← activación en la capa ℓ</text>
      <rect :x="ncx - CELL.w / 2" :y="r.y + CELL.dy" :width="CELL.w" :height="CELL.h" rx="2"
        class="act" :class="r.kind === 'b' ? 'ab' : 'aa'" />
      <rect v-for="(c, k) in ctx" :key="'c' + k" :x="tx(k) + TW / 2 - CELL.w / 2" :y="r.y + CELL.dy" :width="CELL.w" :height="CELL.h" rx="2" class="act ac" />
      <!-- salida -->
      <line :x1="tx(3) + TW + 6" :y1="r.y" :x2="OUTX - 6" :y2="r.y" class="w" marker-end="url(#cp-a)" />
      <rect :x="OUTX" :y="r.y - 15" width="168" height="30" rx="5" class="out" :class="'o-' + r.kind" />
      <text :x="OUTX + 84" :y="r.y + 5" class="ot" text-anchor="middle">{{ r.out }}{{ r.kind === 'p' ? '  ✓' : '' }}</text>
    </g>

    <!-- copia: activación del nombre en A → misma posición en B + patch -->
    <path :d="`M${ncx - CELL.w / 2 - 2},${38 + CELL.dy + CELL.h / 2} H${NX - 22} V${178 + CELL.dy + CELL.h / 2} H${ncx - CELL.w / 2 - 4}`" class="copy" marker-end="url(#cp-t)" />
    <text :x="NX - 26" y="136" class="cpt" text-anchor="end">patch</text>
    <text :x="NX - 26" y="148" class="cpt" text-anchor="end">MJ → TB</text>

  </svg>
</template>

<style scoped>
.cp { width: 100%; height: auto; display: block; color: var(--ink); overflow: visible; }
.tag { font-family: var(--font-mono); font-size: 11px; font-weight: 500; }
.t-a { fill: var(--leaf); }
.t-b { fill: var(--coral); }
.t-p { fill: var(--sun); }
.tok { fill: rgba(241, 236, 216, .05); stroke: rgba(241, 236, 216, .3); stroke-width: 1; }
.tok.na { fill: rgba(143, 227, 106, .14); stroke: var(--leaf); }
.tok.nb { fill: rgba(255, 111, 89, .12); stroke: var(--coral); }
.tt { fill: currentColor; font-family: var(--font-body); font-size: 13px; }
.act { stroke-width: 1; }
.aa { fill: rgba(143, 227, 106, .6); stroke: var(--leaf); }
.ab { fill: rgba(255, 111, 89, .45); stroke: var(--coral); }
.ac { fill: rgba(241, 236, 216, .15); stroke: rgba(241, 236, 216, .35); }
.ell { fill: currentColor; font-family: var(--font-mono); font-size: 10px; opacity: .5; }
.w { stroke: currentColor; stroke-width: 1.1; opacity: .4; }
.out { stroke-width: 1.3; }
.o-a { fill: rgba(143, 227, 106, .12); stroke: var(--leaf); }
.o-b { fill: rgba(255, 111, 89, .1); stroke: var(--coral); }
.o-p { fill: rgba(255, 194, 75, .14); stroke: var(--sun); }
.ot { fill: currentColor; font-family: var(--font-mono); font-size: 12.5px; }
.copy { fill: none; stroke: var(--teal); stroke-width: 1.6; stroke-dasharray: 4 3; }
.f-teal { fill: var(--teal); }
.cpt { fill: var(--teal); font-family: var(--font-mono); font-size: 10px; }
.ann { fill: currentColor; font-family: var(--font-mono); font-size: 10px; opacity: .55; }
.ann.hot { fill: var(--sun); opacity: .9; }
.brace { stroke: currentColor; stroke-width: 1; opacity: .3; }
</style>
