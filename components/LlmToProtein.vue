<script setup lang="ts">
// Transformer (LLM) vs Pairformer (AF3): las mismas piezas con otra forma.
// Izquierda: un stream (vector por token) · self-attention + MLP, × N capas.
// Derecha: dos streams — H (por residuo) y Z (por par) — · atención con pair bias + transition,
// más las operaciones triangulares sobre Z, que no tienen análogo en un LLM. × 48 bloques.
const BH = 30 // alto de bloque
const Y = { out: 76, tri: 218, att: 172, mlp: 126, inp: 262 }

// columnas (centro x · ancho)
const L = { x: 180, w: 150 }
const Hc = { x: 655, w: 140 }
const Zc = { x: 830, w: 140 }

const left = [
  { y: Y.att, t: 'self-attention', k: 'att' },
  { y: Y.mlp, t: 'MLP', k: 'mlp' },
]
const hBlocks = [
  { y: Y.att, t: 'attn + pair bias', k: 'att' },
  { y: Y.mlp, t: 'transition', k: 'mlp' },
]
const zBlocks = [
  { y: Y.tri, t: 'triangle mult. ×2', k: 'tri' },
  { y: Y.att, t: 'triangle attn ×2', k: 'tri' },
  { y: Y.mlp, t: 'transition', k: 'mlp' },
]
const links = [
  { y: Y.att, t: 'mezcla entre posiciones', k: 'att' },
  { y: Y.mlp, t: 'MLP por posición', k: 'mlp' },
  { y: Y.inp, t: 'flujo residual', k: 'res' },
]
const x0 = L.x + L.w / 2, x1 = Hc.x - Hc.w / 2
</script>

<template>
  <div class="l2p">
    <svg viewBox="0 0 960 296" class="fig" role="img" aria-label="comparación entre un bloque transformer de un LLM y un bloque pairformer de AlphaFold 3: atención y MLP equivalentes, más operaciones triangulares sobre el pair">
      <defs>
        <marker id="l2p-a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--ink)" opacity=".55" /></marker>
        <marker id="l2p-z" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--sun)" /></marker>
      </defs>

      <!-- ===== Transformer ===== -->
      <rect x="40" y="6" width="280" height="284" rx="10" class="panel" />
      <text :x="L.x" y="30" class="hd" text-anchor="middle">Transformer · LLM</text>
      <text :x="L.x" y="47" class="sub" text-anchor="middle">× N capas</text>
      <rect :x="L.x - 55" :y="Y.out - 12" width="110" height="24" rx="12" class="chip out" />
      <text :x="L.x" :y="Y.out + 4" class="ct out" text-anchor="middle">→ palabra</text>
      <line :x1="L.x" :y1="Y.inp - 12" :x2="L.x" :y2="Y.out + 14" class="stream" marker-end="url(#l2p-a)" />
      <g v-for="b in left" :key="b.t">
        <rect :x="L.x - L.w / 2" :y="b.y - BH / 2" :width="L.w" :height="BH" rx="5" :class="['blk', b.k]" />
        <text :x="L.x" :y="b.y + 4" class="bt" text-anchor="middle">{{ b.t }}</text>
      </g>
      <rect :x="L.x - 55" :y="Y.inp - 12" width="110" height="24" rx="4" class="chip" />
      <text :x="L.x" :y="Y.inp + 4" class="ct" text-anchor="middle">x · L × d</text>

      <!-- ===== correspondencias ===== -->
      <g v-for="l in links" :key="l.t">
        <line :x1="l.k === 'res' ? L.x + 55 : x0" :y1="l.y" :x2="l.k === 'res' ? Hc.x - 60 : x1" :y2="l.y" :class="['link', l.k]" />
        <rect :x="(x0 + x1) / 2 - 92" :y="l.y - 11" width="184" height="22" rx="11" :class="['tag', l.k]" />
        <text :x="(x0 + x1) / 2" :y="l.y + 4" :class="['tt', l.k]" text-anchor="middle">≈ {{ l.t }}</text>
      </g>

      <!-- ===== Pairformer ===== -->
      <rect x="565" y="6" width="355" height="284" rx="10" class="panel hot" />
      <text x="742" y="30" class="hd hot" text-anchor="middle">Pairformer · AF3</text>
      <text x="742" y="47" class="sub" text-anchor="middle">× 48 bloques</text>
      <rect x="682" :y="Y.out - 12" width="120" height="24" rx="12" class="chip out" />
      <text x="742" :y="Y.out + 4" class="ct out" text-anchor="middle">→ difusión → 3D</text>
      <path :d="`M${Hc.x},${Y.out + 30} L${Hc.x},${Y.out + 22} L${Zc.x},${Y.out + 22} L${Zc.x},${Y.out + 30}`" class="merge" />
      <line x1="742" :y1="Y.out + 22" x2="742" :y2="Y.out + 14" class="merge" marker-end="url(#l2p-a)" />

      <!-- stream H -->
      <line :x1="Hc.x" :y1="Y.inp - 12" :x2="Hc.x" :y2="Y.out + 30" class="stream" />
      <g v-for="b in hBlocks" :key="'h' + b.t">
        <rect :x="Hc.x - Hc.w / 2" :y="b.y - BH / 2" :width="Hc.w" :height="BH" rx="5" :class="['blk', b.k]" />
        <text :x="Hc.x" :y="b.y + 4" class="bt" text-anchor="middle">{{ b.t }}</text>
      </g>
      <rect :x="Hc.x - 58" :y="Y.inp - 12" width="116" height="24" rx="4" class="chip" />
      <text :x="Hc.x" :y="Y.inp + 4" class="ct" text-anchor="middle">H · N × 384</text>

      <!-- stream Z -->
      <line :x1="Zc.x" :y1="Y.inp - 12" :x2="Zc.x" :y2="Y.out + 30" class="stream z" />
      <g v-for="b in zBlocks" :key="'z' + b.t">
        <rect :x="Zc.x - Zc.w / 2" :y="b.y - BH / 2" :width="Zc.w" :height="BH" rx="5" :class="['blk', b.k]" />
        <text :x="Zc.x" :y="b.y + 4" class="bt" text-anchor="middle">{{ b.t }}</text>
      </g>
      <rect :x="Zc.x - 62" :y="Y.inp - 12" width="124" height="24" rx="4" class="chip z" />
      <text :x="Zc.x" :y="Y.inp + 4" class="ct z" text-anchor="middle">Z · N × N × 128</text>

      <!-- pair bias: Z guía la atención de H -->
      <line :x1="Zc.x - Zc.w / 2" :y1="Y.att" :x2="Hc.x + Hc.w / 2 + 2" :y2="Y.att" class="bias" marker-end="url(#l2p-z)" />
      <text :x="(Zc.x - Zc.w / 2 + Hc.x + Hc.w / 2) / 2" :y="Y.att - 7" class="bl" text-anchor="middle">bias</text>
    </svg>

    <div class="caps">
      <div><span>un stream · <b>vector por token</b></span></div>
      <div class="mid"><span>mismas piezas</span></div>
      <div><span>dos streams · <b>H</b> por residuo + <b>Z</b> por par</span></div>
    </div>

    <div class="key">
      <span><i class="k-att" />atención</span>
      <span><i class="k-mlp" />MLP / transition</span>
      <span><i class="k-tri" />triangular · sin análogo en LLMs</span>
    </div>
  </div>
</template>

<style scoped>
.fig { width: 100%; height: auto; display: block; overflow: visible; color: var(--ink); }
.panel { fill: rgba(241, 236, 216, .02); stroke: var(--ink); stroke-opacity: .2; stroke-width: 1; }
.panel.hot { stroke: var(--accent); stroke-opacity: .55; fill: rgba(255, 194, 75, .025); }
.hd { fill: var(--ink); font-family: var(--font-mono); font-size: 14px; letter-spacing: .06em; opacity: .8; }
.hd.hot { fill: var(--accent); opacity: 1; }
.sub { fill: var(--ink); font-family: var(--font-mono); font-size: 10.5px; opacity: .5; }

.chip { fill: rgba(241, 236, 216, .05); stroke: var(--ink); stroke-opacity: .45; stroke-width: 1; }
.chip.z { stroke: var(--sun); stroke-opacity: .8; }
.chip.out { stroke: var(--leaf); stroke-opacity: 1; fill: rgba(143, 227, 106, .08); }
.ct { fill: var(--ink); font-family: var(--font-mono); font-size: 11.5px; }
.ct.z { fill: var(--sun); }
.ct.out { fill: var(--leaf); }

.stream { stroke: var(--ink); stroke-width: 1.4; opacity: .35; }
.stream.z { stroke: var(--sun); opacity: .5; }
.merge { fill: none; stroke: var(--ink); stroke-width: 1.2; opacity: .45; }

.blk { stroke-width: 1.3; }
.blk.att { fill: color-mix(in srgb, var(--teal) 14%, var(--bg)); stroke: var(--teal); }
.blk.mlp { fill: color-mix(in srgb, var(--leaf) 12%, var(--bg)); stroke: var(--leaf); }
.blk.tri { fill: color-mix(in srgb, var(--coral) 14%, var(--bg)); stroke: var(--coral); filter: drop-shadow(0 0 5px rgba(255, 111, 89, .35)); }
.bt { fill: var(--ink); font-family: var(--font-mono); font-size: 11.5px; }

.link { stroke-width: 1.2; stroke-dasharray: 4 4; opacity: .7; animation: flow 1.4s linear infinite; }
.link.att { stroke: var(--teal); }
.link.mlp { stroke: var(--leaf); }
.link.res { stroke: var(--ink); opacity: .35; }
.tag { fill: var(--bg); stroke-width: 1; }
.tag.att { stroke: var(--teal); }
.tag.mlp { stroke: var(--leaf); }
.tag.res { stroke: rgba(241, 236, 216, .35); }
.tt { font-family: var(--font-mono); font-size: 10.5px; }
.tt.att { fill: var(--teal); }
.tt.mlp { fill: var(--leaf); }
.tt.res { fill: var(--ink); opacity: .7; }

.bias { stroke: var(--sun); stroke-width: 1.4; }
.bl { fill: var(--sun); font-family: var(--font-mono); font-size: 10px; }

.caps { display: grid; grid-template-columns: 280fr 245fr 355fr; margin: .7rem 0 0; padding: 0 calc(100% * 40 / 960); font-family: var(--font-mono); font-size: .74rem; text-align: center; }
.caps span { opacity: .7; }
.caps .mid span { opacity: .5; }
.caps b { color: var(--accent); font-weight: 500; }

.key { display: flex; justify-content: center; gap: 1.8rem; margin-top: 1.1rem; font-family: var(--font-mono); font-size: .68rem; opacity: .75; }
.key span { display: flex; align-items: center; gap: .45rem; }
.key i { width: .8rem; height: .8rem; border-radius: 2px; border: 1.3px solid; }
.key i.k-att { border-color: var(--teal); background: color-mix(in srgb, var(--teal) 14%, transparent); }
.key i.k-mlp { border-color: var(--leaf); background: color-mix(in srgb, var(--leaf) 12%, transparent); }
.key i.k-tri { border-color: var(--coral); background: color-mix(in srgb, var(--coral) 14%, transparent); }

@keyframes flow { to { stroke-dashoffset: -16; } }
@media (prefers-reduced-motion: reduce) { .link { animation: none; } }
</style>
