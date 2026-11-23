<script setup lang="ts">
import { ref, computed, onBeforeUnmount } from 'vue'
import { onSlideEnter } from '@slidev/client'
// Secuencia → estructura como un solo listón.
// La cadena empieza recta a la izquierda (cada aminoácido con su letra) y, mientras se desplaza a la
// derecha, se pliega: primero la hélice α, después la horquilla β. Todo es una curva 3D proyectada:
// los tramos de atrás se dibujan primero y más oscuros, así el listón se ve con profundidad.
// La secuencia y la geometría son ilustrativas (no es una proteína real).
// Se reproduce al entrar a la slide y al hacer clic sobre la figura.

type V = [number, number, number]

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
const N = res.length // 42

// ---------- geometría (Å, centrada en el origen) ----------
// recta: un aminoácido cada ~1.4 Å de pantalla (sólo para que quepan las letras)
const straight: V[] = res.map((_, i) => [(i - (N - 1) / 2) * 1.4, 0, 0])
// plegada: N-loop · hélice α (3–16) · loop · hebra β1 (21–27, hacia −x) · giro · hebra β2 (32–38, hacia +x) · C-loop
const folded: V[] = res.map((_, i) => {
  if (i <= 2) return ([[-15, 2, 1], [-14, 4, 1.5], [-12.2, 5.4, 1]] as V[])[i]
  if (i <= 16) {
    const j = i - 3, th = (j * 100 * Math.PI) / 180
    return [-10 + 1.5 * j, 6 + 2.6 * Math.cos(th), 2.6 * Math.sin(th)]
  }
  if (i <= 20) return ([[12, 5, 1], [14, 3, 0.5], [14.5, 1, 0], [13, -0.5, 0]] as V[])[i - 17]
  if (i <= 27) { const m = i - 21; return [10 - 3.3 * m, -1, 0.6 * (m % 2 ? -1 : 1)] }
  if (i <= 31) return ([[-12.5, -1.5, 0], [-14, -3.5, 0], [-13.5, -5.5, 0], [-11.5, -6, 0]] as V[])[i - 28]
  if (i <= 38) { const m = i - 32; return [-9.8 + 3.3 * m, -5.8, 0.6 * (m % 2 ? -1 : 1)] }
  return ([[12.5, -6.5, 0.5], [14.5, -8, 1], [16, -9.5, 1]] as V[])[i - 39]
})

// ---------- animación ----------
const clamp = (v: number) => Math.min(1, Math.max(0, v))
const ease = (v: number) => v < 0.5 ? 4 * v ** 3 : 1 - (-2 * v + 2) ** 3 / 2
const lerp = (a: number, b: number, k: number) => a + (b - a) * k
// cuándo se pliega cada aminoácido: la hélice primero (estructura local), luego la horquilla β
const foldStart = res.map((r, i) => r.ss === 'H' ? 1.0 + (i - 3) * 0.045 : r.ss === 'E' ? 2.0 + (i < 30 ? 0 : 0.35) + (i % 7) * 0.03 : 1.6 + i * 0.025)
const FOLD = 1.3
const END = Math.max(...foldStart) + FOLD   // ≈ 4.0 s
const SPEED = 0.5 // 1 = velocidad original (~4 s); 0.5 = la mitad de rápido (~8 s)
const t = ref(99) // segundos desde el inicio; 99 = estado final
let raf = 0, t0 = 0
function tick(now: number) {
  t.value = ((now - t0) / 1000) * SPEED
  if (t.value < END + 1.5) raf = requestAnimationFrame(tick)
}
function replay() {
  cancelAnimationFrame(raf)
  if (window.matchMedia?.('(prefers-reduced-motion: reduce)').matches) { t.value = 99; return }
  t0 = performance.now(); t.value = 0
  raf = requestAnimationFrame(tick)
}
onSlideEnter(replay)
onBeforeUnmount(() => cancelAnimationFrame(raf))

// ---------- proyección ----------
const PX = 9.5          // px por Å
const CY = 96
const CX0 = 300, CX1 = 620
const global = computed(() => ease(clamp((t.value - 0.7) / (END - 0.7))))
const center = computed(() => lerp(CX0, CX1, global.value))
// el listón gira un poco mientras se pliega, para que se lea en 3D
const rotY = computed(() => lerp(75, 34, global.value) * Math.PI / 180)
const rotX = 22 * Math.PI / 180
function rotate(p: V, ky: number): V {
  const a = rotY.value * ky
  const x1 = p[0] * Math.cos(a) + p[2] * Math.sin(a)
  const z1 = -p[0] * Math.sin(a) + p[2] * Math.cos(a)
  const y2 = p[1] * Math.cos(rotX) - z1 * Math.sin(rotX)
  const z2 = p[1] * Math.sin(rotX) + z1 * Math.cos(rotX)
  return [x1, y2, z2]
}

// posición actual de cada aminoácido (mezcla recta ↔ plegada) y su avance de plegado
const pts = computed(() => res.map((r, i) => {
  const k = ease(clamp((t.value - foldStart[i]) / FOLD))
  const s = straight[i], f = rotate(folded[i], 1)
  const p: V = [lerp(s[0], f[0], k), lerp(s[1], f[1], k), lerp(s[2], f[2], k)]
  return { ...r, i, k, p, sx: center.value + p[0] * PX, sy: CY - p[1] * PX }
}))

// curva suave (Catmull-Rom) muestreada entre aminoácidos → segmentos del listón
const SUB = 7
const segs = computed(() => {
  const P = pts.value
  const at = (j: number) => P[Math.max(0, Math.min(N - 1, j))]
  const out: { x1: number, y1: number, x2: number, y2: number, z: number, w: number, ss: string, key: string }[] = []
  let prev: { x: number, y: number, z: number } | null = null
  for (let i = 0; i < N - 1; i++) {
    const p0 = at(i - 1).p, p1 = at(i).p, p2 = at(i + 1).p, p3 = at(i + 2).p
    for (let s = 0; s <= SUB; s++) {
      if (i > 0 && s === 0) continue
      const u = s / SUB, u2 = u * u, u3 = u2 * u
      const c = (a: number, b: number, cc: number, d: number) => 0.5 * ((2 * b) + (-a + cc) * u + (2 * a - 5 * b + 4 * cc - d) * u2 + (-a + 3 * b - 3 * cc + d) * u3)
      const X = c(p0[0], p1[0], p2[0], p3[0]), Y = c(p0[1], p1[1], p2[1], p3[1]), Z = c(p0[2], p1[2], p2[2], p3[2])
      const cur = { x: center.value + X * PX, y: CY - Y * PX, z: Z }
      if (prev) {
        const r = u < 0.5 ? P[i] : P[i + 1]
        // ancho: listón ancho con letras mientras es secuencia; al plegarse, hélice media, hebra ancha, loop fino
        const wf = r.ss === 'H' ? 6.5 : r.ss === 'E' ? 9 : 3
        out.push({ x1: prev.x, y1: prev.y, x2: cur.x, y2: cur.y, z: (prev.z + cur.z) / 2, w: lerp(15, wf, r.k), ss: r.ss, key: `${i}-${s}` })
      }
      prev = cur
    }
  }
  return out.sort((a, b) => a.z - b.z)
})
const COL: Record<string, string> = { H: 'var(--teal)', E: 'var(--leaf)', L: '#cfc9b4' }
// sombreado por profundidad mezclando con el fondo (sin transparencia, para que no se marquen las uniones)
const shade = (ss: string, z: number) => `color-mix(in srgb, ${COL[ss]} ${Math.round(45 + 55 * clamp((z + 4) / 8))}%, #08130f)`

// flechas al final de las hebras β (aparecen al terminar de plegarse)
const arrows = computed(() => [27, 38].map(e => {
  const a = pts.value[e - 1], b = pts.value[e]
  const dx = b.sx - a.sx, dy = b.sy - a.sy, L = Math.hypot(dx, dy) || 1
  const ux = dx / L, uy = dy / L, nx = -uy, ny = ux
  const tipx = b.sx + ux * 11, tipy = b.sy + uy * 11
  return { d: `M${b.sx + nx * 9},${b.sy + ny * 9} L${tipx},${tipy} L${b.sx - nx * 9},${b.sy - ny * 9} Z`, o: b.k }
}))

const intro = (i: number) => clamp((t.value - 0.05 - i * 0.012) / 0.25)
const reveal = computed(() => clamp((t.value - 0.05) / 0.6))
const labels = computed(() => clamp((t.value - END) / 0.5))
const helixLab = computed(() => { const p = pts.value[16]; return { x: p.sx + 26, y: p.sy - 26 } })
const sheetLab = computed(() => { const p = pts.value[38]; return { x: p.sx + 30, y: p.sy + 4 } })
</script>

<template>
  <div class="afi">
    <svg viewBox="0 0 900 200" class="rb" role="img" aria-label="la secuencia de aminoácidos, como un listón, se desplaza a la derecha y se pliega en una hélice alfa y una hoja beta" @click="replay">
      <!-- rótulo que acompaña al listón -->
      <text :x="center - 220 * (1 - global)" y="36" class="cap" :style="{ opacity: 0.6 * reveal * (1 - clamp(global * 2.5)) }">secuencia · 42 aminoácidos</text>
      <text :x="center - 150" y="-4" class="cap" :style="{ opacity: 0.6 * clamp((global - 0.6) / 0.4) }">estructura 3D</text>

      <!-- máscara de entrada: el listón aparece de N a C -->
      <defs>
        <clipPath id="rb-reveal"><rect x="0" y="-40" :width="40 + 880 * reveal" height="300" /></clipPath>
      </defs>

      <g clip-path="url(#rb-reveal)">
        <!-- borde oscuro + relleno, de atrás hacia adelante -->
        <g v-for="s in segs" :key="s.key">
          <line :x1="s.x1" :y1="s.y1" :x2="s.x2" :y2="s.y2" :stroke-width="s.w + 2.2" class="edge" />
          <line :x1="s.x1" :y1="s.y1" :x2="s.x2" :y2="s.y2" :stroke-width="s.w" class="rib" :style="{ stroke: shade(s.ss, s.z) }" />
        </g>
        <path v-for="(a, k) in arrows" :key="'a' + k" :d="a.d" class="arrow" :style="{ opacity: a.o }" />

        <!-- letras de la secuencia: se ven mientras el listón está recto -->
        <text v-for="p in pts" :key="'t' + p.i" :x="p.sx" :y="p.sy + 3.8" class="aa" text-anchor="middle"
          :style="{ opacity: intro(p.i) * clamp(1 - p.k * 2.2) }">{{ p.a }}</text>
      </g>

      <!-- extremos y etiquetas -->
      <text :x="pts[0].sx - 12" :y="pts[0].sy + 4" class="end" text-anchor="end" :style="{ opacity: reveal }">N</text>
      <text :x="pts[N - 1].sx + 12" :y="pts[N - 1].sy + 4" class="end" :style="{ opacity: reveal }">C</text>
      <g :style="{ opacity: labels }">
        <text :x="helixLab.x" :y="helixLab.y" class="lab t-h">hélice α</text>
        <text :x="sheetLab.x" :y="sheetLab.y" class="lab t-e">hoja β</text>
      </g>
    </svg>
  </div>
</template>

<style scoped>
.rb { width: 100%; height: auto; display: block; overflow: visible; color: var(--ink); cursor: pointer; }
.cap { fill: currentColor; font-family: var(--font-mono); font-size: 11px; letter-spacing: .06em; }
.end { fill: var(--sun); font-family: var(--font-mono); font-size: 12px; font-weight: 600; }

.edge { stroke: #07100c; stroke-linecap: butt; }
.rib { stroke-linecap: round; }
.rib-H { stroke: var(--teal); }
.rib-E { stroke: var(--leaf); }
.rib-L { stroke: #cfc9b4; }
.arrow { fill: var(--leaf); stroke: #07100c; stroke-width: 1; stroke-linejoin: round; }
.aa { fill: #08130f; font-family: var(--font-mono); font-size: 10.5px; font-weight: 600; pointer-events: none; }

.lab { font-family: var(--font-mono); font-size: 12px; }
.t-h { fill: var(--teal); }
.t-e { fill: var(--leaf); }
</style>
