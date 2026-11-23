<script setup lang="ts">
// Flujo residual: Transformer (LLM) vs Pairformer (AF3).
// Cada bloque LEE del flujo y SUMA (⊕) su salida de vuelta; el flujo atraviesa toda la red.
// LLM: un flujo x (L×d). AF3: dos flujos, H (N×384, por residuo) y Z (N×N×128, por par);
// Z además sesga la atención sobre H (pair bias). El patch de la tesis se aplica sobre Z.
const BW = 104, BH = 28
const X0 = 150, X1 = 805

// ----- Transformer -----
const T = { lane: 82, top: 30 }
const tBlocks = [
  { x: 240, t: 'attention', k: 'att' },
  { x: 380, t: 'MLP', k: 'mlp' },
  { x: 520, t: 'attention', k: 'att' },
  { x: 660, t: 'MLP', k: 'mlp' },
]

// ----- Pairformer -----
const H = { lane: 214, top: 162 }
const Z = { lane: 288, bot: 312 }
const zBlocks = [
  { x: 240, t: 'tri. mult ×2', k: 'tri' },
  { x: 380, t: 'tri. attn ×2', k: 'tri' },
  { x: 520, t: 'transition', k: 'mlp' },
]
const hBlocks = [
  { x: 640, t: 'attn + bias', k: 'att' },
  { x: 760, t: 'transition', k: 'mlp' },
]
const PATCH = 585 // punto sobre Z donde se aplica h'
</script>

<template>
  <svg viewBox="-14 -10 928 372" class="rc" role="img" aria-label="flujo residual: en un LLM cada bloque lee y suma a un solo flujo; en el Pairformer de AF3 hay dos flujos, H y Z, y Z sesga la atención sobre H">
    <defs>
      <marker id="rc-a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--ink)" opacity=".7" /></marker>
      <marker id="rc-l" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--ink)" /></marker>
      <marker id="rc-z" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--sun)" /></marker>
    </defs>

    <!-- paneles: uno por arquitectura -->
    <rect x="-12" y="-8" width="924" height="118" rx="10" class="panel llm" />
    <rect x="-12" y="128" width="924" height="232" rx="10" class="panel af3" />

    <!-- ================= Transformer ================= -->
    <text x="0" y="16" class="hd">Transformer · LLM</text>
    <text x="0" y="32" class="sub">× N capas</text>
    <g transform="translate(796,0)">
      <rect x="0" y="2" width="104" height="20" rx="10" class="pill llm" />
      <text x="52" y="16" class="pill-t" text-anchor="middle">1 flujo</text>
    </g>
    <text x="0" :y="T.lane + 4" class="ln">x</text>
    <text x="14" :y="T.lane + 4" class="dim">L × d</text>
    <line :x1="X0 - 40" :y1="T.lane" :x2="X1 + 10" :y2="T.lane" class="lane" marker-end="url(#rc-l)" />
    <line :x1="X0 - 40" :y1="T.lane" :x2="X1 + 10" :y2="T.lane" class="flow" />
    <g v-for="b in tBlocks" :key="'t' + b.x">
      <line :x1="b.x - 30" :y1="T.lane" :x2="b.x - 30" :y2="T.top + BH + 2" class="rw" marker-end="url(#rc-a)" />
      <line :x1="b.x + 30" :y1="T.top + BH" :x2="b.x + 30" :y2="T.lane - 8" class="rw" marker-end="url(#rc-a)" />
      <rect :x="b.x - BW / 2" :y="T.top" :width="BW" :height="BH" rx="5" :class="['blk', b.k]" />
      <text :x="b.x" :y="T.top + 18" class="bt" text-anchor="middle">{{ b.t }}</text>
      <circle :cx="b.x + 30" :cy="T.lane" r="7" class="plus" /><text :x="b.x + 30" :y="T.lane + 4" class="pt" text-anchor="middle">+</text>
    </g>
    <text :x="X1 + 22" :y="T.lane + 4" class="out">→ palabra</text>

    <!-- ================= Pairformer ================= -->
    <text x="0" y="152" class="hd hot">Pairformer · AF3</text>
    <text x="0" y="168" class="sub">× 48 bloques</text>
    <g transform="translate(796,138)">
      <rect x="0" y="2" width="104" height="20" rx="10" class="pill af3" />
      <text x="52" y="16" class="pill-t hot" text-anchor="middle">2 flujos</text>
    </g>

    <!-- flujo H -->
    <text x="0" :y="H.lane + 4" class="ln">H</text>
    <text x="16" :y="H.lane + 4" class="dim">N × 384</text>
    <line :x1="X0 - 40" :y1="H.lane" :x2="X1 + 10" :y2="H.lane" class="lane" marker-end="url(#rc-l)" />
    <line :x1="X0 - 40" :y1="H.lane" :x2="X1 + 10" :y2="H.lane" class="flow" />
    <g v-for="b in hBlocks" :key="'h' + b.x">
      <line :x1="b.x - 30" :y1="H.lane" :x2="b.x - 30" :y2="H.top + BH + 2" class="rw" marker-end="url(#rc-a)" />
      <line :x1="b.x + 30" :y1="H.top + BH" :x2="b.x + 30" :y2="H.lane - 8" class="rw" marker-end="url(#rc-a)" />
      <rect :x="b.x - BW / 2" :y="H.top" :width="BW" :height="BH" rx="5" :class="['blk', b.k]" />
      <text :x="b.x" :y="H.top + 18" class="bt" text-anchor="middle">{{ b.t }}</text>
      <circle :cx="b.x + 30" :cy="H.lane" r="7" class="plus" /><text :x="b.x + 30" :y="H.lane + 4" class="pt" text-anchor="middle">+</text>
    </g>

    <!-- flujo Z -->
    <text x="0" :y="Z.lane + 4" class="ln z">Z</text>
    <text x="16" :y="Z.lane + 4" class="dim">N × N × 128</text>
    <line :x1="X0 - 40" :y1="Z.lane" :x2="X1 + 10" :y2="Z.lane" class="lane z" marker-end="url(#rc-z)" />
    <line :x1="X0 - 40" :y1="Z.lane" :x2="X1 + 10" :y2="Z.lane" class="flow z" />
    <g v-for="b in zBlocks" :key="'z' + b.x">
      <line :x1="b.x - 30" :y1="Z.lane" :x2="b.x - 30" :y2="Z.bot - 2" class="rw" marker-end="url(#rc-a)" />
      <line :x1="b.x + 30" :y1="Z.bot" :x2="b.x + 30" :y2="Z.lane + 8" class="rw" marker-end="url(#rc-a)" />
      <rect :x="b.x - BW / 2" :y="Z.bot" :width="BW" :height="BH" rx="5" :class="['blk', b.k]" />
      <text :x="b.x" :y="Z.bot + 18" class="bt" text-anchor="middle">{{ b.t }}</text>
      <circle :cx="b.x + 30" :cy="Z.lane" r="7" class="plus z" /><text :x="b.x + 30" :y="Z.lane + 4" class="pt" text-anchor="middle">+</text>
    </g>

    <!-- pair bias: Z → atención de H -->
    <path :d="`M${hBlocks[0].x},${Z.lane - 8} L${hBlocks[0].x},${H.top + BH + 2}`" class="bias" marker-end="url(#rc-z)" />
    <text :x="hBlocks[0].x + 7" :y="(Z.lane + H.lane) / 2 + 4" class="bl">bias</text>

    <!-- punto de intervención -->
    <g class="patch">
      <circle :cx="PATCH" :cy="Z.lane" r="10" class="ring" />
      <circle :cx="PATCH" :cy="Z.lane" r="4.5" class="dot" />
      <text :x="PATCH - 4" :y="Z.lane - 17" class="pl" text-anchor="middle">patch h&#39;</text>
    </g>

    <text :x="X1 + 22" :y="(H.lane + Z.lane) / 2 + 4" class="out">→ difusión</text>
    <text :x="X1 + 22" :y="(H.lane + Z.lane) / 2 + 20" class="out">→ coords 3D</text>
  </svg>
</template>

<style scoped>
.rc { width: 100%; height: auto; display: block; overflow: visible; color: var(--ink); }
.hd { fill: var(--ink); font-family: var(--font-mono); font-size: 15px; letter-spacing: .05em; opacity: .85; }
.hd.hot { fill: var(--sun); opacity: 1; }
.sub { fill: var(--ink); font-family: var(--font-mono); font-size: 10px; opacity: .5; }
.ln { fill: var(--ink); font-family: var(--font-mono); font-size: 15px; font-weight: 600; }
.ln.z { fill: var(--sun); }
.dim { fill: var(--ink); font-family: var(--font-mono); font-size: 9.5px; opacity: .5; }
.panel { stroke-width: 1.2; }
.panel.llm { fill: rgba(241, 236, 216, .025); stroke: rgba(241, 236, 216, .22); }
.panel.af3 { fill: rgba(255, 194, 75, .045); stroke: rgba(255, 194, 75, .55); filter: drop-shadow(0 0 14px rgba(255, 194, 75, .12)); }
.pill { stroke-width: 1; }
.pill.llm { fill: rgba(241, 236, 216, .06); stroke: rgba(241, 236, 216, .45); }
.pill.af3 { fill: rgba(255, 194, 75, .14); stroke: var(--sun); }
.pill-t { fill: var(--ink); font-family: var(--font-mono); font-size: 11px; letter-spacing: .04em; }
.pill-t.hot { fill: var(--sun); }

.lane { stroke: var(--ink); stroke-width: 3; opacity: .45; }
.lane.z { stroke: var(--sun); opacity: .7; }
.flow { stroke: var(--ink); stroke-width: 3; stroke-dasharray: 2 18; stroke-linecap: round; opacity: .9; animation: flow 1.6s linear infinite; }
.flow.z { stroke: #fff3c4; }
.rw { stroke: var(--ink); stroke-width: 1.1; opacity: .5; }
.plus { fill: var(--bg); stroke: var(--ink); stroke-width: 1.3; }
.plus.z { stroke: var(--sun); }
.pt { fill: var(--ink); font-family: var(--font-mono); font-size: 12px; font-weight: 600; }

.blk { stroke-width: 1.3; }
.blk.att { fill: color-mix(in srgb, var(--teal) 14%, var(--bg)); stroke: var(--teal); }
.blk.mlp { fill: color-mix(in srgb, var(--leaf) 12%, var(--bg)); stroke: var(--leaf); }
.blk.tri { fill: color-mix(in srgb, var(--coral) 14%, var(--bg)); stroke: var(--coral); }
.bt { fill: var(--ink); font-family: var(--font-mono); font-size: 11.5px; }

.bias { fill: none; stroke: var(--sun); stroke-width: 1.4; stroke-dasharray: 4 3; }
.bl { fill: var(--sun); font-family: var(--font-mono); font-size: 10px; }

.patch .ring { fill: none; stroke: var(--sun); stroke-width: 1.5; animation: ping 1.8s ease-out infinite; transform-box: fill-box; transform-origin: center; }
.patch .dot { fill: var(--sun); filter: drop-shadow(0 0 6px var(--sun)); }
.pl { fill: var(--sun); font-family: var(--font-mono); font-size: 10.5px; }

.out { fill: var(--leaf); font-family: var(--font-mono); font-size: 11.5px; }

@keyframes flow { to { stroke-dashoffset: -20; } }
@keyframes ping { 0% { transform: scale(.7); opacity: 1; } 100% { transform: scale(1.8); opacity: 0; } }
@media (prefers-reduced-motion: reduce) { .flow, .patch .ring { animation: none; } }
</style>
