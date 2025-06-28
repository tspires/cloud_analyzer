<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="9">
          <UIComponentCard title="Basic Heatmap - Single Series" id="basic">
            <div dir="ltr">
              <ApexChart :chart="basicHeatmap" class="apex-charts" id="basic-heatmap"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Heatmap - Multiple Series" id="multiple-series">
            <div dir="ltr">
              <ApexChart :chart="multipleHeatmap" class="apex-charts" id="multiple-series-heatmap"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Heatmap - Color Range" id="color-range">
            <div dir="ltr">
              <ApexChart :chart="colorRangeHeatmap" class="apex-charts" id="color-range-heatmap"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Heatmap - Range without Shades" id="rounded">
            <div dir="ltr">
              <ApexChart :chart="rangeWithoutShade" class="apex-charts" id="rounded-heatmap"/>
            </div>
          </UIComponentCard>
        </b-col>

        <b-col xl="3">
          <AnchorNavigation :elements="anchorNavigation"/>
        </b-col>
      </b-row>
  </VerticalLayout>
</template>

<script setup lang="ts">
import VerticalLayout from "@/layouts/VerticalLayout.vue";
import AnchorNavigation from '@/components/AnchorNavigation.vue'

import ApexChart from '@/components/ApexChart.vue'
import UIComponentCard from '@/components/UIComponentCard.vue'
import {basicHeatmap, multipleHeatmap, colorRangeHeatmap, rangeWithoutShade} from '@/views/charts/heatmap/data'

const anchorNavigation = [
  {
    id: 'basic',
    title: 'Basic Heatmap - Single Series'
  },
  {
    id: 'multiple-series',
    title: 'Heatmap - Multiple Series'
  },
  {
    id: 'color-range',
    title: 'Heatmap - Color Range'
  },
  {
    id: 'rounded',
    title: 'Heatmap - Range without Shades'
  }
]
</script>
