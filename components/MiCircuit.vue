<script setup lang="ts">
// Red esquemática: todas las conexiones tenues; un circuito (subgrafo) resaltado.
const layers = [0, 1, 2, 3, 4].map(l => ({
  x: 40 + l * 75,
  ys: Array.from({ length: 5 }, (_, k) => 30 + k * 38),
}))
// circuito: aristas [capa, nodo origen, nodo destino] (input → output, con una rama paralela)
const hotEdges = [[0, 1, 2], [0, 1, 3], [1, 2, 1], [1, 3, 3], [2, 1, 3], [2, 3, 3], [3, 3, 2]]
const hotKey = new Set(hotEdges.map(([l, a, b]) => `${l}-${a}-${b}`))
const hotNode = new Set(hotEdges.flatMap(([l, a, b]) => [`${l}-${a}`, `${l + 1}-${b}`]))
const edges: { x1: number, y1: number, x2: number, y2: number, hot: boolean }[] = []
for (let l = 0; l < layers.length - 1; l++) {
  layers[l].ys.forEach((y1, a) => layers[l + 1].ys.forEach((y2, b) => {
    edges.push({ x1: layers[l].x, y1, x2: layers[l + 1].x, y2, hot: hotKey.has(`${l}-${a}-${b}`) })
  }))
}
const isHot = (l: number, k: number) => hotNode.has(`${l}-${k}`)
</script>

<template>
  <svg class="mic" viewBox="0 0 380 230" role="img" aria-label="red con un circuito resaltado">
    <line v-for="(e, i) in edges.filter(e => !e.hot)" :key="'e' + i" v-bind="e" class="e" />
    <line v-for="(e, i) in edges.filter(e => e.hot)" :key="'h' + i" v-bind="e" class="eh" />
    <g v-for="(L, l) in layers" :key="l">
      <circle v-for="(y, k) in L.ys" :key="k" :cx="L.x" :cy="y" r="7" :class="isHot(l, k) ? 'nh' : 'n'" />
    </g>
    <text x="40" y="222" class="lab" text-anchor="middle">input</text>
    <text x="340" y="222" class="lab" text-anchor="middle">output</text>
    <text x="190" y="222" class="lab hot" text-anchor="middle">circuito = subgrafo causal</text>
  </svg>
</template>

<style scoped>
.mic { width: 100%; height: auto; display: block; overflow: visible; }
.e { stroke: var(--ink); stroke-width: .6; opacity: .1; }
.eh { stroke: var(--accent); stroke-width: 2; opacity: .9; }
.n { fill: var(--bg); stroke: var(--ink); stroke-width: 1; opacity: .35; }
.nh { fill: var(--accent); stroke: var(--accent); filter: drop-shadow(0 0 5px var(--accent)); }
.lab { fill: var(--ink); font-family: var(--font-mono); font-size: 11px; opacity: .55; }
.lab.hot { fill: var(--accent); opacity: 1; }
</style>
