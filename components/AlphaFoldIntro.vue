<script setup lang="ts">
// AlphaFold: secuencia → estructura 3D, y línea de tiempo.
// La secuencia (ilustrativa, no es una proteína real) está anotada con su estructura secundaria;
// los mismos colores se usan en el cartoon 3D: hélice α (teal), hebras β (leaf), loops (tinta).

// ---------- secuencia ----------
const SEG = [
  { seq: 'MSP', ss: 'L' },
  { seq: 'EELAKKALELAKRL', ss: 'H' },
  { seq: 'GNPD', ss: 'L' },
  { seq: 'KVTVYVE', ss: 'E' },
  { seq: 'NGDG', ss: 'L' },
  { seq: 'TYRIEVK', ss: 'E' },
  { seq: 'GSW', ss: 'L' },
]
const res = SEG.flatMap(s => [...s.seq].map(a => ({ a, ss: s.ss })))
const PER = 14, CW = 19, CH = 22, SX = 21.5, X0 = 26, Y0 = 44, SY = 46
const chips = res.map((r, i) => ({ ...r, i, x: X0 + (i % PER) * SX, y: Y0 + Math.floor(i / PER) * SY }))
const rowStarts = [0, 1, 2].map(r => ({ n: r * PER + 1, y: Y0 + r * SY }))
// pista de estructura secundaria sobre cada fila: tramos contiguos del mismo tipo
const track: { ss: string, x1: number, x2: number, y: number, end: boolean }[] = []
chips.forEach((c, i) => {
  const prev = track[track.length - 1]
  const sameRow = i % PER !== 0
  if (prev && prev.ss === c.ss && sameRow) { prev.x2 = c.x + CW; prev.end = res[i + 1]?.ss !== c.ss }
  else track.push({ ss: c.ss, x1: c.x, x2: c.x + CW, y: c.y - 9, end: res[i + 1]?.ss !== c.ss })
})
function wave(x1: number, x2: number, y: number) {
  const n = Math.max(2, Math.round((x2 - x1) / 3))
  return 'M' + Array.from({ length: n + 1 }, (_, k) => `${x1 + (k / n) * (x2 - x1)},${y + Math.sin(k / n * (x2 - x1) / 5.5 * Math.PI) * 3}`).join(' L')
}

// ---------- cartoon 3D ----------
// hélice: eje horizontal, ~3.9 vueltas; segmentos de adelante (claros, anchos) y de atrás (oscuros, finos)
const HX0 = 600, HX1 = 760, HY = 48, R = 19, TURNS = 3.9, NSEG = 180
const hp = (t: number) => {
  const th = 2 * Math.PI * TURNS * t
  return { x: HX0 + 10 + t * (HX1 - HX0 - 20) + 13 * Math.cos(th), y: HY + R * Math.sin(th), z: Math.cos(th) }
}
const hsegs = Array.from({ length: NSEG }, (_, k) => {
  const a = hp(k / NSEG), b = hp((k + 1) / NSEG)
  const z = (a.z + b.z) / 2
  return { x1: a.x, y1: a.y, x2: b.x, y2: b.y, z, w: z < 0 ? 2.6 + 3.4 * Math.abs(z) : 2.4 + 5.4 * Math.abs(z) }
})
const back = hsegs.filter(s => s.z < 0)
const front = hsegs.filter(s => s.z >= 0)
const hs = hp(0), he = hp(1)

// hebras β antiparalelas como flechas planas
function strand(x1: number, x2: number, y: number) {
  const d = Math.sign(x2 - x1), hw = 7, aw = 13, hl = 16
  const xb = x2 - d * hl
  return `M${x1},${y - hw} L${xb},${y - hw} L${xb},${y - aw} L${x2},${y} L${xb},${y + aw} L${xb},${y + hw} L${x1},${y + hw} Z`
}
const S1 = { x1: 770, x2: 616, y: 108 }
const S2 = { x1: 616, x2: 778, y: 146 }
const loops = [
  `M584,96 C 590,84 ${hs.x - 14},${hs.y + 22} ${hs.x},${hs.y}`,                // N-term → hélice
  `M${he.x},${he.y} C ${he.x + 34},${he.y + 4} ${S1.x1 + 26},${S1.y - 18} ${S1.x1},${S1.y}`, // hélice → β1
  `M${S1.x2 + 2},${S1.y} C 588,${S1.y} 584,${S2.y} ${S2.x1},${S2.y}`,             // giro β
  `M${S2.x2 - 2},${S2.y} C 800,${S2.y} 806,${S2.y - 4} 812,${S2.y - 12}`,         // → C-term
]

const events = [
  { y: '2018', t: 'AlphaFold 1', s: '1º en CASP13' },
  { y: '2020', t: 'AlphaFold 2', s: 'CASP14 · precisión ≈ experimental' },
  { y: '2021–22', t: 'AlphaFold DB', s: '> 200 M estructuras' },
  { y: '2024', t: 'AlphaFold 3', s: 'all-atom · difusión' },
  { y: '2024', t: 'Nobel de Química', s: 'Hassabis & Jumper (con Baker)' },
]
</script>

<template>
  <div class="afi">
    <svg viewBox="0 0 900 180" class="s2s" role="img" aria-label="secuencia de aminoácidos anotada y su estructura 3D">
      <defs>
        <marker id="afi-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" class="fa" /></marker>
        <linearGradient id="afi-st" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="#c4f5a8" />
          <stop offset=".45" stop-color="var(--leaf)" />
          <stop offset="1" stop-color="#4f8f37" />
        </linearGradient>
      </defs>

      <!-- ===== secuencia ===== -->
      <text x="0" y="12" class="cap">secuencia (1D) · 42 aminoácidos</text>
      <text v-for="r in rowStarts" :key="r.n" :x="X0 - 6" :y="r.y + 15" class="idx" text-anchor="end">{{ r.n }}</text>
      <g v-for="t in track" :key="t.x1 + '-' + t.y">
        <path v-if="t.ss === 'H'" :d="wave(t.x1 + 1, t.x2 - 1, t.y)" class="tk-h" />
        <path v-else-if="t.ss === 'E'" :d="`M${t.x1 + 1},${t.y} L${t.x2 - (t.end ? 7 : 1)},${t.y}`" class="tk-e" />
        <path v-if="t.ss === 'E' && t.end" :d="`M${t.x2 - 8},${t.y - 4.5} L${t.x2},${t.y} L${t.x2 - 8},${t.y + 4.5} Z`" class="tk-e-head" />
        <line v-if="t.ss === 'L'" :x1="t.x1 + 2" :y1="t.y" :x2="t.x2 - 2" :y2="t.y" class="tk-l" />
      </g>
      <g v-for="c in chips" :key="c.i">
        <rect :x="c.x" :y="c.y" :width="CW" :height="CH" rx="3" :class="'ch ch-' + c.ss" />
        <text :x="c.x + CW / 2" :y="c.y + 15.5" class="aa" text-anchor="middle">{{ c.a }}</text>
      </g>
      <text :x="X0 - 6" :y="Y0 - 8" class="end" text-anchor="end">N</text>
      <text :x="chips[41].x + CW + 5" :y="chips[41].y + 15" class="end">C</text>

      <!-- ===== modelo ===== -->
      <line x1="352" y1="90" x2="392" y2="90" class="ar" marker-end="url(#afi-a)" />
      <rect x="398" y="66" width="122" height="48" rx="5" class="box" />
      <text x="459" y="88" class="bt" text-anchor="middle">AlphaFold</text>
      <text x="459" y="104" class="bs" text-anchor="middle">+ msa · templates</text>
      <line x1="526" y1="90" x2="556" y2="90" class="ar" marker-end="url(#afi-a)" />

      <!-- ===== estructura 3D ===== -->
      <text x="580" y="12" class="cap">estructura (3D)</text>
      <path v-for="(d, i) in loops" :key="'l' + i" :d="d" class="loop" />
      <line v-for="(s, i) in back" :key="'b' + i" v-bind="s" :stroke-width="s.w" class="hx-back" />
      <path :d="strand(S1.x1, S1.x2, S1.y)" class="st" />
      <path :d="strand(S2.x1, S2.x2, S2.y)" class="st" />
      <line v-for="(s, i) in front" :key="'f' + i" v-bind="s" :stroke-width="s.w" class="hx-front" />
      <text x="574" y="108" class="end">N</text>
      <text x="817" y="130" class="end">C</text>
      <text x="800" y="44" class="lab t-h">hélice α</text>
      <text x="800" y="60" class="lab dim">res 4–17</text>
      <text x="818" y="104" class="lab t-e">hoja β</text>
      <text x="818" y="120" class="lab dim">22–28 · 33–39</text>
      <text x="580" y="176" class="lab dim">una coordenada por átomo · aquí sólo el backbone</text>
    </svg>

    <div class="tl">
      <div v-for="(e, i) in events" :key="i" class="ev" :class="{ hot: e.t === 'AlphaFold 3' }">
        <span class="y">{{ e.y }}</span>
        <span class="dot" />
        <span class="t">{{ e.t }}</span>
        <span class="s">{{ e.s }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.s2s { width: 100%; height: auto; display: block; overflow: visible; color: var(--ink); }
.cap { fill: currentColor; font-family: var(--font-mono); font-size: 11px; letter-spacing: .06em; opacity: .5; }
.idx { fill: currentColor; font-family: var(--font-mono); font-size: 9px; opacity: .45; }
.end { fill: var(--sun); font-family: var(--font-mono); font-size: 11px; font-weight: 600; }

.ch { stroke-width: 1; }
.ch-H { fill: rgba(63, 217, 199, .16); stroke: rgba(63, 217, 199, .7); }
.ch-E { fill: rgba(143, 227, 106, .16); stroke: rgba(143, 227, 106, .7); }
.ch-L { fill: rgba(241, 236, 216, .05); stroke: rgba(241, 236, 216, .25); }
.aa { fill: currentColor; font-family: var(--font-mono); font-size: 12.5px; font-weight: 500; }
.tk-h { fill: none; stroke: var(--teal); stroke-width: 1.6; }
.tk-e { stroke: var(--leaf); stroke-width: 4; }
.tk-e-head { fill: var(--leaf); }
.tk-l { stroke: currentColor; stroke-width: 1; opacity: .3; }

.ar { stroke: currentColor; stroke-width: 1.2; opacity: .5; }
.fa { fill: currentColor; }
.box { fill: rgba(255, 194, 75, .1); stroke: var(--sun); stroke-width: 1.3; }
.bt { fill: var(--sun); font-family: var(--font-mono); font-size: 14px; }
.bs { fill: currentColor; font-family: var(--font-mono); font-size: 10px; opacity: .6; }

.loop { fill: none; stroke: #cfc9b4; stroke-width: 2.6; stroke-linecap: round; opacity: .75; }
.hx-back { stroke: #237a71; stroke-linecap: round; }
.hx-front { stroke: var(--teal); stroke-linecap: round; filter: drop-shadow(0 0 2px rgba(63, 217, 199, .35)); }
.st { fill: url(#afi-st); stroke: #2f5a22; stroke-width: 1; stroke-linejoin: round; }

.lab { fill: currentColor; font-family: var(--font-mono); font-size: 11px; opacity: .8; }
.lab.dim { opacity: .45; font-size: 9.5px; }
.t-h { fill: var(--teal); opacity: 1; }
.t-e { fill: var(--leaf); opacity: 1; }

.tl { display: grid; grid-template-columns: repeat(5, 1fr); margin-top: 1.1rem; position: relative; }
.tl::before { content: ""; position: absolute; left: 0; right: 0; top: 1.62rem; border-top: 1px dashed var(--accent-soft); }
.ev { display: flex; flex-direction: column; gap: .2rem; font-family: var(--font-mono); padding-right: .8rem; }
.y { font-size: .75rem; color: var(--accent); }
.dot { width: .55rem; height: .55rem; border-radius: 999px; background: var(--bg); border: 1.5px solid var(--accent); margin: .15rem 0 .25rem; position: relative; z-index: 1; }
.t { font-size: .85rem; }
.s { font-size: .68rem; opacity: .6; line-height: 1.35; font-family: var(--font-body); }
.ev.hot .dot { background: var(--sun); border-color: var(--sun); box-shadow: 0 0 10px var(--sun); }
.ev.hot .t { color: var(--sun); }
</style>
