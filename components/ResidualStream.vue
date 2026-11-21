<script setup lang="ts">
// Residual stream: cada bloque lee del stream y le suma (⊕) su salida.
// Izquierda: un token de un LLM (attn trae info de otro token, MLP transforma en el lugar).
// Derecha: Pairformer de AF3, con dos streams (H single, Z pair).
// El punto dorado marca dónde se captura → modifica → reanuda (activation patching).
// prop `only`: 'llm' | 'af3' muestra sólo una mitad (con el texto al costado).
const props = defineProps<{ only?: 'llm' | 'af3' }>()
const vb = props.only === 'llm' ? '20 0 400 300' : props.only === 'af3' ? '490 0 460 300' : '0 0 960 300'

// lectura (stream → bloque) y escritura (bloque → ⊕ en el stream)
function rw(sx: number, bx: number, y: number) {
  const side = Math.sign(bx - sx), mid = (sx + bx) / 2
  return {
    read: `M${sx + side * 3},${y + 24} C${mid},${y + 24} ${mid},${y + 8} ${bx},${y + 8}`,
    write: `M${bx},${y - 8} C${mid},${y - 8} ${mid},${y - 24} ${sx + side * 10},${y - 24}`,
    plus: { x: sx, y: y - 24 },
  }
}

// ---------- LLM ----------
const SL = 150, NB = 372
const llm = [
  { y: 208, t: 'attn', ...rw(SL, 212, 208) },
  { y: 112, t: 'MLP', ...rw(SL, 212, 112) },
]

// ---------- AF3 ----------
const SH = 580, SZ = 800
const af = [
  { y: 208, t: 'triangle', box: { x: 836, w: 92 }, s: SZ, ...rw(SZ, 836, 208) },
  { y: 112, t: 'attn + pair bias', box: { x: 618, w: 132 }, s: SH, ...rw(SH, 618, 112) },
]
const grid = Array.from({ length: 16 }, (_, k) => ({ x: SZ - 14 + (k % 4) * 7, y: 262 + Math.floor(k / 4) * 7, o: k % 5 === 0 ? 0.9 : 0.25 }))
</script>

<template>
  <div class="rs" :class="only ? `solo ${only}` : ''">
    <svg :viewBox="vb" class="fig" role="img" aria-label="residual stream: cada bloque lee y suma al stream; en AF3 los streams son H y Z; el patch reemplaza el stream en un punto">
      <defs>
        <marker id="rs-a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--ink)" opacity=".55" /></marker>
        <marker id="rs-b" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--accent)" /></marker>
        <marker id="rs-s" viewBox="0 0 10 10" refX="5" refY="5" markerUnits="userSpaceOnUse" markerWidth="16" markerHeight="16" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--accent)" /></marker>
      </defs>

      <!-- ===== LLM ===== -->
      <g v-if="only !== 'af3'">
      <text x="40" y="12" class="hd">LLM - un token</text>
      <!-- stream vecino (otro token) -->
      <line :x1="NB" y1="282" :x2="NB" y2="62" class="stream dim" />
      <text :x="NB" y="296" class="sl dim" text-anchor="middle">otro token</text>
      <!-- stream principal -->
      <line :x1="SL" y1="282" :x2="SL" y2="66" class="stream" marker-end="url(#rs-s)" />
      <circle r="4" class="pulse"><animateMotion dur="3s" repeatCount="indefinite" :path="`M${SL},282 L${SL},70`" /></circle>
      <text :x="SL" y="296" class="sl" text-anchor="middle">embedding</text>
      <text :x="SL" y="48" class="sl" text-anchor="middle">siguiente palabra</text>
      <g v-for="b in llm" :key="b.t">
        <rect x="212" :y="b.y - 17" width="96" height="34" rx="5" class="blk" />
        <text x="260" :y="b.y + 5" class="bt" text-anchor="middle">{{ b.t }}</text>
        <path :d="b.read" class="rd" marker-end="url(#rs-a)" />
        <path :d="b.write" class="wr" marker-end="url(#rs-b)" />
        <circle :cx="b.plus.x" :cy="b.plus.y" r="9" class="plus" />
        <text :x="b.plus.x" :y="b.plus.y + 4.5" class="pt" text-anchor="middle">+</text>
      </g>
      <!-- attn mueve info entre tokens -->
      <line :x1="NB - 3" y1="208" x2="312" y2="208" class="mv" marker-end="url(#rs-a)" />

      <!-- patch -->
      <g class="patch">
        <circle :cx="SL" cy="160" r="8" />
        <text :x="SL - 16" y="164" text-anchor="end">patch</text>
      </g>

      </g>

      <!-- divisor -->
      <line v-if="!only" x1="470" y1="20" x2="470" y2="290" class="div" />

      <!-- ===== AF3 ===== -->
      <g v-if="only !== 'llm'">
      <text x="510" y="12" class="hd hot">AF3 · Pairformer</text>
      <rect :x="SH - 30" y="28" :width="SZ - SH + 60" height="24" rx="12" class="diff" />
      <text :x="(SH + SZ) / 2" y="44" class="dt" text-anchor="middle">→ difusión → coordenadas 3D</text>
      <line :x1="SH" y1="270" :x2="SH" y2="62" class="stream" marker-end="url(#rs-s)" />
      <line :x1="SZ" y1="254" :x2="SZ" y2="62" class="stream wide" marker-end="url(#rs-s)" />
      <circle r="4" class="pulse"><animateMotion dur="3s" repeatCount="indefinite" :path="`M${SH},270 L${SH},64`" /></circle>
      <circle r="5" class="pulse"><animateMotion dur="3s" begin="1.5s" repeatCount="indefinite" :path="`M${SZ},254 L${SZ},64`" /></circle>
      <text :x="SH" y="286" class="sl" text-anchor="middle">H · single</text>
      <rect v-for="(g, i) in grid" :key="i" :x="g.x" :y="g.y" width="6" height="6" class="gc" :style="{ opacity: g.o }" />
      <text :x="SZ + 22" y="280" class="sl">Z · pair</text>
      <g v-for="b in af" :key="b.t">
        <rect :x="b.box.x" :y="b.y - 17" :width="b.box.w" height="34" rx="5" class="blk" />
        <text :x="b.box.x + b.box.w / 2" :y="b.y + 5" class="bt" text-anchor="middle">{{ b.t }}</text>
        <path :d="b.read" class="rd" marker-end="url(#rs-a)" />
        <path :d="b.write" class="wr" marker-end="url(#rs-b)" />
        <circle :cx="b.plus.x" :cy="b.plus.y" r="9" class="plus" />
        <text :x="b.plus.x" :y="b.plus.y + 4.5" class="pt" text-anchor="middle">+</text>
      </g>
      <!-- pair bias: Z sesga la atención sobre H -->
      <line :x1="SZ - 4" y1="112" x2="754" y2="112" class="mv" marker-end="url(#rs-a)" />
      <text x="932" y="78" class="rep" text-anchor="end">× 48 bloques</text>

      <!-- patch -->
      <g class="patch">
        <circle :cx="SZ" cy="160" r="8" />
        <text :x="SZ - 16" y="164" text-anchor="end">patch</text>
      </g>
      </g>
    </svg>

    <div v-if="!only" class="caps">
      <div><span>Cada bloque <b>lee</b> el stream y le <b>suma</b> su salida</span></div>
      <div><span><b>H</b> y <b>Z</b> son el stream de AF3 · Z sesga la atención sobre H</span></div>
    </div>
    <p v-if="!only" class="key">patch = reemplazar el stream en un punto y dejar que el resto de la red siga</p>

    <div v-if="only === 'llm'" class="side">
      <p>Cada bloque <b>lee</b> el stream y le <b>suma</b> su salida.</p>
      <p>attn trae información de <b>otros tokens</b>.</p>
      <p>MLP transforma en el lugar.</p>
      <p class="key">patch = reemplazar el stream en un punto y dejar que el resto de la red siga</p>
    </div>
    <div v-if="only === 'af3'" class="side">
      <p><b>H</b> y <b>Z</b> son el residual stream de AF3</p>
      <p>triangle escribe en Z · Z sesga la atención sobre H · ×48</p>
      <p class="key">patch en Z, bloque ℓ → el resto del Pairformer y la difusión corren igual</p>
    </div>
  </div>
</template>

<style scoped>
.fig { width: 100%; height: auto; display: block; overflow: visible; color: var(--ink); }
.hd { fill: var(--ink); font-family: var(--font-mono); font-size: 13px; letter-spacing: .08em; opacity: .7; }
.hd.hot { fill: var(--accent); opacity: 1; }

.stream { stroke: var(--accent); stroke-width: 5; stroke-linecap: round; opacity: .75; }
.stream.wide { stroke-width: 9; opacity: .55; }
.stream.dim { stroke: var(--ink); stroke-width: 4; opacity: .18; }
.sl { fill: var(--ink); font-family: var(--font-mono); font-size: 11px; opacity: .55; }
.sl.dim { opacity: .35; }
.pulse { fill: var(--ink); filter: drop-shadow(0 0 5px var(--accent)); }

.blk { fill: var(--bg); stroke: var(--ink); stroke-opacity: .5; stroke-width: 1.2; }
.bt { fill: var(--ink); font-family: var(--font-mono); font-size: 12.5px; }
.rd { fill: none; stroke: var(--ink); stroke-width: 1.2; opacity: .45; }
.wr { fill: none; stroke: var(--accent); stroke-width: 1.6; }
.plus { fill: var(--bg); stroke: var(--accent); stroke-width: 1.6; }
.pt { fill: var(--accent); font-family: var(--font-mono); font-size: 14px; font-weight: 600; }
.mv { stroke: var(--ink); stroke-width: 1.2; stroke-dasharray: 4 4; opacity: .5; animation: flow 1s linear infinite; }

.diff { fill: rgba(63, 217, 199, .06); stroke: var(--accent); stroke-opacity: .5; stroke-width: 1; }
.dt { fill: var(--accent); font-family: var(--font-mono); font-size: 11.5px; }
.gc { fill: var(--accent); }
.rep { fill: var(--ink); font-family: var(--font-mono); font-size: 12px; opacity: .5; }

.patch circle { fill: var(--sun); filter: drop-shadow(0 0 7px var(--sun)); animation: beat 1.8s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }
.patch text { fill: var(--sun); font-family: var(--font-mono); font-size: 12px; font-weight: 500; }
.div { stroke: var(--accent-soft); stroke-width: 1; stroke-dasharray: 2 5; }

.caps { display: grid; grid-template-columns: 1fr 1fr; gap: 2.5rem; margin-top: .9rem; font-family: var(--font-mono); font-size: .74rem; text-align: center; }
.caps span { opacity: .7; }
.caps b { color: var(--accent); font-weight: 500; }
.key { text-align: center; font-family: var(--font-mono); font-size: .9rem !important; color: var(--sun); margin: 1rem 0 0; }

/* una sola mitad: figura a la izquierda, texto a la derecha */
.rs.solo { display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; align-items: center; }
.rs.solo .fig { max-height: 340px; }
.side { display: flex; flex-direction: column; gap: 1.1rem; font-family: var(--font-mono); }
.side p { margin: 0; font-size: .9rem !important; line-height: 1.5; opacity: .8; }
.side b { color: var(--accent); font-weight: 500; }
.side .key { text-align: left; opacity: 1; margin-top: .6rem; font-size: 1rem !important; }

@keyframes flow { to { stroke-dashoffset: -8; } }
@keyframes beat { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.3); } }
</style>
