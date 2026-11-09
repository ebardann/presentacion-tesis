<script setup lang="ts">
// Triangle multiplicative update (AF3 pairformer):
//   outgoing: Z_ij ← Σ_k  a(Z_ik) ⊙ b(Z_jk)    (filas i y j)
//   incoming: Z_ij ← Σ_k  a(Z_ki) ⊙ b(Z_kj)    (columnas i y j)
// + triangle attention (starting / ending node): misma geometría, con atención sobre k.
const N = 8, S = 13, C = 11, X0 = 14, Y0 = 30
const I = 1, J = 3, K = 6
const cells = Array.from({ length: N * N }, (_, n) => {
  const r = Math.floor(n / N), c = n % N
  let cls = 'z'
  if (r === I || r === J) cls = 'row'
  if ((r === I || r === J) && c === K) cls = 'src'
  if (r === I && c === J) cls = 'tgt'
  return { r, c, cls }
})
const cx = (c: number) => X0 + c * S + C / 2
const cy = (r: number) => Y0 + r * S + C / 2

// triángulos: nodos i, j abajo, k arriba
function tri(ox: number) {
  return { i: { x: ox, y: 120 }, j: { x: ox + 70, y: 120 }, k: { x: ox + 35, y: 62 } }
}
const tOut = tri(168)
const tIn = tri(282)
// acorta una línea para que la flecha no tape el nodo
function seg(a: { x: number, y: number }, b: { x: number, y: number }, r = 9) {
  const dx = b.x - a.x, dy = b.y - a.y, L = Math.hypot(dx, dy)
  return { x1: a.x + dx / L * r, y1: a.y + dy / L * r, x2: b.x - dx / L * r, y2: b.y - dy / L * r }
}
</script>

<template>
  <svg class="tu" viewBox="0 0 380 178" role="img" aria-label="triangle updates: Z_ij se actualiza combinando las aristas hacia un tercer residuo k">
    <defs>
      <marker id="tu-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
        <path d="M0,0 L10,5 L0,10 z" class="f-teal" />
      </marker>
      <marker id="tu-s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
        <path d="M0,0 L10,5 L0,10 z" class="f-sun" />
      </marker>
    </defs>

    <!-- matriz Z (caso outgoing) -->
    <text :x="X0" y="10" class="col">Z · outgoing</text>
    <rect v-for="c in cells" :key="c.r + '-' + c.c" :x="X0 + c.c * S" :y="Y0 + c.r * S" :width="C" :height="C" rx="1.5" :class="c.cls" />
    <text :x="X0 - 5" :y="cy(I) + 3.5" class="lab t-sun" text-anchor="end">i</text>
    <text :x="X0 - 5" :y="cy(J) + 3.5" class="lab t-teal" text-anchor="end">j</text>
    <text :x="cx(K)" :y="Y0 - 5" class="lab t-teal" text-anchor="middle">k</text>
    <text :x="cx(J)" :y="Y0 - 5" class="lab t-sun" text-anchor="middle">j</text>
    <line v-bind="seg({ x: cx(K), y: cy(I) }, { x: cx(J), y: cy(I) }, 6)" class="arc" marker-end="url(#tu-a)" />
    <line v-bind="seg({ x: cx(K), y: cy(J) }, { x: cx(J), y: cy(I) }, 6)" class="arc" marker-end="url(#tu-a)" />
    <text :x="X0" :y="Y0 + N * S + 16" class="eq">Z_ij ← Σ_k Z_ik ⊙ Z_jk</text>

    <!-- triángulos -->
    <g v-for="(t, n) in [tOut, tIn]" :key="n">
      <text :x="t.k.x" y="40" class="col" text-anchor="middle">{{ n === 0 ? 'outgoing' : 'incoming' }}</text>
      <line v-bind="seg(t.i, t.j)" class="e-tgt" marker-end="url(#tu-s)" />
      <template v-if="n === 0">
        <line v-bind="seg(t.i, t.k)" class="e-src" marker-end="url(#tu-a)" />
        <line v-bind="seg(t.j, t.k)" class="e-src" marker-end="url(#tu-a)" />
      </template>
      <template v-else>
        <line v-bind="seg(t.k, t.i)" class="e-src" marker-end="url(#tu-a)" />
        <line v-bind="seg(t.k, t.j)" class="e-src" marker-end="url(#tu-a)" />
      </template>
      <circle v-for="(p, name) in t" :key="name" :cx="p.x" :cy="p.y" r="7" class="node" :class="name === 'k' ? 'nk' : 'nij'" />
      <text v-for="(p, name) in t" :key="'l' + name" :x="p.x" :y="p.y + 3.5" class="nl" text-anchor="middle">{{ name }}</text>
      <text :x="t.k.x" y="146" class="eq" text-anchor="middle">{{ n === 0 ? 'ik · jk → ij' : 'ki · kj → ij' }}</text>
    </g>

    <text x="168" y="164" class="sub">+ triangle attention (starting / ending node)</text>
    <text x="168" y="176" class="sub">Σ sobre todos los k · ×48 bloques</text>
  </svg>
</template>

<style scoped>
.tu { width: 100%; height: auto; display: block; color: var(--ink); overflow: visible; }
.z { fill: var(--ink); opacity: .1; }
.row { fill: var(--teal); opacity: .16; }
.src { fill: var(--teal); }
.tgt { fill: var(--sun); }
.f-teal { fill: var(--teal); }
.f-sun { fill: var(--sun); }
.arc { fill: none; stroke: var(--teal); stroke-width: 1.1; }
.e-tgt { stroke: var(--sun); stroke-width: 2; }
.e-src { stroke: var(--teal); stroke-width: 1.3; }
.node { stroke-width: 1.3; fill: var(--bg); }
.nij { stroke: var(--sun); }
.nk { stroke: var(--teal); }
.nl { fill: currentColor; font-family: var(--font-mono); font-size: 9.5px; }
.lab { font-family: var(--font-mono); font-size: 10px; font-weight: 500; }
.t-sun { fill: var(--sun); }
.t-teal { fill: var(--teal); }
.col { fill: currentColor; font-family: var(--font-mono); font-size: 10px; letter-spacing: .06em; opacity: .55; }
.eq { fill: currentColor; font-family: var(--font-mono); font-size: 9.5px; opacity: .8; }
.sub { fill: currentColor; font-family: var(--font-mono); font-size: 9px; opacity: .55; }
</style>
