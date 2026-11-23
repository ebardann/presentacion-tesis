<script setup lang="ts">
// Tabla de contenidos: cinco secciones como un recorrido, cada una con su tono y su pregunta.
// `from` = primera slide de la sección (routerMode: hash → #/n).
const sections = [
  { n: '01', t: 'Tesis', q: '¿qué propongo?', tone: 'leaf', from: 3, to: 8, icon: 'fold' },
  { n: '02', t: 'Motivación', q: '¿por qué importa?', tone: 'coral', from: 9, to: 11, icon: 'papers' },
  { n: '03', t: 'Justificación', q: '¿por qué estudiar AlphaFold es viable?', tone: 'sun', from: 12, to: 14, icon: 'layers' },
  { n: '04', t: 'Diseño', q: '¿cómo lo voy a probar?', tone: 'teal', from: 15, to: 17, icon: 'patch' },
  { n: '05', t: 'Estado actual', q: '¿dónde estoy?', tone: 'sun', from: 18, to: 18, icon: 'progress' },
]
const grid = Array.from({ length: 16 }, (_, k) => ({ r: Math.floor(k / 4), c: k % 4 }))
</script>

<template>
  <div class="toc-map">
    <div class="track" aria-hidden="true" />
    <a v-for="(s, i) in sections" :key="s.n" :href="`#/${s.from}`" class="sec" :class="`t-${s.tone}`" :style="{ animationDelay: `${i * 90}ms` }">
      <div class="top">
        <span class="dot" />
        <span class="range">{{ s.from === s.to ? s.from : `${s.from}–${s.to}` }}</span>
      </div>
      <div class="card">
        <div class="head">
          <span class="num">{{ s.n }}</span>
          <svg class="ico" viewBox="0 0 40 40" aria-hidden="true">
            <template v-if="s.icon === 'net'">
              <line x1="8" y1="10" x2="20" y2="20" /><line x1="8" y1="30" x2="20" y2="20" />
              <line x1="20" y1="20" x2="32" y2="10" /><line x1="20" y1="20" x2="32" y2="30" />
              <circle cx="8" cy="10" r="3" /><circle cx="8" cy="30" r="3" />
              <circle cx="20" cy="20" r="4" class="hot" />
              <circle cx="32" cy="10" r="3" /><circle cx="32" cy="30" r="3" />
            </template>
            <template v-else-if="s.icon === 'fold'">
              <path d="M5,30 C10,8 15,8 18,20 S26,32 30,14 S36,8 36,8" class="bb" />
              <circle cx="11" cy="15" r="2.6" class="hot" /><circle cx="27" cy="22" r="2.6" class="hot" />
              <line x1="11" y1="15" x2="27" y2="22" class="dash" />
            </template>
            <template v-else-if="s.icon === 'layers'">
              <rect x="6" y="6" width="28" height="6" rx="1.5" class="soft" />
              <rect x="6" y="17" width="28" height="6" rx="1.5" class="hot" />
              <rect x="6" y="28" width="28" height="6" rx="1.5" class="soft" />
            </template>
            <template v-else-if="s.icon === 'papers'">
              <rect x="12" y="5" width="20" height="26" rx="2" class="soft" />
              <rect x="7" y="10" width="20" height="26" rx="2" />
              <line x1="11" y1="17" x2="23" y2="17" /><line x1="11" y1="22" x2="23" y2="22" /><line x1="11" y1="27" x2="18" y2="27" />
              <text x="30" y="38" class="q">?</text>
            </template>
            <template v-else-if="s.icon === 'patch'">
              <rect v-for="g in grid" :key="g.r + '-' + g.c" :x="5 + g.c * 8" :y="5 + g.r * 8" width="6" height="6" rx="1"
                :class="g.r === 1 && g.c === 2 ? 'cell hot-fill' : 'cell'" />
            </template>
            <template v-else>
              <rect x="4" y="16" width="32" height="8" rx="4" class="soft" />
              <rect x="4" y="16" width="14" height="8" rx="4" class="hot-fill" />
              <circle cx="22" cy="20" r="2" class="hot-fill blink" />
            </template>
          </svg>
        </div>
        <div class="title">{{ s.t }}</div>
        <div class="q">{{ s.q }}</div>
      </div>
    </a>
  </div>
</template>

<style scoped>
.toc-map { position: relative; display: grid; grid-template-columns: repeat(5, 1fr); gap: 1rem; }
.track { position: absolute; left: .5rem; right: .5rem; top: .62rem; border-top: 1px dashed rgba(241, 236, 216, .25); }

.sec { --c: var(--sun); --cs: rgba(255, 194, 75, .2); display: flex; flex-direction: column; gap: .7rem;
  color: var(--ink); text-decoration: none; border: 0 !important; opacity: 0; animation: rise .5s ease forwards; }
.t-sun   { --c: var(--sun);   --cs: rgba(255, 194, 75, .22); }
.t-leaf  { --c: var(--leaf);  --cs: rgba(143, 227, 106, .22); }
.t-coral { --c: var(--coral); --cs: rgba(255, 111, 89, .22); }
.t-teal  { --c: var(--teal);  --cs: rgba(63, 217, 199, .22); }

.top { display: flex; align-items: center; justify-content: space-between; position: relative; }
.dot { width: 1.25rem; height: 1.25rem; border-radius: 999px; background: var(--bg); border: 1.5px solid var(--c); box-shadow: 0 0 12px var(--cs); position: relative; }
.dot::after { content: ""; position: absolute; inset: 3px; border-radius: 999px; background: var(--c); }
.range { font-family: var(--font-mono); font-size: .62rem; letter-spacing: .08em; opacity: .45; }

.card { border: 1px solid var(--cs); border-top: 2px solid var(--c); border-radius: 6px; padding: .8rem .75rem .9rem;
  background: linear-gradient(180deg, color-mix(in srgb, var(--c) 7%, transparent), rgba(0, 0, 0, .25) 55%);
  min-height: 10rem; transition: transform .2s ease, box-shadow .2s ease; }
.sec:hover .card { transform: translateY(-3px); box-shadow: 0 0 26px var(--cs); }

.head { display: flex; align-items: flex-start; justify-content: space-between; }
.num { font-family: var(--font-display); font-size: 2rem; line-height: 1; color: var(--c); text-shadow: 0 0 18px var(--cs); }
.ico { width: 2rem; height: 2rem; overflow: visible; }
.ico line, .ico circle, .ico rect, .ico path { fill: none; stroke: var(--ink); stroke-width: 1.3; opacity: .7; }
.ico .bb { stroke-linecap: round; }
.ico .dash { stroke: var(--c); stroke-dasharray: 2 2; opacity: 1; }
.ico .hot { stroke: var(--c); fill: var(--c); opacity: 1; }
.ico .hot-fill { fill: var(--c); stroke: none; opacity: 1; }
.ico .soft { opacity: .3; }
.ico .cell { fill: var(--ink); stroke: none; opacity: .15; }
.ico .cell.hot-fill { fill: var(--c); opacity: 1; }
.ico text.q { fill: var(--c); font-family: var(--font-mono); font-size: 13px; }
.ico .blink { animation: blink 1.4s steps(1) infinite; }

.title { font-size: 1.1rem; font-weight: 400; margin-top: .75rem; line-height: 1.2; }
.q { font-family: var(--font-mono); font-size: .72rem; color: var(--c); margin-top: .3rem; letter-spacing: .02em; }

@keyframes rise { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }
@keyframes blink { 50% { opacity: 0; } }
@media (prefers-reduced-motion: reduce) { .sec { animation: none; opacity: 1; } .ico .blink { animation: none; } }
</style>
