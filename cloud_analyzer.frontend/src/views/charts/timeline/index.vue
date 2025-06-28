<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="9">
          <UIComponentCard title="Basic Timeline" id="basic">
            <div dir="ltr">
              <ApexChart :chart="basicTimelineChart" class="apex-charts" id="basic-timeline"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Distributed Timeline" id="distributed">
            <div dir="ltr">
              <ApexChart :chart="distributedTimelineChart" class="apex-charts" id="distributed-timeline"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Multi Series Timeline" id="multi-series">
            <div dir="ltr">
              <ApexChart :chart="multiSeriesTimelineChart" class="apex-charts" id="multi-series-timeline"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Advanced Timeline" id="advanced">
            <div dir="ltr">
              <ApexChart :chart="advancedTimelineChart" class="apex-charts" id="advanced-timeline"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Multiple Series - Group Rows" id="group-rows">
            <div dir="ltr">
              <ApexChart :chart="groupRowsTimelineChart" class="apex-charts" id="group-rows-timeline"/>
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
  basicTimelineChart,
  distributedTimelineChart,
  multiSeriesTimelineChart,
  advancedTimelineChart,
  groupRowsTimelineChart
} from '@/views/charts/timeline/data'

const anchorNavigation = [
  {
    id: 'basic',
    title: 'Basic Timeline'
  },
  {
    id: 'distributed',
    title: 'Distributed Timeline'
  },
  {
    id: 'multi-series',
    title: 'Multi Series Timeline'
  },
  {
    id: 'advanced',
    title: 'Advanced Timeline'
  },
  {
    id: 'group-rows',
    title: 'Multiple Series - Group Rows'
  }
]
</script>
