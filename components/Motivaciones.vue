<script setup lang="ts">
// Motivación en tres partes: por qué interpretabilidad · por qué AF3 · qué falta en el trabajo previo.
const parts = [
  {
    n: '01', tone: 'sun', icon: 'net', t: 'Interpretabilidad',
    claim: 'Usamos modelos que no entendemos',
    out: 'el cómo, no sólo el qué',
  },
  {
    n: '02', tone: 'leaf', icon: 'fold', t: 'AlphaFold 3',
    claim: 'Un modelo central para la biología',
    out: 'en qué se basa cada predicción',
  },
  {
    n: '03', tone: 'coral', icon: 'gap', t: 'Trabajo previo',
    claim: 'Nadie sigue una feature hasta la estructura 3D',
    out: 'feature → coords 3D',
  },
]
</script>

<template>
  <div class="mot">
    <div class="cols">
      <div v-for="(p, i) in parts" :key="p.n" class="col" :class="`t-${p.tone}`" :style="{ animationDelay: `${i * 120}ms`, viewTransitionName: `mot-${i + 1}` }">
        <div class="head">
          <span class="num">{{ p.n }}</span>
          <svg class="ico" viewBox="0 0 40 40" aria-hidden="true">
            <template v-if="p.icon === 'net'">
              <line x1="8" y1="10" x2="20" y2="20" /><line x1="8" y1="30" x2="20" y2="20" />
              <line x1="20" y1="20" x2="32" y2="10" /><line x1="20" y1="20" x2="32" y2="30" />
              <circle cx="8" cy="10" r="3" /><circle cx="8" cy="30" r="3" />
              <circle cx="20" cy="20" r="4" class="hot" />
              <circle cx="32" cy="10" r="3" /><circle cx="32" cy="30" r="3" />
            </template>
            <template v-else-if="p.icon === 'fold'">
              <path d="M5,30 C10,8 15,8 18,20 S26,32 30,14 S36,8 36,8" class="bb" />
              <circle cx="11" cy="15" r="2.6" class="hot" /><circle cx="27" cy="22" r="2.6" class="hot" />
              <line x1="11" y1="15" x2="27" y2="22" class="dash" />
            </template>
            <template v-else>
              <!-- dos piezas que no se tocan: feature (izq.) · coordenadas (der.) -->
              <rect x="3" y="13" width="13" height="14" rx="2" />
              <rect x="24" y="13" width="13" height="14" rx="2" />
              <line x1="16" y1="20" x2="24" y2="20" class="dash" />
              <circle cx="20" cy="20" r="2.2" class="hot blink" />
            </template>
          </svg>
        </div>
        <div class="title">{{ p.t }}</div>
        <div class="claim">{{ p.claim }}</div>
        <div class="out"><span class="arr">→</span>{{ p.out }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.mot { display: flex; flex-direction: column; }
.cols { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.2rem; }

.col { --c: var(--sun); --cs: rgba(255, 194, 75, .22); display: flex; flex-direction: column;
  border: 1px solid var(--cs); border-top: 2px solid var(--c); border-radius: 6px; padding: 1rem 1.1rem; min-height: 15rem;
  background: linear-gradient(180deg, color-mix(in srgb, var(--c) 7%, transparent), rgba(0, 0, 0, .25) 55%);
  opacity: 0; animation: rise .5s ease forwards; }
.t-sun   { --c: var(--sun);   --cs: rgba(255, 194, 75, .22); }
.t-leaf  { --c: var(--leaf);  --cs: rgba(143, 227, 106, .22); }
.t-coral { --c: var(--coral); --cs: rgba(255, 111, 89, .22); }

.head { display: flex; align-items: flex-start; justify-content: space-between; }
.num { font-family: var(--font-display); font-size: 2.1rem; line-height: 1; color: var(--c); text-shadow: 0 0 18px var(--cs); }
.ico { width: 2.2rem; height: 2.2rem; overflow: visible; }
.ico line, .ico circle, .ico rect, .ico path { fill: none; stroke: var(--ink); stroke-width: 1.3; opacity: .7; }
.ico .bb { stroke-linecap: round; }
.ico .dash { stroke: var(--c); stroke-dasharray: 2 2; opacity: 1; }
.ico .hot { stroke: var(--c); fill: var(--c); opacity: 1; }
.ico .blink { animation: blink 1.4s steps(1) infinite; }

.title { font-family: var(--font-mono); font-size: .78rem; letter-spacing: .08em; text-transform: uppercase; color: var(--c); margin-top: .6rem; }
.claim { font-size: 1.4rem; font-weight: 300; line-height: 1.3; margin-top: .5rem; }


.out { font-family: var(--font-mono); font-size: .74rem; color: var(--c); margin-top: auto; padding-top: .55rem; border-top: 1px dashed var(--cs); }
.arr { margin-right: .45rem; }

@keyframes rise { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }
@keyframes blink { 50% { opacity: 0; } }
@media (prefers-reduced-motion: reduce) { .col { animation: none; opacity: 1; } .ico .blink { animation: none; } }
</style>
