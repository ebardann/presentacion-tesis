<script setup lang="ts">
// Dos enfoques de interpretabilidad mecanística.
// A · ciencia normal sobre la red: mirar neuronas/circuitos, seguir el flujo, experimentar.
// B · partir de features hipotetizadas: extraerlas con objetivos de reconstrucción, la red queda de lado.
const L = [0, 1, 2, 3].map(l => ({ x: 30 + l * 62, ys: [28, 62, 96, 130] }))
const edges = L.slice(0, -1).flatMap((a, l) => a.ys.flatMap((y1, i) => L[l + 1].ys.map((y2, j) => ({ x1: a.x, y1, x2: L[l + 1].x, y2, hot: (l === 0 && i === 1 && j === 2) || (l === 1 && i === 2 && j === 1) || (l === 2 && i === 1 && j === 1) }))))
const hotNodes = ['0-1', '1-2', '2-1', '3-1']
const feats = ['hélice α', 'contacto i–j', 'hoja β', 'bolsillo', '…']
</script>

<template>
  <div class="ta">
    <!-- A -->
    <div class="panel">
      <div class="hd"><span class="n">01</span><span class="t">ciencia normal sobre la red</span></div>
      <div class="tag">bottom-up · desde el modelo</div>
      <svg viewBox="0 0 380 160" class="fig" aria-label="mirar la red y experimentar sobre ella">
        <defs>
          <marker id="ta-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" class="fa" /></marker>
        </defs>
        <line v-for="(e, i) in edges" :key="i" v-bind="e" :class="e.hot ? 'eh' : 'e'" />
        <g v-for="(c, l) in L" :key="l">
          <circle v-for="(y, k) in c.ys" :key="k" :cx="c.x" :cy="y" r="6" :class="hotNodes.includes(`${l}-${k}`) ? 'nh' : 'n'" />
        </g>
        <!-- flujo de datos -->
        <circle r="3.5" class="pulse"><animateMotion dur="2.6s" repeatCount="indefinite" path="M30,62 L92,96 L154,62 L216,62" /></circle>
        <!-- lupa -->
        <circle cx="92" cy="96" r="17" class="lens" />
        <line x1="104" y1="108" x2="116" y2="120" class="lens-h" />
        <!-- ciclo experimental -->
        <g transform="translate(300,78)">
          <path d="M0,-44 A44,44 0 0 1 38,22" class="cyc" marker-end="url(#ta-a)" />
          <path d="M38,22 A44,44 0 0 1 -38,22" class="cyc" marker-end="url(#ta-a)" />
          <path d="M-38,22 A44,44 0 0 1 0,-44" class="cyc" marker-end="url(#ta-a)" />
          <text x="0" y="-50" class="cl" text-anchor="middle">hipótesis</text>
          <text x="50" y="46" class="cl" text-anchor="middle">intervenir</text>
          <text x="-50" y="46" class="cl" text-anchor="middle">observar</text>
          <text x="0" y="4" class="cl dim" text-anchor="middle">× agentes</text>
        </g>
      </svg>
      <p>mirar las <b>neuronas y circuitos</b> de la red, estudiar cómo se relacionan, <b>seguir el flujo de datos</b> y correr experimentos —a escala agéntica— para poner a prueba las explicaciones.</p>
    </div>

    <!-- B -->
    <div class="panel">
      <div class="hd"><span class="n">02</span><span class="t">partir de features hipotetizadas</span></div>
      <div class="tag">top-down · desde la hipótesis</div>
      <svg viewBox="0 0 380 160" class="fig" aria-label="extraer features con objetivos de reconstrucción">
        <defs>
          <marker id="tb-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" class="fa" /></marker>
        </defs>
        <!-- lista de features -->
        <g v-for="(f, i) in feats" :key="f">
          <rect x="0" :y="10 + i * 28" width="96" height="20" rx="10" class="chip" />
          <text x="48" :y="24 + i * 28" class="ct" text-anchor="middle">{{ f }}</text>
        </g>
        <line x1="102" y1="80" x2="140" y2="80" class="ar" marker-end="url(#tb-a)" />
        <!-- encoder / decoder -->
        <path d="M146,40 L196,62 L196,98 L146,120 Z" class="enc" />
        <path d="M200,62 L250,40 L250,120 L200,98 Z" class="enc" />
        <text x="198" y="138" class="cl" text-anchor="middle">diccionario · SAE</text>
        <line x1="256" y1="80" x2="282" y2="80" class="ar" marker-end="url(#tb-a)" />
        <text x="332" y="76" class="eq" text-anchor="middle">min ‖x − x̂‖²</text>
        <text x="332" y="92" class="cl dim" text-anchor="middle">+ objetivos cada</text>
        <text x="332" y="104" class="cl dim" text-anchor="middle">vez más finos</text>
        <!-- red original, apartada -->
        <g transform="translate(300,118)" class="ghost">
          <rect x="-32" y="0" width="76" height="34" rx="4" />
          <text x="6" y="21" text-anchor="middle">red original</text>
        </g>
      </svg>
      <p>empezar con una <b>lista de features esperadas</b> e intentar extraerlas todas, diseñando <b>objetivos de reconstrucción</b> cada vez más sofisticados — usualmente <b>ignorando la red original</b>.</p>
    </div>
  </div>
</template>

<style scoped>
.ta { display: grid; grid-template-columns: 1fr 1fr; gap: 1.6rem; }
.panel { border: 1px solid var(--accent-soft); border-radius: 6px; padding: .8rem 1rem .6rem; background: rgba(0, 0, 0, .25); }
.hd { display: flex; gap: .7rem; align-items: baseline; font-family: var(--font-mono); }
.n { color: var(--accent); font-size: .8rem; font-weight: 500; }
.t { font-size: 1rem; }
.tag { font-family: var(--font-mono); font-size: .68rem; letter-spacing: .08em; opacity: .5; margin: .15rem 0 .4rem 1.75rem; }
.fig { width: 100%; height: auto; display: block; overflow: visible; color: var(--ink); }
.panel p { font-size: .82rem !important; line-height: 1.45 !important; margin: .5rem 0 0; opacity: .88; }
.e { stroke: var(--ink); stroke-width: .6; opacity: .14; }
.eh { stroke: var(--accent); stroke-width: 1.8; }
circle.n { fill: var(--bg); stroke: var(--ink); stroke-width: 1; opacity: .45; }
.nh { fill: var(--accent); }
.pulse { fill: var(--teal); filter: drop-shadow(0 0 4px var(--teal)); }
.lens { fill: rgba(63, 217, 199, .08); stroke: var(--teal); stroke-width: 1.6; }
.lens-h { stroke: var(--teal); stroke-width: 3; stroke-linecap: round; }
.cyc { fill: none; stroke: var(--accent); stroke-width: 1.3; opacity: .8; }
.fa { fill: var(--accent); }
.cl { fill: currentColor; font-family: var(--font-mono); font-size: 10px; }
.cl.dim { opacity: .55; }
.chip { fill: rgba(63, 217, 199, .1); stroke: var(--teal); stroke-width: 1; }
.ct { fill: currentColor; font-family: var(--font-mono); font-size: 9.5px; }
.ar { stroke: currentColor; stroke-width: 1.2; opacity: .5; }
.enc { fill: rgba(255, 194, 75, .1); stroke: var(--accent); stroke-width: 1.2; }
.eq { fill: var(--accent); font-family: var(--font-mono); font-size: 11px; }
.ghost { opacity: .28; }
.ghost rect { fill: none; stroke: currentColor; stroke-dasharray: 3 3; }
.ghost text { fill: currentColor; font-family: var(--font-mono); font-size: 9px; }
</style>
