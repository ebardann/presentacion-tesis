<script setup lang="ts">
defineProps<{ items: string[] }>()
</script>

<template>
  <span class="slashes">
    <template v-for="(it, i) in items" :key="i">
      <span>{{ it }}</span><span v-if="i < items.length - 1" class="sep">/</span>
    </template>
  </span>
</template>

<style scoped>
.slashes { font-family: var(--font-mono); font-size: 1rem; letter-spacing: .08em; opacity: .8; display: block; margin: -.4rem 0 1.2rem; }
.sep { margin: 0 .45em; opacity: .35; }
</style>
