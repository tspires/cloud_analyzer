<template>
  <b-card no-body>
    <b-card-body class="overflow-hidden position-relative">
      <Icon :icon="item.icon" class="fs-36 mb-1" :class="`text-${item.variant}`" />
      <h3 class="mb-0 fw-bold mt-3 mb-1">{{ item.prefix }}{{ item.statistic }}{{ item.suffix }}</h3>
      <p class="text-muted">{{ item.title }}</p>
      <b-badge v-if="item.growth" class="fs-12" :class="item.growth > 0 ? 'badge-soft-success text-success' : 'badge-soft-danger text-danger'"> 
        <i class="ti" :class="item.growth > 0 ? 'ti-arrow-badge-up' : 'ti-arrow-badge-down'" />
        {{ Math.abs(item.growth) }}% 
      </b-badge>
      <i class="widget-icon" :class="item.background?.icon"></i>
    </b-card-body>
  </b-card>
</template>

<script lang="ts" setup>
import type { PropType } from 'vue'
import type { StatisticCardType } from '@/types'
import { Icon } from '@iconify/vue'

defineProps({
  item: {
    type: Object as PropType<StatisticCardType>,
    required: true
  }
})
</script>
