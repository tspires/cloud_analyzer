<template>
  <b-col lg="6">
    <b-card no-body class="card-height-100">
      <b-card-header class="d-flex align-items-center justify-content-between gap-2">
        <b-card-title class="flex-grow-1">Top Pages</b-card-title>
        <div>
          <a href="#" class="btn btn-sm btn-soft-primary">View All</a>
        </div>
      </b-card-header>
      <div class="table-responsive mb-0">
        <table class="table table-hover table-nowrap table-centered m-0">
          <thead class="bg-light bg-opacity-50">
            <tr>
              <th class="text-muted py-1">Page Path</th>
              <th class="text-muted py-1">Page Views</th>
              <th class="text-muted py-1">Avg Time on Page</th>
              <th class="text-muted py-1">Exit Rate</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, idx) in topPages" :key="idx">
              <td><a href="#" class="text-muted">{{ item.path }}</a></td>
              <td>{{ item.views }}</td>
              <td>{{ item.avgTime }}</td>
              <td><span :class="`badge badge-soft-${item.variant}`">{{ item.exitRate }}%</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </b-card>
  </b-col>
</template>
<script setup lang="ts">
import { topPages } from '@/views/dashboards/components/data';
</script>