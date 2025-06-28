<template>
  <b-card no-body>
    <b-card-body>
      <b-card-title tag="h5" class="anchor" :class="titleClass ?? 'mb-3'" :id="id">
        {{ title }}
        <a class="anchor-link" :href="`#${id}`">#</a>
      </b-card-title>
      <p class="text-muted" v-if="caption" v-html="caption"/>

      <slot/>
    </b-card-body>
  </b-card>
</template>

<script setup lang="ts">
type CardPropsType = {
  id?: string
  title?: string
  caption?: string
  titleClass?: string
}

defineProps<CardPropsType>()
</script>
