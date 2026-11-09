<script setup lang="ts">
import { computed } from 'vue'
import { useSlideContext } from '@slidev/client'

// Diagrama de la arquitectura de AF3.
// focus: nodo que se resalta a partir del click `at` (el slide debe declarar `clicks`).
// visited: nodos ya explicados (se marcan con ✓).
// Los nodos msa y pairformer llevan view-transition-name para hacer morph
// hacia el chip del slide siguiente (transition: view-transition).
const props = withDefaults(defineProps<{ focus?: string, at?: number, visited?: string[] }>(), { at: 1, visited: () => [] })
const { $clicks } = useSlideContext()
const active = computed(() => props.focus && $clicks.value >= props.at ? props.focus : null)

const W = 940, H = 290
const nodes = [
  { id: 'inputs', x: 0, y: 100, w: 135, h: 90, t: 'inputs', s: 'seq · msa · templates · ligandos' },
  { id: 'embedder', x: 168, y: 125, w: 112, h: 40, t: 'embedder' },
  { id: 'msa', x: 313, y: 125, w: 128, h: 40, t: 'MSA', kind: 'msa', vt: 'msa-box' },
  { id: 'pairformer', x: 474, y: 88, w: 142, h: 114, t: 'Pairformer ×48', s: 'single H · pair Z + recycling', kind: 'pf', vt: 'pf-box' },
  { id: 'diffusion', x: 652, y: 30, w: 132, h: 72, t: 'difusión', s: 'denoising iterativo', kind: 'diff' },
  { id: 'distogram', x: 652, y: 205, w: 132, h: 50, t: 'distograma' },
  { id: 'coords', x: 818, y: 14, w: 122, h: 40, t: 'coords. X', kind: 'out' },
  { id: 'confidence', x: 818, y: 80, w: 122, h: 62, t: 'confianza', s: 'plddt · pae · iptm' },
]
const pct = (v: number, of: number) => `${(v / of) * 100}%`
const wires = [
  'M135,145 H164', 'M280,145 H309', 'M441,145 H470',
  'M616,120 H634 V66 H648', 'M616,175 H634 V230 H648',
  'M784,52 H800 V34 H814', 'M784,82 H800 V111 H814',
]
</script>

<template>
  <div class="af" :class="{ dim: active }" :style="{ aspectRatio: `${W} / ${H}` }">
    <svg :viewBox="`0 0 ${W} ${H}`" class="wires" aria-hidden="true">
      <defs>
        <marker id="af-arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M0,0 L10,5 L0,10 z" class="ah" />
        </marker>
      </defs>
      <path v-for="(d, i) in wires" :key="i" :d="d" marker-end="url(#af-arr)" />
    </svg>
    <div v-for="n in nodes" :key="n.id" class="node" :class="[n.kind, { on: active === n.id, done: visited.includes(n.id) }]"
      :style="{ left: pct(n.x, W), top: pct(n.y, H), width: pct(n.w, W), height: pct(n.h, H), viewTransitionName: n.vt }">
      <span class="t">{{ n.t }}</span>
      <span v-if="n.s" class="s">{{ n.s }}</span>
      <span v-if="visited.includes(n.id)" class="ck">✓</span>
    </div>
  </div>
</template>

<style scoped>
.af { position: relative; width: 100%; }
.wires { position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; }
.wires path { fill: none; stroke: var(--leaf); stroke-width: 1.3; opacity: .7; transition: opacity .4s; }
.ah { fill: var(--leaf); }
.af.dim .wires path { opacity: .2; }

.node {
  position: absolute; box-sizing: border-box; display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: .2rem; text-align: center; padding: .3rem .5rem; border-radius: 4px;
  border: 1px solid rgba(241, 236, 216, .35); background: #161b18; color: var(--ink);
  font-family: var(--font-mono); transition: opacity .45s ease, transform .45s ease, box-shadow .45s ease;
}
.t { font-size: 13px; line-height: 1.2; }
.s { font-size: 10.5px; line-height: 1.25; opacity: .65; }
.msa { border-color: var(--sun); background: #221c08; }
.pf { border-color: var(--sun); background: #221c08; }
.diff { border-color: var(--teal); background: #0a201e; }
.out { border-color: var(--leaf); background: #12240c; color: var(--leaf); }

.af.dim .node { opacity: .22; }
.af.dim .node.on { opacity: 1; transform: scale(1.12); z-index: 2; box-shadow: 0 0 0 1px var(--sun), 0 0 28px rgba(255, 194, 75, .45); }
.node.done { opacity: .5; }
.ck { position: absolute; top: -.55rem; right: -.45rem; font-size: 11px; color: var(--leaf); background: var(--bg); border: 1px solid var(--leaf); border-radius: 999px; width: 1.1rem; height: 1.1rem; display: grid; place-items: center; }
</style>
