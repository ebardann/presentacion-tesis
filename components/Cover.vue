<script setup lang="ts">
defineProps<{ title: string; status?: string[]; sub?: string[]; author?: string }>()
</script>

<template>
  <div class="cover-wrap">
    <div class="grid-bg" />
    <div class="status-bar">
      <span class="dot-live" />
      <template v-for="(s, i) in (status ?? ['frozen', 'af3', 'online'])" :key="i">
        <span>{{ s }}</span><span v-if="i < (status ?? ['', '', '']).length - 1" class="sep">//</span>
      </template>
    </div>

    <div class="handle-big">
      <span v-for="(c, i) in title.split('')" :key="i" class="u" :style="{ animationDelay: `${i * 0.3}s` }">{{ c }}</span>
      <span class="cursor">▊</span>
    </div>

    <div class="sub">
      <Slashes v-if="sub" :items="sub" />
      <div v-if="author" class="author">{{ author }}</div>
    </div>

    <div class="glyph tl">因果</div>
    <div class="glyph tr">構造</div>
    <div class="glyph bl">折</div>
    <div class="scan" />
    <div class="vignette" />
  </div>
</template>

<style scoped>
.cover-wrap {
  position: absolute; inset: 0; overflow: hidden;
  background: radial-gradient(ellipse at 70% 30%, rgba(127,255,181,.08), transparent 55%),
              radial-gradient(ellipse at 20% 80%, rgba(255,46,195,.06), transparent 50%), #0b0f0d;
}
.grid-bg {
  position: absolute; inset: 0; z-index: 2; pointer-events: none;
  background-image: linear-gradient(rgba(127,255,181,.08) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(127,255,181,.08) 1px, transparent 1px);
  background-size: 80px 80px;
  mask-image: radial-gradient(ellipse at 50% 60%, black 10%, transparent 75%);
}
.status-bar {
  position: absolute; top: 1.5rem; left: 2.5rem; z-index: 8; display: flex; gap: .7rem; align-items: center;
  font-family: var(--font-mono); font-size: .8rem; color: var(--green-fg); letter-spacing: .15em; text-transform: uppercase; opacity: .88;
}
.status-bar .sep { opacity: .35; }
.dot-live { width: 8px; height: 8px; border-radius: 999px; background: var(--green-fg); box-shadow: 0 0 10px var(--green-fg); animation: pulse 1.4s ease-in-out infinite; }
.handle-big {
  position: absolute; top: 46%; left: 50%; transform: translate(-50%, -50%); z-index: 7;
  font-family: var(--font-mono); font-size: 6.5rem; font-weight: 300; color: var(--green-fg);
  letter-spacing: .12em; line-height: 1; display: flex; align-items: center; white-space: nowrap;
}
.handle-big .u { display: inline-block; text-shadow: 0 0 20px rgba(127,255,181,.6), 0 0 60px rgba(127,255,181,.4), 0 0 3px rgba(46,245,255,.8); animation: flicker 6s infinite; }
.handle-big .cursor { margin-left: .15em; animation: blink 1s steps(1) infinite; }
.sub { position: absolute; bottom: 3rem; left: 50%; transform: translateX(-50%); z-index: 8; text-align: center; color: var(--green-ink); white-space: nowrap; }
.sub :deep(.slashes) { font-size: 1.05rem; letter-spacing: .15em; margin: 0 0 .6rem; }
.author { font-family: var(--font-mono); font-size: .8rem; letter-spacing: .2em; opacity: .55; text-transform: lowercase; }
.glyph { position: absolute; z-index: 7; font-family: var(--font-jp), var(--font-mono); color: var(--green-fg); opacity: .5; font-size: 1.3rem; letter-spacing: .1em; }
.glyph.tl { top: 2.5rem; right: 2.5rem; }
.glyph.tr { top: 16%; left: 3rem; font-size: 2.2rem; opacity: .18; }
.glyph.bl { bottom: 3rem; left: 2.5rem; font-size: 1.1rem; opacity: .6; }
.scan { position: absolute; inset: 0; z-index: 9; pointer-events: none; mix-blend-mode: multiply;
  background: repeating-linear-gradient(0deg, rgba(0,0,0,.22) 0px, rgba(0,0,0,.22) 1px, transparent 1px, transparent 3px); }
.vignette { position: absolute; inset: 0; z-index: 6; pointer-events: none;
  background: radial-gradient(ellipse at 50% 50%, transparent 35%, rgba(11,15,13,.6) 100%), linear-gradient(180deg, #0b0f0d33, #0b0f0d73); }
@keyframes pulse { 0%, to { opacity: 1; transform: scale(1) } 50% { opacity: .4; transform: scale(.7) } }
@keyframes flicker { 0%, to { opacity: 1 } 34% { opacity: .65 } 36% { opacity: 1 } 51% { opacity: .85 } 52% { opacity: 1 } }
@keyframes blink { 0%, 49% { opacity: 1 } 50%, to { opacity: 0 } }
</style>
