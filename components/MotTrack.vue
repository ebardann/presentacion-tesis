<script setup lang="ts">
// Rastreador de las tres motivaciones. Cada pill comparte view-transition-name (mot-1..3) con la
// tarjeta correspondiente de <Motivaciones>, así las tarjetas se encogen en el rastreador al avanzar.
defineProps<{ active: 1 | 2 | 3 }>()
const items = [
  { n: '01', t: 'Interpretabilidad', tone: 'sun' },
  { n: '02', t: 'AlphaFold 3', tone: 'leaf' },
  { n: '03', t: 'La brecha', tone: 'coral' },
]
</script>

<template>
  <div class="mt" aria-label="motivaciones">
    <span class="lbl">motivación</span>
    <span v-for="(it, i) in items" :key="it.n" class="pill" :class="[`t-${it.tone}`, { on: active === i + 1 }]"
      :style="{ viewTransitionName: `mot-${i + 1}` }">
      <b>{{ it.n }}</b><span class="t">{{ it.t }}</span>
    </span>
  </div>
</template>

<style scoped>
.mt { display: flex; align-items: center; gap: .5rem; margin: -.5rem 0 .9rem; font-family: var(--font-mono); }
.lbl { font-size: .68rem; letter-spacing: .1em; text-transform: uppercase; opacity: .45; margin-right: .3rem; }
.pill { --c: var(--sun); --cs: rgba(255, 194, 75, .22); display: inline-flex; align-items: center; gap: .45rem;
  padding: .22rem .7rem; border: 1px solid var(--cs); border-radius: 999px; font-size: .72rem; opacity: .45;
  background: rgba(0, 0, 0, .25); }
.t-sun   { --c: var(--sun);   --cs: rgba(255, 194, 75, .3); }
.t-leaf  { --c: var(--leaf);  --cs: rgba(143, 227, 106, .3); }
.t-coral { --c: var(--coral); --cs: rgba(255, 111, 89, .3); }
.pill b { color: var(--c); font-weight: 600; }
.pill.on { opacity: 1; border-color: var(--c); box-shadow: 0 0 16px var(--cs);
  background: linear-gradient(180deg, color-mix(in srgb, var(--c) 12%, transparent), rgba(0, 0, 0, .25)); }
.pill.on .t { color: var(--ink); }
</style>
