<script setup lang="ts">
import { computed } from 'vue'
import { useNav } from '@slidev/client'

const props = withDefaults(defineProps<{
  items: string[]
  position: 'top' | 'bottom'
  speed?: number // segundos por vuelta
  reverse?: boolean
}>(), { speed: 60, reverse: false })

const { currentPage, total, currentSlideRoute } = useNav()

// color según el tema (class) de la slide actual
const palette: Record<string, string> = {
  'theme-green': '#7fffb5',
  'theme-red': '#f7b500',
  'theme-navy': '#d4af6b',
  'theme-sand': '#d7c7a3',
  'theme-bronze': '#c9a159',
}
const color = computed(() => {
  const cls = String(currentSlideRoute.value?.meta?.slide?.frontmatter?.class ?? '')
  const key = Object.keys(palette).find(k => cls.includes(k))
  return key ? palette[key] : palette['theme-green']
})
const hidden = computed(() => currentPage.value === 1)
const pad = (n: number) => String(n).padStart(2, '0')
</script>

<template>
  <div v-if="!hidden" class="ticker" :class="position" :style="{ '--c': color }">
    <div class="tag">
      <span class="dot" />
      <span v-if="position === 'top'">live</span>
      <span v-else>{{ pad(currentPage) }} / {{ pad(total) }}</span>
    </div>
    <div class="track-wrap">
      <div class="track" :style="{ animationDuration: `${props.speed}s`, animationDirection: props.reverse ? 'reverse' : 'normal' }">
        <template v-for="copy in 2" :key="copy">
          <span v-for="(it, i) in items" :key="`${copy}-${i}`" class="item">
            {{ it }}<span class="sep">//</span>
          </span>
        </template>
      </div>
    </div>
  </div>
</template>

<style scoped>
.ticker {
  position: absolute; left: 0; right: 0; height: 1.6rem; z-index: 50;
  display: flex; align-items: center; overflow: hidden;
  font-family: var(--font-mono); font-size: .68rem; letter-spacing: .16em; text-transform: uppercase;
  color: var(--c); background: rgba(5, 8, 7, .72); backdrop-filter: blur(4px);
  transition: color .4s ease;
  pointer-events: none;
}
.ticker.top { top: 0; border-bottom: 1px solid color-mix(in srgb, var(--c) 28%, transparent); }
.ticker.bottom { bottom: 0; border-top: 1px solid color-mix(in srgb, var(--c) 28%, transparent); }
.tag {
  flex: 0 0 auto; display: flex; align-items: center; gap: .5rem; padding: 0 .9rem; height: 100%;
  border-right: 1px solid color-mix(in srgb, var(--c) 28%, transparent);
  background: color-mix(in srgb, var(--c) 10%, transparent); z-index: 1;
}
.dot { width: 6px; height: 6px; border-radius: 999px; background: var(--c); box-shadow: 0 0 8px var(--c); animation: pulse 1.4s ease-in-out infinite; }
.track-wrap {
  flex: 1; overflow: hidden; height: 100%; display: flex; align-items: center;
  mask-image: linear-gradient(90deg, transparent, black 4%, black 96%, transparent);
}
.track { display: inline-flex; white-space: nowrap; animation: scroll linear infinite; opacity: .85; }
.item { padding-right: 0; }
.sep { margin: 0 1.1em; opacity: .35; }
@keyframes scroll { from { transform: translateX(0) } to { transform: translateX(-50%) } }
@keyframes pulse { 0%, to { opacity: 1; transform: scale(1) } 50% { opacity: .4; transform: scale(.7) } }
</style>
