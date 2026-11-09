<script setup lang="ts">
// Activation patching, versión genérica:
// corrida A (source) y B (target); en la capa ℓ se reemplaza h_B por h' = h_B + m ⊙ (h_A − h_B)
// y se reanuda el resto de la red. El efecto se mide como fracción del cambio A↔B recuperado.
const rows = [
  { y: 42, tag: 'A · source', x: 'x_A', kind: 'a' },
  { y: 128, tag: 'B · target', x: 'x_B', kind: 'b' },
  { y: 214, tag: 'B + patch', x: 'x_B', kind: 'p' },
]
const mask = [0, 1, 1, 0, 0, 1]
const CX = 236, CS = 12, CW = 10, CH = 24
function cellKind(row: string, k: number) {
  if (row === 'a') return 'a'
  if (row === 'b') return 'b'
  return mask[k] ? 'a' : 'b'
}
// salida escalar y: A alto, B bajo, patched recupera ~80 %
const GX0 = 420, GX1 = 540
const yval = { a: 0.88, b: 0.14, p: 0.73 }
const gx = (v: number) => GX0 + v * (GX1 - GX0)
</script>

<template>
  <svg class="pc" viewBox="0 0 560 280" role="img" aria-label="activation patching genérico: copiar h de la corrida A a la corrida B en la capa ℓ">
    <defs>
      <marker id="pc-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="currentColor" /></marker>
      <marker id="pc-t" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" class="f-teal" /></marker>
    </defs>

    <text x="152" y="12" class="col" text-anchor="middle">capas previas</text>
    <text :x="CX + 35" y="12" class="col hot" text-anchor="middle">capa ℓ · h</text>
    <text x="352" y="12" class="col" text-anchor="middle">resto</text>
    <text :x="(GX0 + GX1) / 2" y="12" class="col" text-anchor="middle">output y</text>

    <g v-for="r in rows" :key="r.tag">
      <text x="0" :y="r.y + 4" class="tag" :class="'t-' + r.kind">{{ r.tag }}</text>
      <text x="92" :y="r.y + 4" class="mono" text-anchor="middle">{{ r.x }}</text>
      <line x1="108" :y1="r.y" x2="124" :y2="r.y" class="w" marker-end="url(#pc-a)" />
      <rect x="128" :y="r.y - 15" width="48" height="30" rx="4" class="box" :class="r.kind === 'a' ? 'a' : 'b'" />
      <line x1="176" :y1="r.y" x2="196" :y2="r.y" class="w" />
      <rect x="196" :y="r.y - 15" width="28" height="30" rx="4" class="box" :class="r.kind === 'a' ? 'a' : 'b'" />
      <line x1="224" :y1="r.y" x2="232" :y2="r.y" class="w" />
      <!-- vector h en la capa ℓ -->
      <rect v-for="(mk, k) in mask" :key="k" :x="CX + k * CS" :y="r.y - CH / 2" :width="CW" :height="CH" rx="2" class="cell" :class="'c-' + cellKind(r.kind, k)" />
      <line :x1="CX + 6 * CS + 2" :y1="r.y" :x2="324" :y2="r.y" class="w" marker-end="url(#pc-a)" />
      <rect x="328" :y="r.y - 15" width="48" height="30" rx="4" class="box" :class="r.kind" />
      <line x1="376" :y1="r.y" x2="410" :y2="r.y" class="w" marker-end="url(#pc-a)" />
      <!-- output escalar -->
      <line :x1="GX0" :y1="r.y" :x2="GX1" :y2="r.y" class="track" />
      <circle :cx="gx(yval[r.kind])" :cy="r.y" r="6" class="mk" :class="'m-' + r.kind" />
      <text :x="gx(yval[r.kind])" :y="r.y - 11" class="yl" text-anchor="middle">{{ r.kind === 'a' ? 'y_A' : r.kind === 'b' ? 'y_B' : "y'" }}</text>
    </g>

    <!-- etiquetas de h -->
    <text :x="CX + 35" :y="42 + 26" class="h t-a" text-anchor="middle">h_A</text>
    <text :x="CX + 35" :y="128 + 26" class="h t-b" text-anchor="middle">h_B</text>
    <text :x="CX + 35" :y="214 + 26" class="h t-p" text-anchor="middle">h'</text>

    <!-- máscara -->
    <text :x="CX - 8" y="176" class="h t-teal" text-anchor="end">m</text>
    <rect v-for="(mk, k) in mask" :key="'m' + k" :x="CX + k * CS" y="168" :width="CW" height="10" rx="2" class="mcell" :class="{ on: mk }" />

    <!-- copia A → patched -->
    <path :d="`M${CX + 6 * CS + 6},${42 + 8} C 318,70 318,180 ${CX + 6 * CS + 4},${214 - 8}`" class="copy" marker-end="url(#pc-t)" />
    <text x="322" y="96" class="cp">copiar h_A</text>
    <text x="322" y="108" class="cp">donde m = 1</text>

    <!-- efecto -->
    <line :x1="gx(yval.b)" y1="248" :x2="gx(yval.a)" y2="248" class="span" />
    <line :x1="gx(yval.b)" y1="248" :x2="gx(yval.p)" y2="248" class="span on" />
    <text x="0" y="272" class="eq">efecto = (y' − y_B) / (y_A − y_B) ≈ 0.8 → h en ℓ (bajo m) explica ~80 % del cambio</text>
  </svg>
</template>

<style scoped>
.pc { width: 100%; height: auto; display: block; color: var(--ink); overflow: visible; }
.col { fill: currentColor; font-family: var(--font-mono); font-size: 10px; letter-spacing: .06em; opacity: .45; }
.col.hot { fill: var(--sun); opacity: .9; }
.tag { font-family: var(--font-mono); font-size: 11px; font-weight: 500; }
.t-a { fill: var(--leaf); }
.t-b { fill: var(--coral); }
.t-p { fill: var(--sun); }
.t-teal { fill: var(--teal); }
.mono { fill: currentColor; font-family: var(--font-mono); font-size: 11px; opacity: .8; }
.w { stroke: currentColor; stroke-width: 1.1; opacity: .4; }
.box { stroke-width: 1.2; }
.box.a { fill: rgba(143, 227, 106, .12); stroke: var(--leaf); }
.box.b { fill: rgba(255, 111, 89, .1); stroke: var(--coral); }
.box.p { fill: rgba(255, 194, 75, .12); stroke: var(--sun); }
.cell { stroke-width: 1; }
.c-a { fill: rgba(143, 227, 106, .55); stroke: var(--leaf); }
.c-b { fill: rgba(255, 111, 89, .4); stroke: var(--coral); }
.mcell { fill: none; stroke: currentColor; stroke-width: .8; opacity: .3; }
.mcell.on { fill: var(--teal); stroke: var(--teal); opacity: 1; }
.h { font-family: var(--font-mono); font-size: 10.5px; }
.copy { fill: none; stroke: var(--teal); stroke-width: 1.6; stroke-dasharray: 4 3; }
.f-teal { fill: var(--teal); }
.cp { fill: var(--teal); font-family: var(--font-mono); font-size: 10px; }
.track { stroke: currentColor; stroke-width: 1; opacity: .25; }
.mk { stroke-width: 1.5; }
.m-a { fill: var(--leaf); stroke: var(--leaf); }
.m-b { fill: var(--coral); stroke: var(--coral); }
.m-p { fill: var(--sun); stroke: var(--sun); }
.yl { fill: currentColor; font-family: var(--font-mono); font-size: 10px; opacity: .7; }
.span { stroke: currentColor; stroke-width: 3; opacity: .15; stroke-linecap: round; }
.span.on { stroke: var(--sun); opacity: .9; }
.eq { fill: currentColor; font-family: var(--font-mono); font-size: 10.5px; opacity: .8; }
</style>
