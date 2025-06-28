<template>
  <b-col lg="6">
    <b-card no-body>
      <b-card-header class="d-flex justify-content-between align-items-center border-bottom border-dashed">
        <b-card-title>Sessions by Country</b-card-title>
        <b-dropdown size="sm" variant="outline-light" text="View Data" menu-class="dropdown-menu-end">
          <b-dropdown-item>Download</b-dropdown-item>
          <b-dropdown-item>Export</b-dropdown-item>
          <b-dropdown-item>Import</b-dropdown-item>
        </b-dropdown>
      </b-card-header>
      <b-card-body class="pt-0">
        <b-row class="align-items-center">
          <b-col lg="7">
            <JsVectorMap id="world-map-markers" class="mt-3" :height="220" :options="worldMapOptions" />
          </b-col>
          <b-col lg="5" dir="ltr">
            <div class="p-3 pb-0">
              <template v-for="(item, idx) in countries" :key="idx">
                <div class="d-flex justify-content-between align-items-center">
                  <p class="mb-1">
                    <Icon :icon="item.icon" class="fs-16 align-middle me-1" />
                    <span class="align-middle">{{ item.name }}</span>
                  </p>
                </div>
                <b-row class="align-items-center" :class="!(countries.length - 1 === idx) && 'mb-3'">
                  <div class="col">
                    <b-progress class="progress-soft progress-sm">
                      <b-progress-bar :value="item.value" :variant="item.variant" />
                    </b-progress>
                  </div>
                  <div class="col-auto">
                    <p class="mb-0 fs-13 fw-semibold">{{ item.amount }}k</p>
                  </div>
                </b-row>
              </template>
            </div>
          </b-col>
        </b-row>
      </b-card-body>
    </b-card>
  </b-col>
</template>
<script setup lang="ts">
import { Icon } from "@iconify/vue";
import { countries } from '@/views/dashboards/components/data';

const worldMapOptions = {
  map: 'world',
  selector: '#world-map-markers',
  zoomOnScroll: true,
  zoomButtons: false,
  markersSelectable: true,
  markers: [
    { name: 'Canada', coords: [56.1304, -106.3468] },
    { name: 'Brazil', coords: [-14.235, -51.9253] },
    { name: 'Russia', coords: [61, 105] },
    { name: 'China', coords: [35.8617, 104.1954] },
    { name: 'United States', coords: [37.0902, -95.7129] }
  ],
  markerStyle: {
    initial: { fill: '#7f56da' },
    selected: { fill: '#22c55e' }
  },
  labels: {
    markers: {
      render: (marker: any) => marker.name
    }
  },
  regionStyle: {
    initial: {
      fill: 'rgba(169,183,197, 0.3)',
      fillOpacity: 1
    }
  }
};
</script>