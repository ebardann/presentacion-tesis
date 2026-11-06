<script setup lang="ts">
import { useSlideContext } from '@slidev/client'
// el slide debe declarar `clicks: 2` en su frontmatter
const { $clicks } = useSlideContext()
// Ilustración de activation patching en tres corridas:
// clean (msa profundo) · corrupted (msa superficial) · patched (corrupted + h del clean en el bloque ℓ).
const lanes = [
  { y: 55, n: '01', name: 'clean run', input: 'msa profundo', kind: 'clean' },
  { y: 170, n: '02', name: 'corrupted run', input: 'msa superficial', kind: 'bad' },
  { y: 285, n: '03', name: 'patched run', input: 'msa superficial', kind: 'patch' },
]
const blocks = [
  { x: 330, t: '1' },
  { x: 400, t: '…' },
  { x: 480, t: 'ℓ' },
  { x: 560, t: '…' },
]
const BW = 56
const BH = 44

function blockClass(kind: string, i: number) {
  if (kind === 'clean') return 'clean'
  if (kind === 'bad') return 'bad'
  if (i < 2) return 'bad'      // upstream: misma computación corrupta
  if (i === 2) return 'clean'  // h reemplazada por la del clean run
  return 'patch'               // downstream: recomputado a partir de h'
}
</script>

<template>
  <svg class="pr" viewBox="0 0 920 340" role="img" aria-label="clean, corrupted y patched run">
    <defs>
      <marker id="pr-arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M0,0 L10,5 L0,10 z" fill="currentColor" />
      </marker>
      <marker id="pr-arr-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M0,0 L10,5 L0,10 z" class="f-clean" />
      </marker>
    </defs>

    <g v-for="(l, li) in lanes" :key="l.n" class="step" :class="{ off: $clicks < li }">
      <!-- etiqueta -->
      <text x="0" :y="l.y - 6" class="lbl-n" :class="'t-' + (l.kind === 'patch' ? 'patch' : l.kind)">{{ l.n }}</text>
      <text x="0" :y="l.y + 14" class="lbl">{{ l.name }}</text>

      <!-- input -->
      <rect x="150" :y="l.y - BH / 2" width="140" :height="BH" rx="5" class="box" :class="l.kind === 'clean' ? 'clean' : 'bad'" />
      <text x="220" :y="l.y + 5" class="txt" text-anchor="middle">{{ l.input }}</text>

      <!-- flechas entre cajas -->
      <line x1="290" :y1="l.y" x2="326" :y2="l.y" class="wire" marker-end="url(#pr-arr)" />
      <line v-for="(b, i) in blocks.slice(0, -1)" :key="'w' + i"
        :x1="b.x + BW" :y1="l.y" :x2="blocks[i + 1].x - 4" :y2="l.y" class="wire" marker-end="url(#pr-arr)" />
      <line :x1="560 + BW" :y1="l.y" x2="656" :y2="l.y" class="wire" marker-end="url(#pr-arr)" />

      <!-- bloques pairformer -->
      <g v-for="(b, i) in blocks" :key="'b' + i">
        <rect :x="b.x" :y="l.y - BH / 2" :width="BW" :height="BH" rx="4" class="box" :class="blockClass(l.kind, i)" />
        <text :x="b.x + BW / 2" :y="l.y + 5" class="txt mono" text-anchor="middle">{{ b.t }}</text>
      </g>
      <text x="508" :y="l.kind === 'patch' ? l.y + BH / 2 + 15 : l.y - BH / 2 - 6" class="h" text-anchor="middle"
        :class="l.kind === 'bad' ? 't-bad' : 't-clean'">{{ l.kind === 'clean' ? 'h_source' : l.kind === 'bad' ? 'h_target' : "h'" }}</text>

      <!-- output -->
      <rect x="660" :y="l.y - BH / 2" width="260" :height="BH" rx="5" class="box" :class="l.kind" />
      <text x="790" :y="l.y - 3" class="txt" text-anchor="middle">
        {{ l.kind === 'clean' ? 'contacto (i, j) presente' : l.kind === 'bad' ? 'contacto (i, j) perdido' : '¿vuelve el contacto?' }}
      </text>
      <text x="790" :y="l.y + 14" class="sub" text-anchor="middle">
        {{ l.kind === 'clean' ? 'd(i, j) < τ  ✓' : l.kind === 'bad' ? 'd(i, j) > τ  ✗' : 'sí → h en ℓ es causal' }}
      </text>
    </g>

    <!-- cabecera de columnas -->
    <text x="220" y="14" class="col" text-anchor="middle">input</text>
    <text x="445" y="14" class="col" text-anchor="middle">pairformer · bloques</text>
    <text x="790" y="14" class="col" text-anchor="middle">difusión → coordenadas</text>

    <!-- flecha de patch: h del clean → bloque ℓ del patched -->
    <g class="step" :class="{ off: $clicks < 2 }">
      <path d="M508,77 V108 H468 V224 H508 V259" class="patch-wire" marker-end="url(#pr-arr-g)" />
      <text x="522" y="104" class="patch-lbl">copiar h_source → h'</text>
      <text x="522" y="120" class="patch-lbl dim">m: pares (i, j) · canales · capa · recycle</text>
    </g>
  </svg>
</template>

<style scoped>
.pr { width: 100%; height: auto; max-height: 275px; display: block; color: var(--green-ink); overflow: visible; }
.step { transition: opacity .35s ease; }
.step.off { opacity: 0; }
.box { stroke-width: 1.4; }
.box.clean { fill: rgba(127, 255, 181, .14); stroke: var(--green-fg); }
.box.bad { fill: rgba(255, 58, 47, .12); stroke: var(--red-fg); }
.box.patch { fill: rgba(247, 181, 0, .12); stroke: var(--red-amber); }
.f-clean { fill: var(--green-fg); }
.wire { stroke: currentColor; stroke-width: 1.2; opacity: .45; }
.txt { fill: currentColor; font-family: var(--font-body); font-size: 14px; font-weight: 300; }
.mono { font-family: var(--font-mono); font-size: 15px; }
.sub { fill: currentColor; font-family: var(--font-mono); font-size: 11.5px; opacity: .65; }
.lbl-n { font-family: var(--font-mono); font-size: 13px; font-weight: 500; letter-spacing: .06em; }
.lbl { fill: currentColor; font-family: var(--font-mono); font-size: 14px; }
.t-clean { fill: var(--green-fg); }
.t-bad { fill: var(--red-fg); }
.t-patch { fill: var(--red-amber); }
.h { font-family: var(--font-mono); font-size: 12px; }
.col { fill: currentColor; font-family: var(--font-mono); font-size: 11.5px; letter-spacing: .08em; opacity: .5; }
.patch-wire { fill: none; stroke: var(--green-fg); stroke-width: 1.8; stroke-dasharray: 5 4; }
.patch-lbl { fill: var(--green-fg); font-family: var(--font-mono); font-size: 12.5px; }
.patch-lbl.dim { opacity: .65; font-size: 11px; }
</style>
