---
theme: default
colorSchema: dark
routerMode: hash
title: mecanismos causales dentro de alphafold 3
info: |
  tesis · activation patching sobre un AF3 congelado.
  de una feature interna a un cambio selectivo y reproducible en la geometría 3D final.
fonts:
  sans: Inter
  serif: Cinzel
  mono: IBM Plex Mono
  weights: '200,300,400,500,600'
drawings:
  persist: false
transition: fade
duration: 30min
layout: default
class: theme-solar tone-sun
---

<Cover
  title="AlphaFold3"
  :status="['Interpretabilidad', 'JAX', 'Activation Patching']"
  :sub="['mecanismos causales', 'características', 'geometría 3D']"
  author="Emilio Bardán · tesis · 2026"
/>

<!--
Basado en el field assessment del 14 oct 2026 (assessment.pdf).
-->

---
class: theme-solar tone-sun
---

# Interpretabilidad mecanística

<Slashes :items="['features', 'circuitos', 'intervenciones']" />

<p class="lead">Ingeniería inversa de una red entrenada: identificar <b>qué representa</b> internamente y <b>qué algoritmo implementa</b>, a partir de sus pesos y activaciones.</p>

<div class="grid gap-10 mt-4" style="grid-template-columns:1.25fr 1fr">
<div class="rows compact">
  <div class="r"><span class="name">feature</span><span class="what">dirección en el espacio de activaciones que codifica una propiedad del input</span></div>
  <div class="r"><span class="name">superposición</span><span class="what">la red guarda más features que neuronas → una neurona ≠ un concepto</span></div>
  <div class="r"><span class="name">circuito</span><span class="what">subgrafo de features y pesos que implementa un cómputo concreto</span></div>
  <div class="r"><span class="name">intervención</span><span class="what">patch · ablación · steering: correlación no basta, hay que mover el output</span></div>
</div>
<div>
<MiCircuit />
</div>
</div>

<p class="note refs mt-3">circuits (Olah 2020) · superposición (Elhage 2022) · causal tracing (Meng 2022) · path patching (Wang 2022) · SAEs (Bricken 2023)</p>

---
class: theme-solar tone-teal
---

# Dos enfoques

<Slashes :items="['desde la red', 'desde las features']" />

<TwoApproaches class="mt-2" />

<p class="note mt-4">→ esta tesis: enfoque 01 · intervenir AF3 directamente; probes / SAEs sólo como candidatos</p>

---
class: theme-solar tone-leaf
---

# AlphaFold

<Slashes :items="['secuencia', 'estructura', 'all-atom']" />

<AlphaFoldIntro class="mt-2" />

<p class="note mt-5">AlphaFold permite acelerar el diseño de fármacos, el estudio de enfermedades, el desarrollo de vacunas y enzimas, y la comprensión de la vida a nivel molecular.</p>

---
class: theme-solar tone-leaf
---


# La tesis en una frase

<Slashes :items="['AF3 congelado', 'una feature', 'coordenadas finales']" />

<p class="big-quote">
Usar <b>activation patching</b> sobre un <b>AlphaFold 3 congelado</b> para conectar
<b>una feature o vía interna</b> con un <b>cambio selectivo y reproducible</b>
en las coordenadas 3D generadas por difusión.
</p>

<ThesisStrip class="mt-5" />

<div class="kv mt-4">
  <div><span class="k">selectivo</span> cambia la propiedad objetivo · el resto de la estructura se preserva</div>
  <div><span class="k">reproducible</span> se sostiene entre seeds, controles pareados y proteínas held-out</div>
</div>

<!--
El assessment lo identifica como la oportunidad abierta más fuerte en MI de predictores de estructura (p.5).
-->

---
class: theme-solar tone-coral
---

# La brecha abordada

<Slashes :items="['trabajo previo', 'qué falta']" />

| trabajo | qué mostró | qué **no** mostró |
|---|---|---|
| **alphainterp** · feldman & skolnick 2026 · AF3 | dependencia del modelo en sus datos de MSA | características ni circuitos interpretables, ni su efecto en la geometría |
| **pair scaling** · suzuki & amagasa 2026 · af3 + boltz-2 | escalar el pair rep amplía el sampling y recupera estados alternativos (86 proteínas) | perilla **global** — edita todas las features a la vez |
| **pairsae** · migliorini et al. 2026 · boltz-2 | sae sobre pair comprimido; features alineadas con anotaciones | sin intervenciones · sin msas |
| **saefold** · parsan et al. 2025 · esmfold | edit sae aumenta accesibilidad al solvente | ¿estado válido o daño / desorden? |
| interplm · adams et al. · esm-2 | features interpretables en plms | sobre el lenguaje, no el plegador |

<p class="note mt-4">→ el descubrimiento de features está más maduro que la explicación a nivel circuito.
la contribución: explicar un efecto selectivo <b>y su transmisión</b>, con held-out y controles.</p>

---
class: theme-solar tone-sun
clicks: 1
transition: view-transition
---

# Arquitectura de AF3

<Slashes :items="['trunk', 'difusión', 'heads']" />

<ArchFlow focus="msa" class="mt-8" />

<p class="note mt-10">recycling y pasos de difusión = cómputo del modelo, no tiempo físico de plegamiento.
recycles / pasos / samples por seed se leen del config instalado — no se asumen.</p>

---
class: theme-solar tone-sun
transition: view-transition
---

# Módulo MSA

<div class="vt-chip" style="view-transition-name: msa-box">msa module · ×4 bloques</div>

<Slashes :items="['evolución', 'covariación', 'pair Z']" />

<MsaModule class="mm-big" />

<div class="grid grid-cols-3 gap-5 mt-3">
<div class="box"><h3>outer product mean</h3><p>msa → pair. la covariación entre las columnas i y j se escribe en Z_ij: aquí entra la señal evolutiva de contacto.</p></div>
<div class="box"><h3>pair-weighted averaging</h3><p>pair → msa. Z pondera cómo se mezcla la información dentro de cada secuencia (reemplaza la row attention de AF2).</p></div>
<div class="box"><h3>salida</h3><p>la msa se descarta al terminar el módulo: sólo Z continúa hacia el pairformer.</p></div>
</div>

<p class="note mt-3">→ tesis: aquí la profundidad del msa entra a Z · profundo = h_source, superficial = h_target</p>

---
class: theme-solar tone-sun
clicks: 1
transition: view-transition
---

# Arquitectura de AF3

<Slashes :items="['trunk', 'difusión', 'heads']" />

<ArchFlow focus="pairformer" :visited="['msa']" class="mt-8" />

<p class="note mt-10">la msa ya dejó su señal en Z · ahora: cómo el pairformer refina H y Z durante 48 bloques.</p>

---
class: theme-solar tone-leaf
---

# Pairformer

<div class="vt-chip" style="view-transition-name: pf-box">pairformer · ×48 bloques</div>

<Slashes :items="['H', 'Z', 'triangle updates']" />

<div class="grid gap-10" style="grid-template-columns:1.2fr 1fr">
<div>

<div class="rows">
  <div class="r"><span class="name">single H · N × 384</span><span class="what">vector contextual por token (residuo; átomos para ligandos)</span></div>
  <div class="r"><span class="name">pair Z · N × N × 128</span><span class="what">vector por par ordenado i→j</span></div>
  <div class="r"><span class="name">coords X · A × 3</span><span class="what">una posición por átomo · A ≠ N · la genera la difusión</span></div>
</div>

<div class="tight mt-3">
<v-clicks>

- los vectores pair **no son distancias**; una distancia puede ser *decodificable*
- triangle updates: Z_ij se actualiza con las aristas hacia un tercer residuo k
- H se actualiza con atención sesgada por Z (pair bias)
- intervenir = instrumentar haiku: **capturar → modificar → reanudar**

</v-clicks>
</div>

</div>
<div>
<TriangleUpdates class="mt-2" />
</div>
</div>

---
class: theme-solar tone-teal
---

# Activation Patching

<Slashes :items="['contrast pairs', 'patch', 'localizar']" />

<div class="grid grid-cols-2 gap-5" style="margin-top:-.4rem">
<div class="box"><h3>el problema</h3><p>si borramos un componente y deja de decir «baloncesto», ¿borramos el deporte, «esto es de deportes» o «hablo español»?</p></div>
<div class="box hot"><h3>idea clave · contrast pairs</h3><p>prompts lo más parecidos posible, <b>salvo</b> la propiedad que nos importa → el patch aísla sólo esa diferencia.</p></div>
</div>

<ContrastPatching class="mt-3" />

<p class="note refs mt-2">h' = h_B + m ⊙ (h_A − h_B) · m = token del nombre, capa ℓ · variantes: ablación · rescate · steering</p>

---
class: theme-solar tone-teal
clicks: 2
---

# Diseño principal

<ContactGlyph />

<Slashes :items="['clean', 'corrupted', 'patched']" />

<div class="note" style="margin:-.9rem 0 .2rem">

$f(x) = g(h(x))$ &nbsp;·&nbsp; $h' = h_{\text{target}} + m \odot (h_{\text{source}} - h_{\text{target}})$

</div>

<PatchingRuns />

<p class="note mt-2">mismo seed en las tres corridas · fuente, máscara y magnitud <b>son parte de la hipótesis</b></p>

---
class: theme-solar tone-leaf
---

# Protocolo y controles

<Slashes :items="['de decodificable a mecanístico', 'controles']" />

<div class="steps mt-2" style="grid-template-columns:repeat(4, 1fr); gap:1.6rem">
  <div class="st"><span class="n">1</span><span class="t">probe</span><span class="d">antes de intervenir: ¿una dirección en Z_ij predice el contacto?</span><span class="lv">decodificable</span></div>
  <div class="st seen"><span class="n">2</span><span class="t">patch</span><span class="d">el diseño principal</span><span class="lv">causal</span></div>
  <div class="st"><span class="n">3</span><span class="t">vía</span><span class="d">path patching: cómo viaja la señal hasta la difusión</span><span class="lv">mecanístico</span></div>
  <div class="st"><span class="n">4</span><span class="t">generalizar</span><span class="d">familias de proteínas held-out</span><span class="lv">reproducible</span></div>
</div>

<div class="grid grid-cols-2 gap-x-12 mt-10">
<div class="rows inline-rows">
  <div class="r"><span class="name">no-change patch</span><span class="what">h' = h debe dar el mismo output bit a bit</span></div>
  <div class="r"><span class="name">edits random</span><span class="what">igual norma → descarta daño genérico</span></div>
</div>
<div class="rows inline-rows">
  <div class="r"><span class="name">pair-scaling</span><span class="what">comparar contra la perilla global</span></div>
  <div class="r"><span class="name">leakage</span><span class="what">post-cutoff ≠ sin homólogos en training</span></div>
</div>
</div>

<p class="note mt-10" style="opacity:.9">Éxito → la explicación predice cuándo funciona, cuándo falla y qué queda intacto</p>

---
class: theme-solar tone-teal
---

# Endpoints

<Slashes :items="['geometría', 'distograma', 'confianza']" />

| endpoint | métrica |
|---|---|
| contacto objetivo | $d(i,j)$ Cα/Cβ · $C_{ij} = \mathbb{1}[d(i,j) < \tau]$ · p.ej. Cβ, 8 Å |
| estructura local / global | lddt · tm-score · rmsd |
| daño off-target | Δ lddt / distancias fuera de la región objetivo |
| distograma (vs. alphainterp) | distribución y entropía en (i, j) — reportado aparte |
| confianza | plddt · pae · iptm — confianza, **no** precisión |
| ligandos | posebusters · ligand rmsd · lddt-pli |

<p class="note mt-4">Diferencias chicas sin barras de error no son resultados.</p>

---
class: theme-solar tone-teal
---

# Estado actual

<Slashes :items="['hecho', 'en espera', 'siguiente']" />

<div class="grid gap-10" style="grid-template-columns:1fr 1.6fr">
<div class="rows">
  <div class="r"><span class="name">✓ modelo</span><span class="what">AlphaFold 3</span></div>
  <div class="r"><span class="name">✓ método</span><span class="what">activation patching</span></div>
  <div class="r"><span class="name">✓ diseño</span><span class="what">marco y protocolo definidos</span></div>
  <div class="r"><span class="name">✓ AF3</span><span class="what">código y pesos disponibles</span></div>
</div>
<div>
<div class="box hot mb-4" style="padding:.6rem 1rem"><span class="note" style="opacity:1">⏳ en espera · acceso SSH a la GPU para instalar y comenzar</span></div>
<div class="rows inline-rows">
  <div class="r"><span class="name">01 · baseline</span><span class="what">instalar AF3 en el servidor y correr una predicción</span></div>
  <div class="r"><span class="name">02 · hooks</span><span class="what">capture / patch / resume → pasar el no-change test</span></div>
  <div class="r"><span class="name">03 · piloto</span><span class="what">proteínas con contactos dependientes del msa</span></div>
  <div class="r"><span class="name">04 · perfil</span><span class="what">memoria y runtime</span></div>
  <div class="r"><span class="name">05 · refinar</span><span class="what">la hipótesis</span></div>
</div>
</div>
</div>

---
layout: center
class: theme-solar tone-teal text-center
---

<GlitchBg image="closing-bg.png" :opacity="0.75" :dim="0.6" />

# <span class="glitch" data-text="gracias">Gracias</span>

<p class="big-quote mt-6" style="opacity:.85">
"AF3 usa la feature x para acercar i y j"<br/>
<span style="opacity:.5">≠</span><br/>
"así se pliega la proteína"
</p>
