<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="9">
          <UIComponentCard title="Basic Treemap" id="basic">
            <div dir="ltr">
              <ApexChart :chart="basicTreemapChart" class="apex-charts" id="basic-treemap"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Treemap Multiple Series" id="multiple">
            <div dir="ltr">
              <ApexChart :chart="multipleSeriesTreemapChart" class="apex-charts" id="multiple-treemap"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Distributed Treemap" id="distributed">
            <div dir="ltr">
              <ApexChart :chart="distributedTreemapChart" class="apex-charts" id="distributed-treemap"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Color Range Treemap" id="color-range">
            <div dir="ltr">
              <ApexChart :chart="colorRangeTreemapChart" class="apex-charts" id="color-range-treemap"/>
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
import UIComponentCard from '@/components/UIComponentCard.vue'
import ApexChart from '@/components/ApexChart.vue'
import {
  basicTreemapChart,
  multipleSeriesTreemapChart,
  distributedTreemapChart,
  colorRangeTreemapChart
} from '@/views/charts/treemap/data'

const anchorNavigation = [
  {
    id: 'basic',
    title: 'Basic'
  },
  {
    id: 'multiple',
    title: 'Treemap Multiple Series'
  },
  {
    id: 'distributed',
    title: 'Distributed Treemap'
  },
  {
    id: 'color-range',
    title: 'Color Range Treemap'
  }
]
</script>
