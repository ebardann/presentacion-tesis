<script setup lang="ts">
// Esquema del MSA module de AF3 (4 bloques):
// la representación MSA (N_seq × N × 64) escribe en el pair Z vía outer product mean,
// y lee de Z vía pair-weighted averaging. Z se refina con triangle updates.
// Al salir, la MSA se descarta: sólo Z continúa al pairformer.
const NC = 12          // columnas = residuos (tokens)
const NR = 7           // filas = secuencias del MSA
const I = 3
const J = 9
const MX = 40, MY = 34, CW = 14, CH = 11, SX = 16, SY = 14
const PX = 650, PY = 30, PC = 8, PS = 9

// relleno pseudoaleatorio determinista: conservación variable, algunos gaps
function cell(r: number, c: number) {
  if (r === 0) return { cls: 'q', op: 1 }
  if (c === I || c === J) return { cls: (r % 3 === 1 ? 'cvA' : 'cvB'), op: 1 } // co-varían juntas
  const h = ((r * 73 + c * 151) % 97) / 97
  if (h < 0.12) return { cls: 'gap', op: 1 }
  return { cls: 'aa', op: 0.18 + 0.5 * h }
}
const msa = Array.from({ length: NR }, (_, r) =>
  Array.from({ length: NC }, (_, c) => ({ r, c, ...cell(r, c) }))).flat()
const pair = Array.from({ length: NC * NC }, (_, k) => {
  const i = Math.floor(k / NC), j = k % NC
  const hot = (i === I && j === J) || (i === J && j === I)
  const diag = Math.abs(i - j) <= 1
  return { i, j, hot, op: diag ? 0.45 : 0.08 + 0.12 * (((i * 31 + j * 17) % 11) / 11) }
})
const msaRight = MX + NC * SX
const msaMid = MY + (NR * SY) / 2
</script>

<template>
  <svg class="mm" viewBox="0 0 900 180" role="img" aria-label="msa module: msa y pair representation intercambian información durante 4 bloques">
    <defs>
      <marker id="mm-arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M0,0 L10,5 L0,10 z" fill="currentColor" />
      </marker>
    </defs>

    <!-- MSA -->
    <text :x="MX" y="20" class="col">msa · N_seq × N × 64</text>
    <rect v-for="m in msa" :key="'m' + m.r + '-' + m.c"
      :x="MX + m.c * SX" :y="MY + m.r * SY" :width="CW" :height="CH" rx="1.5"
      :class="m.cls" :style="m.cls === 'aa' ? { opacity: m.op } : undefined" />
    <text :x="MX - 8" :y="MY + 9" class="tag t-sun" text-anchor="end">query</text>
    <text :x="MX + I * SX + CW / 2" :y="MY + NR * SY + 12" class="tag t-teal" text-anchor="middle">i</text>
    <text :x="MX + J * SX + CW / 2" :y="MY + NR * SY + 12" class="tag t-teal" text-anchor="middle">j</text>
    <text :x="MX" y="172" class="sub">i, j co-varían → señal de contacto</text>

    <!-- intercambio msa ⇄ pair -->
    <path :d="`M${msaRight + 14},${msaMid - 22} C 380,34 520,34 ${PX - 14},${PY + 20}`" class="wire w-sun" marker-end="url(#mm-arr)" />
    <text x="445" y="22" class="op t-sun" text-anchor="middle">outer product mean · msa → pair</text>
    <path :d="`M${PX - 14},${PY + 86} C 520,146 380,146 ${msaRight + 14},${msaMid + 22}`" class="wire" marker-end="url(#mm-arr)" />
    <text x="445" y="164" class="op" text-anchor="middle">pair-weighted averaging · pair → msa</text>

    <rect x="370" y="68" width="150" height="46" rx="5" class="blk" />
    <text x="445" y="88" class="txt" text-anchor="middle">msa module</text>
    <text x="445" y="105" class="sub" text-anchor="middle">× 4 bloques</text>

    <!-- pair Z -->
    <text :x="PX" y="20" class="col">pair Z · N × N × 128</text>
    <rect v-for="p in pair" :key="'p' + p.i + '-' + p.j"
      :x="PX + p.j * PS" :y="PY + p.i * PS" :width="PC" :height="PC"
      :class="p.hot ? 'hot' : 'zz'" :style="p.hot ? undefined : { opacity: p.op }" />
    <text :x="PX + J * PS + PC + 6" :y="PY + I * PS + 7" class="tag t-sun">Z_ij</text>
    <text :x="PX" y="172" class="sub">+ triangle updates sobre Z</text>

    <!-- salida -->
    <line :x1="PX + NC * PS + 30" :y1="PY + 54" :x2="PX + NC * PS + 72" :y2="PY + 54" class="wire" marker-end="url(#mm-arr)" />
    <text :x="PX + NC * PS + 80" :y="PY + 50" class="txt sm">pairformer</text>
    <text :x="PX + NC * PS + 80" :y="PY + 66" class="sub">sólo Z sigue</text>
  </svg>
</template>

<style scoped>
.mm { width: 100%; height: auto; max-height: 132px; display: block; color: var(--ink); overflow: visible; }
.aa { fill: var(--ink); }
.gap { fill: none; stroke: var(--ink); stroke-width: .8; opacity: .25; stroke-dasharray: 2 2; }
.q { fill: rgba(255, 194, 75, .55); }
.cvA { fill: var(--teal); }
.cvB { fill: rgba(63, 217, 199, .35); }
.zz { fill: var(--ink); }
.hot { fill: var(--sun); }
.blk { fill: rgba(255, 194, 75, .08); stroke: var(--sun); stroke-width: 1.2; }
.wire { fill: none; stroke: currentColor; stroke-width: 1.2; opacity: .5; }
.w-sun { stroke: var(--sun); opacity: .8; }
.txt { fill: currentColor; font-family: var(--font-body); font-size: 14px; font-weight: 400; }
.txt.sm { font-size: 13px; }
.sub { fill: currentColor; font-family: var(--font-mono); font-size: 10.5px; opacity: .6; }
.col { fill: currentColor; font-family: var(--font-mono); font-size: 11px; letter-spacing: .06em; opacity: .55; }
.op { fill: currentColor; font-family: var(--font-mono); font-size: 11px; opacity: .75; }
.tag { font-family: var(--font-mono); font-size: 10.5px; font-weight: 500; }
.t-sun { fill: var(--sun); opacity: 1; }
.t-teal { fill: var(--teal); }
</style>
