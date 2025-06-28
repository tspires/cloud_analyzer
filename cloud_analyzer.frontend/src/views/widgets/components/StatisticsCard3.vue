<template>
  <b-card no-body>
    <b-card-body>
      <b-row>
        <b-col cols="6">
          <div class="avatar-md bg-light bg-opacity-50 rounded">
            <div class="avatar-title">
              <Icon :icon="item.icon" :class="`fs-32 text-${item.variant}`" />
            </div>
          </div>
        </b-col>

        <b-col cols="6" class="text-end">
          <p class="text-muted mb-0 text-truncate">
            {{ item.title }}
          </p>
          <h3 class="text-dark mt-1 mb-0">
            <span v-if="item.prefix">{{ item.prefix }}</span>{{ item.statistic }}<span v-if="item.suffix">{{ item.suffix }}</span>
          </h3>
        </b-col>
      </b-row>
    </b-card-body>

    <b-card-footer class="py-2 bg-light bg-opacity-50">
      <div class="d-flex align-items-center justify-content-between">
        <div v-if="item.growth">
          <span class="text-success" :class="item.growth > 0 ? 'text-success' : 'text-danger'">
            <i v-if="item.growth > 0" class="bx bxs-up-arrow fs-12"></i>
            <i v-else class="bx bxs-down-arrow fs-12"></i>
            {{ Math.abs(item.growth) }}%
          </span>
          <span class="text-muted ms-1 fs-12">Last Month</span>
        </div>
        <a href="#!" class="text-reset fw-semibold fs-12">View More</a>
      </div>
    </b-card-footer>
  </b-card>
</template>

<script lang="ts" setup>
import type { PropType } from 'vue';
import type { StatisticCardType } from '@/types';
import { Icon } from '@iconify/vue';

defineProps({
  item: {
    type: Object as PropType<StatisticCardType>,
    required: true
  }
});
</script>
