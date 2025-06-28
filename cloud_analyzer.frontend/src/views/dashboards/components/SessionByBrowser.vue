<template>
  <b-col lg="3">
    <b-card-title tag="h5" class="p-3">Session By Browser</b-card-title>
    <simplebar class="px-3" data-simplebar style="max-height: 310px;">
      <div class="d-flex justify-content-between align-items-center p-2" v-for="(item, idx) in sessionBrowser" :key="idx">
        <span class="align-middle fw-medium">{{ item.name }}</span>
        <span class="fw-semibold text-muted">{{ item.percentage }}%</span>
        <span class="fw-semibold text-muted">{{ item.amount }}k</span>
      </div>
    </simplebar>
    <div class="text-center p-3">
      <b-button type="button" variant="light" class="shadow-none w-100">View All</b-button>
    </div>
  </b-col>
</template>
<script setup lang="ts">
import simplebar from 'simplebar-vue'
import { sessionBrowser } from '@/views/dashboards/components/data';
</script>