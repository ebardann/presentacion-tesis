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
class: theme-solar tone-teal toc-slide
---

# Indice

<TocMap class="toc-center" />

---
class: theme-solar tone-leaf af-slide
---

# AlphaFold 3

<Slashes :items="['secuencia', 'estructura', 'all-atom']" />

<AlphaFoldIntro class="af-center" />

<p class="note">AlphaFold permite acelerar el diseño de fármacos, el estudio de enfermedades, el desarrollo de vacunas y enzimas, y la comprensión de la vida a nivel molecular.</p>

---
class: theme-solar tone-sun mi-slide
---

# Interpretabilidad

<p class="lead lead-strong">Entrenamos a los modelos para que aprendan, pero <b>no decidimos qué aprenden</b>.</p>

<BehavMech class="mi-push" />

<p class="note refs">Barez et al. · Understanding AI from the Inside · §4.1</p>

---
class: theme-solar tone-teal two-slide
---

# Dos enfoques

<Slashes :items="['desde la red',  'desde las features']" />

<TwoApproaches class="two-center" />


---
class: theme-solar tone-leaf
---

# Activation patching

<Slashes :items="['contrast pairs', 'patch', 'localizar']" />

<div style="margin-top:-.4rem">
<div class="box hot"><h3>Idea clave: contrast pairs</h3><p>Prompts lo más parecidos posible, <b>salvo</b> la propiedad que nos importa → el patch aísla solo esa diferencia.</p></div>
</div>

<ContrastPatching class="mt-3" />

<p class="note refs mt-2">h' = h_B + m ⊙ (h_A − h_B) · m = token del nombre, capa ℓ · variantes: ablación · rescate · steering</p>

---
class: theme-solar tone-leaf
---

# Tesis

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
class: theme-solar tone-teal mot-slide
transition: view-transition
---

# Motivación

<Motivaciones class="mot-center" />

<!--
01 Interpretabilidad: entrenamos a los modelos para que aprendan pero no decidimos qué aprenden; la brecha
entre lo que hacen y lo que entendemos crece con la escala (Barez et al.). La MI busca el cómo: afirmaciones causales.
02 AlphaFold 3: predicción all-atom de complejos (proteínas, ácidos nucleicos, ligandos, modificaciones).
Base para diseño de fármacos y enzimas; Nobel de Química 2024 (Hassabis, Jumper; con Baker). Si se usa para decidir,
importa saber en qué evidencia interna se apoya cada predicción.
03 La brecha: AlphaInterp (Feldman & Skolnick 2026) edita el pair final y cambia la entropía del distograma, no las
coordenadas de difusión. Pair scaling (Suzuki & Amagasa 2026) es una perilla global que edita todas las features a la vez.
SAEs en proteínas (PairSAE, InterPLM) descubren features pero casi no intervienen. Esa es la oportunidad (assessment p.5).
-->

---
class: theme-solar tone-sun gap-slide
transition: view-transition
---

# La brecha de interpretabilidad

<MotTrack :active="1" />

<InterpGap class="gap-center" />

<p class="note refs">Barez et al. · Understanding AI from the Inside · §1</p>

<!--
Interpretability gap: la disparidad entre lo que los modelos hacen (capacidades y comportamientos)
y lo que entendemos de cómo lo hacen (sus mecanismos internos). Al escalar, la brecha tiende a crecer:
razonamiento que no podemos rastrear, comportamientos engañosos sin detectar, garantías de seguridad
construidas sobre una comprensión incompleta.
-->

---
class: theme-solar tone-leaf imp-slide
transition: view-transition
---

# Si entendiéramos AlphaFold

<MotTrack :active="2" />

<AfImplications class="imp-center" />

<p class="note imp-key">el mecanismo describe <b>al predictor</b>, no al plegamiento real · las hipótesis biológicas se verifican aparte</p>

<!--
Qué cambiaría si entendiéramos el cómputo de AF3 por completo:
Precisión: si sabemos por qué falla una predicción (poca evidencia en el MSA, template engañoso, una vía interna que
no se activa) podemos corregir la causa en el input o en el modelo, en vez de sólo muestrear más. Ojo: pLDDT/PAE son
confianza, no precisión.
Control: intervenir a propósito — cambiar un contacto, recuperar un estado alternativo — en vez de perillas globales
(pair scaling) o más samples.
Diseño de fármacos: AF3 predice complejos proteína–ligando; entender qué evidencia interna sostiene una pose
(y cuándo es una alucinación con confianza alta) permitiría priorizar mejores candidatos antes de sintetizarlos.
Descubrimiento: si el modelo aprendió reglas geométricas útiles, extraerlas como hipótesis — que hay que verificar
experimentalmente: un mecanismo del predictor no es la física del plegamiento.
-->

---
class: theme-solar tone-coral pw-slide
---

# Trabajo previo

<MotTrack :active="3" />

<PriorWork class="pw-center" />

<p class="note pw-key">Nadie conecta una feature <b>localizada</b> con las <b>coordenadas 3D</b> finales.</p>

<!--
InterPLM · Adams et al. · ESM-2: features interpretables en PLMs; sobre el lenguaje, no el plegador.
PairSAE · Migliorini et al. 2026 · Boltz-2: SAE sobre pair comprimido, features alineadas con anotaciones; sin intervenciones, sin MSAs.
SAEFold · Parsan et al. 2025 · ESMFold: edit SAE aumenta accesibilidad al solvente; ¿estado válido o daño / desorden? (por eso coords = parcial).
AlphaInterp · Feldman & Skolnick 2026 · AF3: probes en H y Z; edits PCA del pair final cambian la entropía del distograma, no las coordenadas de difusión.
Pair scaling · Suzuki & Amagasa 2026 · AF3 + Boltz-2: escalar Z amplía el sampling y recupera estados alternativos (86 proteínas); perilla global, edita todas las features a la vez.
El descubrimiento de features está más maduro que la explicación a nivel circuito. Contribución: explicar un efecto selectivo y su transmisión, con held-out y controles.
-->

---
class: theme-solar tone-sun jump-slide
---

# De LLMs a proteínas

<LlmToProtein class="jump-center" />

<!--
El Pairformer es "un transformer con dos streams": H (N×384, por residuo) y Z (N×N×128, por par).
Equivalencias: self-attention ↔ attention con pair bias sobre H (Z sesga los pesos); MLP ↔ transition
(H y Z); flujo residual ↔ H y Z, que cada bloque lee y actualiza. × N capas ↔ × 48 bloques.
Lo nuevo: triangle multiplicative updates (outgoing/incoming) y triangle attention (starting/ending node)
sobre Z — actualizan i–j combinando i–k y k–j. No tienen análogo en un LLM.
Por eso las herramientas de MI (probes, patching, SAEs, circuitos) se transfieren: ESM-2 (InterPLM),
ESMFold (SAEFold), Boltz-2 (PairSAE), AF3 (AlphaInterp). Diferencia clave: la salida no es una palabra
sino geometría 3D (vía difusión).
-->

---
class: theme-solar tone-teal rc-slide
---

# Flujo residual

<ResidualCompare class="rc-center" />

<!--
El flujo residual es el "bus" de la red: cada bloque lee de él y le suma (⊕) su salida; nada se reemplaza.
LLM: un solo flujo x (L×d); attention mezcla entre tokens, el MLP transforma cada token. × N capas.
AF3 · Pairformer: dos flujos. Z (N×N×128, por par) recibe triangle multiplicative updates, triangle attention y
transition; H (N×384, por residuo) recibe attention con pair bias —Z sesga los pesos— y transition. × 48 bloques.
Al final H y Z condicionan la difusión, que genera las coordenadas.
Activation patching = capturar el flujo en un punto (aquí: Z en el bloque ℓ / recycle, pares i,j), reemplazarlo
por h' y dejar que todo lo que sigue corra igual, con seeds fijos.
-->

---
class: theme-solar tone-teal dp-slide
---

# Diseño principal

<ContactGlyph />

<div class="note" style="margin:.6rem 0 0">

$f(x) = g(h(x))$ &nbsp;·&nbsp; $h' = h_{\text{target}} + m \odot (h_{\text{source}} - h_{\text{target}})$

</div>

<PatchingRuns class="dp-center" />

---
class: theme-solar tone-leaf pc-slide
---

# Protocolo y controles

<SuccessCriteria class="pc-center" />

<!--
Criterio de éxito (assessment p.16): la explicación predice cuándo funciona la intervención, cuándo falla y qué
otras salidas quedan intactas. El protocolo y los controles se organizan alrededor de eso:
1 · cuándo funciona: probe (decodificable) → patch y rescate (causal) → path patching hasta la difusión (mecanístico).
2 · cuándo falla: generalizar a familias held-out prediciendo de antemano aciertos y fallos; contactos que no
    dependen del MSA son controles negativos naturales; ojo con leakage (post-cutoff no excluye homólogos).
3 · qué queda intacto: no-change patch bit a bit; edits random de igual norma (descarta daño genérico);
    comparar contra pair-scaling global a magnitud y presupuesto de samples equivalentes; lDDT fuera de (i, j).
-->

---
class: theme-solar tone-sun
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
