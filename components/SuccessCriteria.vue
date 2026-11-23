<script setup lang="ts">
// Protocolo y controles organizados alrededor del criterio de éxito:
// "la explicación predice cuándo funciona, cuándo falla y qué queda intacto".
// Cada columna = una parte de la predicción, con los pasos / controles que la ponen a prueba.
const cols = [
  {
    k: 'ok', tone: 'leaf', q: 'cuándo funciona',
    d: 'copiar la feature devuelve el contacto (i,\u00a0j)',
    items: [
      { n: 'probe', w: '¿una dirección en Z_ij predice el contacto?', lv: 'decodificable' },
      { n: 'patch / rescate', w: 'copiarla del MSA profundo lo recupera', lv: 'causal' },
      { n: 'vía', w: 'path patching hasta la difusión', lv: 'mecanístico' },
    ],
  },
  {
    k: 'fail', tone: 'coral', q: 'cuándo falla',
    d: 'anticipar dónde el patch no debería funcionar',
    items: [
      { n: 'held-out', w: 'familias nuevas: aciertos y fallos predichos', lv: 'reproducible' },
      { n: 'contactos sin MSA', w: 'si no dependen del MSA, el patch no hace nada' },
      { n: 'leakage', w: 'post-cutoff ≠ sin homólogos en training' },
    ],
  },
  {
    k: 'keep', tone: 'teal', q: 'qué queda intacto',
    d: 'sólo cambia el contacto; el resto se preserva',
    items: [
      { n: 'no-change patch', w: "h' = h → mismo output bit a bit" },
      { n: 'edits random', w: 'igual norma → descarta daño genérico' },
      { n: 'pair-scaling', w: 'la perilla global cambia todo; la feature no' },
    ],
  },
]
</script>

<template>
  <div class="sc">
    <p class="hero">La explicación tiene que <b>predecir</b>:</p>
    <div class="cols">
      <div v-for="(c, ci) in cols" :key="c.k" class="col" :class="`t-${c.tone}`">
        <div class="head">
          <span class="num">{{ ci + 1 }}</span>
          <span class="q">{{ c.q }}</span>
        </div>
        <div class="d">{{ c.d }}</div>
        <div class="items">
          <div v-for="it in c.items" :key="it.n" class="it">
            <span class="n">{{ it.n }}</span>
            <span class="w">{{ it.w }}</span>
            <span v-if="it.lv" class="lv">{{ it.lv }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.sc { display: flex; flex-direction: column; gap: 1.1rem; }
.hero { font-size: 1.5rem !important; font-weight: 300 !important; line-height: 1.3 !important; margin: 0; color: var(--ink); }
.hero b { color: var(--accent); font-weight: 500; }

.cols { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.1rem; }
.col { --c: var(--leaf); --cs: rgba(143, 227, 106, .22); border: 1px solid var(--cs); border-top: 2px solid var(--c); border-radius: 6px;
  padding: .85rem 1rem 1rem; background: linear-gradient(180deg, color-mix(in srgb, var(--c) 8%, transparent), rgba(0, 0, 0, .25) 55%); }
.t-leaf  { --c: var(--leaf);  --cs: rgba(143, 227, 106, .22); }
.t-coral { --c: var(--coral); --cs: rgba(255, 111, 89, .22); }
.t-teal  { --c: var(--teal);  --cs: rgba(63, 217, 199, .22); }

.head { display: flex; align-items: baseline; gap: .6rem; }
.num { font-family: var(--font-display); font-size: 1.7rem; line-height: 1; color: var(--c); text-shadow: 0 0 14px var(--cs); }
.q { font-size: 1.3rem; font-weight: 400; color: var(--c); }
.d { font-size: .8rem; opacity: .75; margin-top: .35rem; font-weight: 300; line-height: 1.35; }

.items { margin-top: .75rem; border-top: 1px dashed var(--cs); }
.it { display: flex; flex-direction: column; gap: .1rem; padding: .42rem 0; border-bottom: 1px dashed var(--cs); }
.it:last-child { border-bottom: 0; padding-bottom: 0; }
.n { font-family: var(--font-mono); font-size: .8rem; font-weight: 500; color: var(--ink); }
.w { font-size: .72rem; opacity: .7; font-weight: 300; line-height: 1.35; }
.lv { font-family: var(--font-mono); font-size: .62rem; letter-spacing: .08em; color: var(--c); opacity: .9; }
</style>
