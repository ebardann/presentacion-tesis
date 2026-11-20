<script setup lang="ts">
// Un bloque del Pairformer, visual: Z (pair) se refina a sí mismo con triangle updates
// y sesga la atención entre tokens de H (single). Se repite ×48.
const N = 8, S = 17, C = 14
const ZX = 24, ZY = 52
const I = 2, J = 5
const zc = Array.from({ length: N * N }, (_, n) => {
  const r = Math.floor(n / N), c = n % N
  const d = Math.abs(r - c)
  return { x: ZX + c * S, y: ZY + r * S, o: d === 0 ? 0.5 : d === 1 ? 0.3 : 0.08 + ((r * 7 + c * 3) % 5) * 0.03, hot: r === I && c === J }
})
const HX = 300, HW = 74
const hrows = Array.from({ length: N }, (_, r) => ({ y: ZY + r * S, w: HW * (0.45 + ((r * 5) % 7) / 12) }))
const Q = 2 // token que atiende
const att = [
  { r: 0, w: 0.35 }, { r: 4, w: 0.7 }, { r: 5, w: 1 }, { r: 7, w: 0.25 },
].map(a => {
  const y1 = ZY + Q * S + C / 2, y2 = ZY + a.r * S + C / 2, x = HX + HW + 6
  const bulge = 18 + Math.abs(a.r - Q) * 7
  return { ...a, d: `M${x},${y1} C${x + bulge},${y1} ${x + bulge},${y2} ${x},${y2}` }
})
const gx = ZX + N * S
</script>

<template>
  <svg viewBox="0 0 420 250" class="pfb" role="img" aria-label="bloque del pairformer: Z se actualiza con triangle updates y sesga la atención sobre H">
    <defs>
      <marker id="pfb-a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--teal)" /></marker>
      <marker id="pfb-b" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--accent)" /></marker>
    </defs>

    <!-- Z -->
    <text :x="ZX" y="26" class="nm">Z</text>
    <text :x="ZX + 18" y="26" class="dm">N × N × 128</text>
    <rect v-for="(c, i) in zc" :key="i" :x="c.x" :y="c.y" :width="C" :height="C" rx="2" :class="c.hot ? 'zh' : 'zc'" :style="c.hot ? {} : { opacity: c.o }" />
    <text :x="ZX - 6" :y="ZY + I * S + 11" class="ix" text-anchor="end">i</text>
    <text :x="ZX + J * S + C / 2" :y="ZY - 6" class="ix" text-anchor="middle">j</text>

    <!-- triangle update: bucle sobre Z -->
    <path :d="`M${ZX + 30},${ZY + N * S + 6} C${ZX + 30},${ZY + N * S + 44} ${ZX + 106},${ZY + N * S + 44} ${ZX + 106},${ZY + N * S + 10}`" class="loop" marker-end="url(#pfb-a)" />
    <g :transform="`translate(${ZX + 68},${ZY + N * S + 36})`">
      <path d="M-9,6 L9,6 L0,-9 Z" class="tri" />
    </g>
    <text :x="ZX + 68" :y="ZY + N * S + 62" class="lb t" text-anchor="middle">triangle</text>

    <!-- pair bias: Z → atención de H -->
    <path :d="`M${gx + 6},${ZY + I * S + C / 2} C${gx + 50},${ZY + I * S + C / 2} ${HX - 50},${ZY + Q * S + C / 2} ${HX - 8},${ZY + Q * S + C / 2}`" class="bias" marker-end="url(#pfb-b)" />
    <text :x="(gx + HX) / 2" :y="ZY + Q * S - 8" class="lb b" text-anchor="middle">pair bias</text>

    <!-- H -->
    <text :x="HX" y="26" class="nm">H</text>
    <text :x="HX + 18" y="26" class="dm">N × 384</text>
    <rect v-for="(h, r) in hrows" :key="r" :x="HX" :y="h.y" :width="h.w" :height="C" rx="2" :class="r === Q ? 'hq' : 'hc'" />
    <path v-for="a in att" :key="a.r" :d="a.d" class="att" :style="{ strokeOpacity: a.w, strokeWidth: 0.8 + a.w * 2 }" />
    <text :x="HX + HW + 24" :y="ZY + N * S + 18" class="lb b" text-anchor="middle">attn</text>
  </svg>
</template>

<style scoped>
.pfb { width: 100%; height: auto; display: block; overflow: visible; color: var(--ink); }
.nm { fill: var(--accent); font-family: var(--font-mono); font-size: 18px; font-weight: 500; }
.dm { fill: var(--ink); font-family: var(--font-mono); font-size: 11px; opacity: .5; }
.ix { fill: var(--sun); font-family: var(--font-mono); font-size: 11px; font-weight: 500; }
.zc { fill: var(--teal); }
.zh { fill: var(--sun); filter: drop-shadow(0 0 5px var(--sun)); }
.hc { fill: var(--accent); opacity: .35; }
.hq { fill: var(--accent); filter: drop-shadow(0 0 5px var(--accent)); }
.loop { fill: none; stroke: var(--teal); stroke-width: 1.6; stroke-dasharray: 4 4; animation: flow 1.2s linear infinite; }
.tri { fill: none; stroke: var(--teal); stroke-width: 1.6; stroke-linejoin: round; }
.bias { fill: none; stroke: var(--accent); stroke-width: 1.8; stroke-dasharray: 5 4; animation: flow 1.2s linear infinite; }
.att { fill: none; stroke: var(--accent); }
.lb { font-family: var(--font-mono); font-size: 12px; }
.lb.t { fill: var(--teal); }
.lb.b { fill: var(--accent); }
@keyframes flow { to { stroke-dashoffset: -8; } }
</style>
