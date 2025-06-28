<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="9">
          <UIComponentCard title="Basic Polar Area Chart" id="basic">
            <div dir="ltr">
              <ApexChart :chart="basicPolarAreaChart" class="apex-charts" id="basic-polar-area"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Monochrome Polar Area" id="monochrome">
            <div dir="ltr">
              <ApexChart :chart="monochromePolarAreaChart" class="apex-charts" id="monochrome-polar-area"/>
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
import {basicPolarAreaChart, monochromePolarAreaChart} from '@/views/charts/polar/data'

const anchorNavigation = [
  {
    id: 'basic',
    title: 'Basic Polar Area Chart'
  },
  {
    id: 'monochrome',
    title: 'Monochrome Polar Area'
  }
]
</script>
