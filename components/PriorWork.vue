<script setup lang="ts">
// Trabajo previo como matriz de cobertura: qué piezas cubre cada trabajo.
// 2 = sí · 1 = parcial · 0 = no
const cols = ['features', 'intervención', 'localizada', 'coords 3D']
const rows = [
  { w: 'InterPLM', m: 'ESM-2', v: [2, 0, 0, 0] },
  { w: 'PairSAE', m: 'Boltz-2', v: [2, 0, 0, 0] },
  { w: 'SAEFold', m: 'ESMFold', v: [2, 2, 2, 1] },
  { w: 'AlphaInterp', m: 'AF3', v: [1, 2, 1, 0] },
  { w: 'Pair scaling', m: 'AF3 · Boltz-2', v: [0, 2, 0, 2] },
]
</script>

<template>
  <div class="pw">
    <div class="grid">
      <div class="corner" />
      <div v-for="c in cols" :key="c" class="ch">{{ c }}</div>

      <template v-for="r in rows" :key="r.w">
        <div class="rw"><b>{{ r.w }}</b><span>{{ r.m }}</span></div>
        <div v-for="(v, j) in r.v" :key="j" class="cell"><i :class="'d' + v" /></div>
      </template>

      <div class="rw me"><b>Esta tesis</b><span>AF3</span></div>
      <div v-for="(c, j) in cols" :key="'me' + j" class="cell me"><i class="d2 glow" :style="{ animationDelay: `${j * 0.25}s` }" /></div>
    </div>

    <div class="legend">
      <span><i class="d2" />sí</span>
      <span><i class="d1" />parcial</span>
      <span><i class="d0" />no</span>
    </div>
  </div>
</template>

<style scoped>
.pw { display: flex; flex-direction: column; align-items: center; gap: .8rem; }
.grid { display: grid; grid-template-columns: 13rem repeat(4, 8.5rem); align-items: center; row-gap: .15rem; }
.ch { font-family: var(--font-mono); font-size: .8rem; letter-spacing: .05em; text-align: center; opacity: .65; padding-bottom: .4rem; border-bottom: 1px solid var(--accent-soft); }
.corner { border-bottom: 1px solid var(--accent-soft); align-self: stretch; }
.rw { display: flex; flex-direction: column; padding: .2rem 0; font-family: var(--font-mono); }
.rw b { font-size: .92rem; font-weight: 500; color: var(--ink); }
.rw span { font-size: .66rem; opacity: .5; }
.cell { display: flex; justify-content: center; }

i { display: inline-block; width: 1.05rem; height: 1.05rem; border-radius: 999px; box-sizing: border-box; }
.d2 { background: var(--ink); opacity: .85; }
.d1 { background: linear-gradient(90deg, var(--ink) 50%, transparent 50%); border: 1.5px solid var(--ink); opacity: .7; }
.d0 { border: 1.5px solid var(--ink); opacity: .25; }

.rw.me { border-top: 1px solid var(--accent-soft); margin-top: .3rem; padding-top: .45rem; }
.cell.me { border-top: 1px solid var(--accent-soft); margin-top: .3rem; padding-top: .45rem; align-self: stretch; align-items: center; }
.rw.me b { color: var(--accent); font-size: 1.05rem; }
.rw.me span { color: var(--accent); opacity: .8; }
.glow { background: var(--accent); opacity: 1; box-shadow: 0 0 12px var(--accent); animation: pop 2.4s ease-in-out infinite; }

.legend { display: flex; gap: 1.6rem; font-family: var(--font-mono); font-size: .7rem; opacity: .6; }
.legend span { display: flex; align-items: center; gap: .45rem; }
.legend i { width: .75rem; height: .75rem; }

@keyframes pop { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.25); } }
</style>
