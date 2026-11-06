<script setup lang="ts">
defineProps<{ title: string; status?: string[]; sub?: string[]; author?: string }>()
</script>

<template>
  <div class="cover-wrap">
    <GlitchBg image="cover-bg.png" :opacity="0.7" :dim="0" />
    <div class="grid-bg" />
    <div class="status-bar">
      <span class="dot-live" />
      <template v-for="(s, i) in (status ?? ['frozen', 'af3', 'online'])" :key="i">
        <span>{{ s }}</span><span v-if="i < (status ?? ['', '', '']).length - 1" class="sep">//</span>
      </template>
    </div>

    <div class="handle-big glitch" :data-text="title">
      <span v-for="(c, i) in title.split('')" :key="i" class="u" :style="{ animationDelay: `${i * 0.3}s` }">{{ c }}</span>
      <span class="cursor">▊</span>
    </div>

    <div class="sub">
      <Slashes v-if="sub" :items="sub" />
      <div v-if="author" class="author">{{ author }}</div>
    </div>

    <div class="scan" />
    <div class="vignette" />
  </div>
</template>

<style scoped>
.cover-wrap {
  position: absolute; inset: 0; overflow: hidden;
  background: radial-gradient(ellipse at 70% 30%, rgba(255,194,75,.08), transparent 55%),
              radial-gradient(ellipse at 20% 80%, rgba(63,217,199,.07), transparent 50%), #08130f;
}
.cover-wrap :deep(.glitch-bg) { z-index: 1 !important; }
.cover-wrap :deep(.glitch-bg .shade), .cover-wrap :deep(.glitch-bg .scan) { display: none; }
.grid-bg {
  position: absolute; inset: 0; z-index: 2; pointer-events: none;
  background-image: linear-gradient(rgba(143,227,106,.07) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(143,227,106,.07) 1px, transparent 1px);
  background-size: 80px 80px;
  mask-image: radial-gradient(ellipse at 50% 60%, black 10%, transparent 75%);
}
.status-bar {
  position: absolute; top: 1.5rem; left: 2.5rem; z-index: 8; display: flex; gap: .7rem; align-items: center;
  font-family: var(--font-mono); font-size: .8rem; color: var(--teal); letter-spacing: .15em; text-transform: uppercase; opacity: .88;
}
.status-bar .sep { opacity: .35; }
.dot-live { width: 8px; height: 8px; border-radius: 999px; background: var(--teal); box-shadow: 0 0 10px var(--teal); animation: pulse 1.4s ease-in-out infinite; }
.handle-big {
  position: absolute; top: 46%; left: 50%; transform: translate(-50%, -50%); z-index: 7;
  font-family: var(--font-mono); font-size: 6.5rem; font-weight: 300; color: var(--sun);
  letter-spacing: .12em; line-height: 1; display: flex; align-items: center; white-space: nowrap;
}
.handle-big .u { display: inline-block; text-shadow: 0 0 20px rgba(255,194,75,.6), 0 0 60px rgba(255,194,75,.35), 0 0 3px rgba(143,227,106,.8); animation: flicker 6s infinite; }
.handle-big.glitch::before, .handle-big.glitch::after { letter-spacing: .12em; white-space: nowrap; }
.handle-big .cursor { margin-left: .15em; animation: blink 1s steps(1) infinite; }
.sub { position: absolute; bottom: 3rem; left: 50%; transform: translateX(-50%); z-index: 8; text-align: center; color: var(--ink); white-space: nowrap; }
.sub :deep(.slashes) { font-size: 1.05rem; letter-spacing: .15em; margin: 0 0 .6rem; }
.author { font-family: var(--font-mono); font-size: .8rem; letter-spacing: .2em; opacity: .55; text-transform: lowercase; }
.scan { position: absolute; inset: 0; z-index: 9; pointer-events: none; mix-blend-mode: multiply;
  background: repeating-linear-gradient(0deg, rgba(0,0,0,.22) 0px, rgba(0,0,0,.22) 1px, transparent 1px, transparent 3px); }
.vignette { position: absolute; inset: 0; z-index: 6; pointer-events: none;
  background: radial-gradient(ellipse at 50% 50%, transparent 35%, rgba(8,19,15,.6) 100%), linear-gradient(180deg, #08130f33, #08130f73); }
@keyframes pulse { 0%, to { opacity: 1; transform: scale(1) } 50% { opacity: .4; transform: scale(.7) } }
@keyframes flicker { 0%, to { opacity: 1 } 34% { opacity: .65 } 36% { opacity: 1 } 51% { opacity: .85 } 52% { opacity: 1 } }
@keyframes blink { 0%, 49% { opacity: 1 } 50%, to { opacity: 0 } }
</style>
