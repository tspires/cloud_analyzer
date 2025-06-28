<template>
  <b-col lg="6" class="border-start border-end">
    <div class="p-3">
      <div class="d-flex justify-content-between align-items-center">
        <b-card-title>Performance</b-card-title>
        <div>
          <button type="button" class="btn btn-sm btn-outline-light">ALL</button>{{ ' ' }}
          <button type="button" class="btn btn-sm btn-outline-light">1M</button>{{ ' ' }}
          <button type="button" class="btn btn-sm btn-outline-light">6M</button>{{ ' ' }}
          <button type="button" class="btn btn-sm btn-outline-light active">1Y</button>
        </div>
      </div>

      <div class="alert alert-warning mt-3 text text-truncate mb-0" role="alert">
        We regret to inform you that our server is currently experiencing technical difficulties.
      </div>

      <div dir="ltr">
        <ApexChart :chart="performanceChart" id="dash-performance-chart" class="apex-charts" />
      </div>
    </div>
  </b-col>
</template>
<script setup lang="ts">
import { performanceChart } from '@/views/dashboards/components/data';
</script>