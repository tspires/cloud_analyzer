<template>
  <component :is="is ?? 'div'" :id="id"></component>
</template>

<script setup lang="ts">
import { Grid } from 'gridjs'
import { onMounted } from 'vue'

type GridJsTablePropsType = {
  is?: string
  id: string
  options: object
}

const props = defineProps<GridJsTablePropsType>()

onMounted(() => {
  const ele = document.getElementById(props.id)

  if (ele) new Grid(props.options).render(ele)
})
</script>
