<script setup lang="ts">
import { useNav } from '@slidev/client'
const { currentPage, total } = useNav()
</script>

<template>
  <footer
    class="absolute text-xs opacity-60 pointer-events-none select-none"
    style="bottom: 8px; right: 18px; color: #666;"
  >
    {{ currentPage }} / {{ total }}
  </footer>
</template>
