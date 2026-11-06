---
theme: default
colorSchema: dark
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
class: theme-lain
---

<Cover
  title="AlphaFold3"
  :status="['Interpretabilidad', 'JAX', 'Patching']"
  :sub="['mecanismos causales', 'activation patching', 'geometría 3D']"
  author="Emilio Bardan · tsesis · 2026"
/>

<!--
Basado en el field assessment del 14 oct 2026 (assessment.pdf).
-->

---
class: theme-frieren layer-solarpunk
---


# la tesis en una frase

<Slashes :items="['af3 congelado', 'una feature', 'coordenadas finales']" />

<p class="big-quote">
usar <b>activation patching</b> sobre un <b>alphafold 3 congelado</b> para conectar
<b>una feature o vía interna</b> con un <b>cambio selectivo y reproducible</b>
en las coordenadas 3d generadas por difusión.
</p>

<div class="kv mt-8">
  <div><span class="k">selectivo</span> cambia la propiedad objetivo · el resto de la estructura se preserva</div>
  <div><span class="k">reproducible</span> se sostiene entre seeds, controles pareados y proteínas held-out</div>
</div>

<!--
El assessment lo identifica como la oportunidad abierta más fuerte en MI de predictores de estructura (p.5).
-->

---
class: theme-lain layer-cyberpunk
---

# decisiones

<Slashes :items="['modelo', 'método', 'endpoint', 'claim']" />

<div class="rows mt-4">
  <div class="r"><span class="name">modelo</span><span class="what">alphafold 3 · jax/haiku · pesos congelados</span></div>
  <div class="r"><span class="name">método</span><span class="what">activation patching + ablación / rescate</span></div>
  <div class="r"><span class="name">endpoint</span><span class="what">coordenadas finales del módulo de difusión — no una lectura intermedia</span></div>
  <div class="r"><span class="name">claim</span><span class="what">causal sobre el output → idealmente mecanístico (circuito / vía)</span></div>
  <div class="r"><span class="name">entrenamiento</span><span class="what">ninguno · sólo forward passes</span></div>
</div>

---
class: theme-eva layer-cyberpunk
---

# el gap

<Slashes :items="['trabajo previo', 'qué falta']" />

| trabajo | qué mostró | qué **no** mostró |
|---|---|---|
| **alphainterp** · feldman & skolnick 2026 · af3 | probes en single/pair en 4 ubicaciones; edits pca del pair final cambian la entropía del distograma | efecto en el **distogram head**, no en coordenadas de difusión |
| **pair scaling** · suzuki & amagasa 2026 · af3 + boltz-2 | escalar el pair rep amplía el sampling y recupera estados alternativos (86 proteínas) | perilla **global** — edita todas las features a la vez |
| **pairsae** · migliorini et al. 2026 · boltz-2 | sae sobre pair comprimido; features alineadas con anotaciones | sin intervenciones · sin msas |
| **saefold** · parsan et al. 2025 · esmfold | edit sae aumenta accesibilidad al solvente | ¿estado válido o daño / desorden? |
| interplm · adams et al. · esm-2 | features interpretables en plms | sobre el lenguaje, no el plegador |

<p class="note mt-4">→ el descubrimiento de features está más maduro que la explicación a nivel circuito.
la contribución: explicar un efecto selectivo <b>y su transmisión</b>, con held-out y controles.</p>

---
class: theme-lain layer-vaporwave
---

# pipeline af3

<Slashes :items="['trunk', 'difusión', 'heads']" />

```mermaid {scale: 0.85}
flowchart LR
  A[inputs<br/>seq · msa · templates · ligandos] --> B[embedder]
  B --> C[msa module]
  C --> D[pairformer ×48<br/>single H · pair Z<br/>+ recycling]
  D --> E[diffusion module<br/>denoising iterativo]
  E --> F[coordenadas X]
  D --> G[distogram head]
  E --> H[confidence<br/>plddt · pae · iptm]
  style D fill:#1b2a10,stroke:#f7b500,color:#f6e9e3
  style E fill:#0b1d22,stroke:#2ef5ff,color:#e8fff3
  style F fill:#0f2a1c,stroke:#7fffb5,color:#7fffb5
```

<p class="note mt-6">recycling y pasos de difusión = cómputo del modelo, no tiempo físico de plegamiento.
recycles / pasos / samples por seed se leen del config instalado — no se asumen.</p>

---
class: theme-frieren layer-solarpunk
---

# representaciones

<Slashes :items="['H', 'Z', 'X']" />

<div class="grid gap-10" style="grid-template-columns:1.3fr 1fr">
<div>

<div class="rows">
  <div class="r"><span class="name">single H · N × 384</span><span class="what">vector contextual por token (residuo; átomos para ligandos)</span></div>
  <div class="r"><span class="name">pair Z · N × N × 128</span><span class="what">vector por par ordenado i→j</span></div>
  <div class="r"><span class="name">coords X · A × 3</span><span class="what">una posición por átomo · A ≠ N</span></div>
</div>

<v-clicks>

- los vectores pair **no son distancias**; una distancia puede ser *decodificable*
- triangle updates combinan i–k y k–j para actualizar i–j
- intervenir = instrumentar haiku: **capturar → modificar → reanudar**

</v-clicks>

</div>
<pre class="ascii pt-4">
      j →
    ┌─────────────┐
  i │ · · · · · · │
  ↓ │ · · · · · · │
    │ · · ■ · · · │ ← Z_ij ∈ ℝ¹²⁸
    │ · · · · · · │
    │ · · · · · · │
    └─────────────┘
     N × N × 128
</pre>
</div>

---
class: theme-lain layer-cyberpunk
---



# activation patching

<Slashes :items="['capturar', 'modificar', 'reanudar']" />

ver la red como $f(x) = g(h(x))$ · $h$ = activación intermedia · $g$ = resto (incl. difusión)

$$
h' = h_{\text{target}} + m \odot (h_{\text{source}} - h_{\text{target}})
$$

<div class="grid grid-cols-2 gap-8 mt-2">
<div class="kv">
  <div><span class="k">m · tokens</span> pares (i, j)</div>
  <div><span class="k">m · canales</span> dirección de feature</div>
  <div><span class="k">m · capa</span> bloque pairformer</div>
  <div><span class="k">m · recycle</span> iteración</div>
</div>
<div class="kv">
  <div><span class="k">ablación</span> cero · media · proyectar fuera</div>
  <div><span class="k">rescate</span> restaurar tras ablar</div>
  <div><span class="k">steering</span> sumar α · dirección</div>
</div>
</div>

<p class="note mt-5">h_source = corrida pareada (misma secuencia, otro msa). fuente, máscara y magnitud <b>son parte de la hipótesis</b>.</p>

---
class: theme-vinland layer-solarpunk
---

# features y evidencia

<Slashes :items="['decodificable', 'causal', 'mecanístico']" />

<div class="grid grid-cols-2 gap-10">
<div>

### candidatos · barato → rico

<div class="chips mt-3">
  <span class="chip">canales</span>
  <span class="chip">pca</span>
  <span class="chip">linear probe · Z_ij</span>
  <span class="chip">sae</span>
</div>

<p class="note mt-5">comparar sae siempre contra baselines neurona / pca / probe.
superposición: un canal ≠ un concepto.</p>

</div>
<div>

### niveles

<div class="rows">
  <div class="r"><span class="name">1 · decodificable</span><span class="what">un probe lee la propiedad de h — no causal</span></div>
  <div class="r"><span class="name">2 · causal</span><span class="what">intervenir h cambia el output como se predijo</span></div>
  <div class="r"><span class="name">3 · mecanístico</span><span class="what">explica cómo se transforma y transmite la información</span></div>
</div>

</div>
</div>

<p class="note mt-6">un mecanismo describe <b>al predictor</b>, no la dinámica real del plegamiento.</p>

---
class: theme-eva layer-cyberpunk
---

<div class="corner-glyph">仮説</div>

# diseño principal

<Slashes :items="['msa', 'contacto', 'coordenadas']" />

<div class="kv mb-4">
  <div><span class="k">pregunta</span> ¿cómo se vuelve la evidencia evolutiva una restricción de contacto?</div>
  <div><span class="k">hipótesis</span> una feature localizada en Z_ij media el efecto del msa sobre (i, j) y llega hasta las coordenadas</div>
</div>

```mermaid {scale: 0.75}
flowchart LR
  D[msa profundo<br/>contacto presente] -->|h_source · Z_ij| P((patch))
  S[msa superficial<br/>contacto perdido] -->|h_target| P
  P --> R[reanudar pairformer<br/>+ difusión · seeds fijas]
  R --> M[¿vuelve d i,j en<br/>coordenadas finales?]
  style P fill:#2a0a08,stroke:#ff3a2f,color:#ff3a2f
  style M fill:#1f1800,stroke:#f7b500,color:#f7b500
```

<p class="note mt-4">riesgo principal: la información está <b>distribuida</b> — no existe una feature pequeña y localizada.</p>

---
class: theme-lain layer-vaporwave
---

# protocolo

<Slashes :items="['7 pasos']" />

<div class="grid grid-cols-2 gap-x-10">
<div class="rows">
  <div class="r" v-click><span class="name">01 · targets</span><span class="what">proteínas chicas/medianas, post-cutoff · contacto de largo alcance presente con msa profundo, perdido con msa submuestreado</span></div>
  <div class="r" v-click><span class="name">02 · probe</span><span class="what">¿una dirección en Z_ij predice el contacto entre ejemplos? (nivel 1)</span></div>
  <div class="r" v-click><span class="name">03 · patch</span><span class="what">copiar la feature (i, j) ± vecindad profundo → superficial, o ablarla · barrer capa y recycle</span></div>
  <div class="r" v-click><span class="name">04 · medir</span><span class="what">distancia en coordenadas finales · daño off-target · confianza aparte</span></div>
</div>
<div class="rows">
  <div class="r" v-click><span class="name">05 · rescate</span><span class="what">restaurar la feature y confirmar que la geometría vuelve</span></div>
  <div class="r" v-click><span class="name">06 · vía</span><span class="what">path patching entre capas · triangle updates vs. atención · hasta el condicionamiento de difusión</span></div>
  <div class="r" v-click><span class="name">07 · generalizar</span><span class="what">familias held-out · opcional: otro predictor all-atom</span></div>
</div>
</div>

---
class: theme-elden layer-solarpunk
---

# controles

<Slashes :items="['no negociables']" />

<div class="grid grid-cols-2 gap-x-10">
<div class="rows">
  <div class="r"><span class="name">no-change patch</span><span class="what">h' = h reproduce el baseline bit a bit antes de interpretar nada</span></div>
  <div class="r"><span class="name">edits aleatorios</span><span class="what">dirección / máscara random de igual norma → descarta daño genérico</span></div>
  <div class="r"><span class="name">rescate</span><span class="what">reversibilidad del efecto</span></div>
  <div class="r"><span class="name">pair-scaling global</span><span class="what">baseline a magnitud y budget de samples equivalentes</span></div>
</div>
<div class="rows">
  <div class="r"><span class="name">seeds y sampling</span><span class="what">fijar inputs, seeds, nº samples · top-1 vs. best-of-n</span></div>
  <div class="r"><span class="name">off-target</span><span class="what">regiones no relacionadas intactas · confianza ≠ geometría</span></div>
  <div class="r"><span class="name">sae recon-only</span><span class="what">insertar sólo la reconstrucción ya puede cambiar outputs</span></div>
  <div class="r"><span class="name">leakage</span><span class="what">fecha posterior ≠ sin homólogos en training</span></div>
</div>
</div>

<div class="box hot mt-6 text-center">
<span class="note" style="opacity:1">éxito → la explicación predice cuándo funciona, cuándo falla y qué outputs quedan intactos</span>
</div>

---
class: theme-frieren layer-cyberpunk
---

# endpoints

<Slashes :items="['geometría', 'distograma', 'confianza']" />

| endpoint | métrica |
|---|---|
| contacto objetivo | $d(i,j)$ Cα/Cβ · $C_{ij} = \mathbb{1}[d(i,j) < \tau]$ · p.ej. Cβ, 8 Å |
| estructura local / global | lddt · tm-score · rmsd |
| daño off-target | Δ lddt / distancias fuera de la región objetivo |
| distograma (vs. alphainterp) | distribución y entropía en (i, j) — reportado aparte |
| confianza | plddt · pae · iptm — confianza, **no** precisión |
| ligandos | posebusters · ligand rmsd · lddt-pli |

<p class="note mt-4">diferencias chicas sin barras de error no son resultados.</p>

---
class: theme-lain layer-cyberpunk
---

# cómputo

<Slashes :items="['gpu', 'storage', 'runtime']" />

<div class="grid grid-cols-2 gap-10">
<div class="kv">
  <div><span class="k">gpu</span> 1× a100/h100 80 gb</div>
  <div><span class="k">host</span> 128 gb ram · 16–32 cores</div>
  <div><span class="k">scratch</span> 1–2 tb ssd</div>
  <div><span class="k">bases af3</span> ~1 tb → msas cacheados</div>
  <div><span class="k">runtime</span> ~62 s · 1.024 tokens</div>
  <div><span class="k">piloto</span> 50 × 10 × 3 ≈ 26 gpu-h</div>
</div>
<div>
<pre class="ascii">
pair tensor  N=512 · 128ch · fp16
  ├─ 1 tensor        64 MiB
  ├─ × 48 capas       3 GiB / recycle
  └─ × 10 recycles   30 GiB / proteína
                     ∝ N²
</pre>
<p class="note mt-4">capturar sólo ubicaciones seleccionadas · muestrear pares · streamear.
reutilizar cómputo upstream al parchear tarde.</p>
</div>
</div>

---
class: theme-vinland layer-solarpunk
---

# estado

<Slashes :items="['hecho', 'siguiente']" />

<div class="grid gap-10" style="grid-template-columns:1fr 1.6fr">
<div class="rows">
  <div class="r"><span class="name">✓ modelo</span><span class="what">alphafold 3</span></div>
  <div class="r"><span class="name">✓ método</span><span class="what">activation patching</span></div>
  <div class="r"><span class="name">✓ diseño</span><span class="what">marco y protocolo definidos</span></div>
</div>
<div class="rows">
  <div class="r"><span class="name">01 · pesos</span><span class="what">obtener af3 + revisar términos no comerciales</span></div>
  <div class="r"><span class="name">02 · baseline</span><span class="what">instalar af3 y correr una predicción</span></div>
  <div class="r"><span class="name">03 · hooks</span><span class="what">capture / patch / resume → pasar el no-change test</span></div>
  <div class="r"><span class="name">04 · piloto</span><span class="what">proteínas con contactos dependientes del msa</span></div>
  <div class="r"><span class="name">05 · perfil</span><span class="what">memoria y runtime</span></div>
  <div class="r"><span class="name">06 · refinar</span><span class="what">la hipótesis</span></div>
</div>
</div>

---
layout: center
class: theme-elden layer-vaporwave text-center
---

# gracias

<p class="big-quote mt-6" style="opacity:.85">
"af3 usa la feature x para acercar i y j"<br/>
<span style="opacity:.5">≠</span><br/>
"así se pliega la proteína"
</p>
