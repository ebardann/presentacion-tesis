# Presentación de tesis — Mecanismos causales dentro de AlphaFold 3

Presentación en [Slidev](https://sli.dev/) de la propuesta de tesis: usar **activation patching** sobre un
**AlphaFold 3 congelado** para conectar una feature interna con un cambio selectivo y reproducible en las
coordenadas 3D finales. El contenido sale de [`../CLAUDE.md`](../CLAUDE.md) (basado en `assessment.pdf`).

## Uso

```bash
npm install
npm run dev        # abre http://localhost:3030
```

| Ruta | Qué es |
|---|---|
| `http://localhost:3030/` | presentación |
| `http://localhost:3030/presenter/` | modo presentador (notas + siguiente slide) |
| `http://localhost:3030/overview/` | vista general de todas las slides |

Otros comandos:

```bash
npm run build      # sitio estático en dist/ (deployable en Netlify/Vercel, ya configurados)
npm run export     # PDF — requiere: npm i -D playwright-chromium
```

## Contenido (15 slides)

1. portada
2. la tesis en una frase
3. decisiones (modelo, método, endpoint, claim)
4. el gap — trabajo previo y qué no mostró
5. pipeline de AF3 (diagrama mermaid)
6. representaciones `H`, `Z`, `X`
7. activation patching — fórmula, máscara y variantes
8. candidatos a feature y niveles de evidencia
9. diseño principal — hipótesis MSA → contacto → coordenadas
10. protocolo en 7 pasos
11. controles no negociables
12. endpoints y métricas
13. cómputo y almacenamiento
14. estado actual y próximos pasos
15. cierre

## Estilo

Inspirado en [uumami.wiki/presentacion_clase_esponda](https://uumami.wiki/presentacion_clase_esponda/#/1):
fondo oscuro, títulos en minúscula (Inter ligera), etiquetas en IBM Plex Mono, Cinzel como display.

- **Temas por slide** — se eligen con `class:` en el frontmatter de cada slide:
  `theme-green` (verde) · `theme-red` (rojo/ámbar) · `theme-navy` (dorado, Cinzel) ·
  `theme-sand` (tierra) · `theme-bronze` (dorado, mayúsculas).
- **Capas atmosféricas** — se combinan con el tema: `layer-cool` · `layer-pink` · `layer-warm`.
  Ejemplo: `class: theme-red layer-cool`.
- **Clases de contenido** (en `styles/index.css`):
  `kv` (clave · valor), `rows` / `.r` / `.name` / `.what` (filas punteadas), `chips` / `chip`,
  `box` / `box hot`, `note`, `ascii` (usar con `<pre>`), `big-quote`.

## Estructura

| Archivo | Función |
|---|---|
| `slides.md` | las slides |
| `styles/index.css` | fuentes, paleta, temas, capas y clases de contenido |
| `components/Cover.vue` | portada tipo terminal CRT (título con glow, barra de estado, imagen de fondo `assets/cover-bg.png`) |
| `components/Slashes.vue` | subtítulo `a / b / c` — `<Slashes :items="['a','b']" />` |
| `components/Ticker.vue` | barra con texto desplazándose; toma el color del tema de la slide actual |
| `global-top.vue` / `global-bottom.vue` | barras superior e inferior (se ocultan en la portada). Editar aquí las frases y la velocidad (`:speed`, segundos por vuelta) |
| `assets/cover-bg.png` | fondo de la portada (proteína en cintas, estilo neón/glitch) |
| `assets/fold-bg.png` | fondo alternativo, sin uso: cadena desplegada → ubiquitina plegada (PDB 1UBQ, dominio público). Se regenera con `curl -sLO https://files.rcsb.org/download/1UBQ.pdb && python3 scripts/render_fold.py 1UBQ.pdb assets/fold-bg.png` |
| `setup/mermaid.ts` | colores oscuros para los diagramas mermaid |

Quedan del template de Slidev y no se usan: `components/Counter.vue`, `pages/imported-slides.md`,
`snippets/external.ts`.
