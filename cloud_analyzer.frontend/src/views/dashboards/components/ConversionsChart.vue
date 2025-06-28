<template>
  <b-col lg="3">
    <div class="p-3">
      <b-card-title tag="h5">Conversions</b-card-title>
      <ApexChart :chart="conversionsChart" id="conversions" class="apex-charts mb-2 mt-n2" />
      <b-row class="text-center">
        <b-col cols="6">
          <p class="text-muted mb-2">This Week</p>
          <h3 class="text-dark mb-3">23.5k</h3>
        </b-col>
        <b-col cols="6">
          <p class="text-muted mb-2">Last Week</p>
          <h3 class="text-dark mb-3">41.05k</h3>
        </b-col>
      </b-row>
      <div class="text-center">
        <b-button type="button" variant="light" class="shadow-none w-100">View Details</b-button>
      </div>
    </div>
  </b-col>
</template>
<script setup lang="ts">
import { conversionsChart } from '@/views/dashboards/components/data';
</script>