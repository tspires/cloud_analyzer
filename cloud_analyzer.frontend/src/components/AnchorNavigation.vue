<template>
  <b-card no-body class="docs-nav">
    <ul class="nav bg-transparent flex-column">
      <li v-for="(item, idx) in elements" :key="item.id" class="nav-item" :class="{ active: currentElementId === item.id }">
        <a :href="`#${item.id}`" class="nav-link">{{ item.title }}</a>
      </li>
    </ul>
  </b-card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { PropType } from 'vue'

type ElementType = {
  id: string
  title: string
}

const props = defineProps({
  elements: {
    type: Object as PropType<ElementType[]>
  }
})

function isInViewport(el: HTMLElement) {
  const rect = el.getBoundingClientRect()
  return rect.top >= 0 && rect.bottom <= window.innerHeight - 700
}

let currentElementId = ref(null)

onMounted(() => {
  let elements: any = []

  if (props.elements) {
    props.elements.forEach((i) => elements.push(document.getElementById(i.id)))
  }

  window.addEventListener('scroll', () => {
    elements.forEach((element: any) => {
      if (isInViewport(element)) {
        currentElementId.value = element.id
      }
    })
  })
})
</script>
