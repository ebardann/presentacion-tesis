<script setup lang="ts">
import { computed } from 'vue'

// fondo con glitch intermitente: copias desplazadas en rgb + franjas recortadas + scanlines
const props = withDefaults(defineProps<{
  image: string // nombre del archivo en assets/, p.ej. "closing-bg.png"
  opacity?: number
  dim?: number // oscurecido central (0–1) para que el texto se lea
}>(), { opacity: 0.7, dim: 0.55 })

const images = import.meta.glob('../assets/*.{png,jpg,jpeg,webp}', { eager: true, import: 'default' }) as Record<string, string>
const src = computed(() => images[`../assets/${props.image}`])
</script>

<template>
  <div class="glitch-bg" :style="{ '--o': opacity, '--dim': dim }">
    <img :src="src" class="layer base" alt="">
    <img :src="src" class="layer g1" alt="">
    <img :src="src" class="layer g2" alt="">
    <div class="bar" />
    <div class="scan" />
    <div class="shade" />
  </div>
</template>

<style scoped>
.glitch-bg { position: absolute !important; inset: 0; overflow: hidden; z-index: 0 !important; pointer-events: none; }
.layer { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.base { opacity: var(--o); animation: jolt 5s infinite steps(1); }

/* copias tintadas: aparecen solo durante las ráfagas */
.g1, .g2 { opacity: 0; mix-blend-mode: screen; }
.g1 { filter: hue-rotate(-60deg) saturate(2.2); animation: slice-a 5s infinite steps(1); }
.g2 { filter: hue-rotate(140deg) saturate(2.4); animation: slice-b 5s infinite steps(1); animation-delay: .07s; }

/* barra de ruido que cruza la pantalla */
.bar {
  position: absolute; left: 0; right: 0; height: 9%; top: -10%;
  background: linear-gradient(180deg, transparent, rgba(63, 217, 199, .09), rgba(255, 194, 75, .06), transparent);
  mix-blend-mode: screen; animation: sweep 7s linear infinite;
}
.scan {
  position: absolute; inset: 0; mix-blend-mode: multiply;
  background: repeating-linear-gradient(0deg, rgba(0, 0, 0, .25) 0, rgba(0, 0, 0, .25) 1px, transparent 1px, transparent 3px);
}
.shade {
  position: absolute; inset: 0;
  background: radial-gradient(ellipse at 50% 50%, rgba(8, 19, 15, var(--dim)) 0%, rgba(8, 19, 15, calc(var(--dim) * .6)) 45%, rgba(8, 19, 15, .85) 100%);
}

@keyframes jolt {
  0%, 100% { transform: none; }
  61% { transform: translate(-6px, 0) skewX(-1.5deg); }
  62% { transform: translate(4px, 0); }
  63% { transform: none; }
  88% { transform: translate(0, 3px); }
  89% { transform: none; }
}
@keyframes slice-a {
  0%, 100% { opacity: 0; }
  60% { opacity: .55; clip-path: inset(18% 0 62% 0); transform: translate(-14px, 0); }
  61% { opacity: .55; clip-path: inset(55% 0 30% 0); transform: translate(10px, 0); }
  62% { opacity: .55; clip-path: inset(8% 0 85% 0); transform: translate(-22px, 0); }
  63% { opacity: 0; }
  87% { opacity: .45; clip-path: inset(70% 0 12% 0); transform: translate(16px, 0); }
  88% { opacity: 0; }
}
@keyframes slice-b {
  0%, 100% { opacity: 0; }
  60% { opacity: .5; clip-path: inset(40% 0 44% 0); transform: translate(12px, 0); }
  61% { opacity: .5; clip-path: inset(75% 0 8% 0); transform: translate(-9px, 0); }
  62% { opacity: .5; clip-path: inset(25% 0 66% 0); transform: translate(18px, 0); }
  63% { opacity: 0; }
  87% { opacity: .4; clip-path: inset(30% 0 58% 0); transform: translate(-12px, 0); }
  88% { opacity: 0; }
}
@keyframes sweep { from { top: -10%; } to { top: 110%; } }

@media (prefers-reduced-motion: reduce) {
  .base, .g1, .g2, .bar { animation: none; }
}
</style>
