<template>
  <b-card no-body class="card-height-100">
    <b-card-body>
      <div class="float-end">
        <div class="form-check form-switch">
          <input class="form-check-input" type="checkbox" id="googleMailSwitch" :checked="integration.checked" />
        </div>
      </div>
      <img :src="integration.image" alt="Google Mail" class="img-fluid avatar-sm" />
      <b-card-title tag="h5" class="mt-3 mb-2">
        {{ integration.name }}
      </b-card-title>
      <p class="mb-0">
        {{ integration.description }}
      </p>
    </b-card-body>
  </b-card>
</template>

<script setup lang="ts">
import type { PropType } from 'vue'
import type { IntegrationType } from '@/views/apps/calendar/integration/components/types'

defineProps({
  integration: {
    type: Object as PropType<IntegrationType>,
    required: true
  }
})
</script>
