<template>
  <b-card no-body class="card-pricing">
    <b-card-body>
      <div class="pricing-ribbon pricing-ribbon-primary float-end" v-if="item.ribbon">
        {{ item.ribbon }}
      </div>
      <h5 class="mt-0 mb-3 fs-14 text-uppercase fw-semibold">
        {{ item.name }}
      </h5>
      <h2 class="mt-0 mb-3 fw-bold">
        {{ currency }}{{ item.price }}
        <span class="fs-14 fw-medium text-muted">/ {{ item.period }}</span>
      </h2>

      <ul class="card-pricing-features text-muted border-top pt-2 mt-2 ps-0 list-unstyled">
        <li class="text-dark" v-for="(feat, idx) in item.features" :key="idx"><i class="bx bx-check-circle text-primary fs-15 me-1"></i>{{ feat }}</li>
      </ul>

      <div class="mt-4 text-center">
        <b-button variant="primary" class="px-sm-4 w-100" :disabled="item.button.disabled">
          {{ item.button.text }}
        </b-button>
      </div>
    </b-card-body>
  </b-card>
</template>
<script setup lang="ts">
import type { PropType } from 'vue'
import type { PlanType } from '@/views/pages/components/types'
import { currency } from '@/helpers/constants'

defineProps({
  item: {
    type: Object as PropType<PlanType>,
    required: true
  }
})
</script>
