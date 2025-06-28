<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="9">
          <UIComponentCard title="Simple Bubble Chart" id="simple">
            <div dir="ltr">
              <ApexChart :chart="simpleChart" class="apex-charts" id="simple-bubble"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="3D Bubble Chart" id="3d-bubble">
            <div dir="ltr">
              <ApexChart :chart="bubbleChart3D" class="apex-charts" id="second-bubble"/>
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
import {simpleChart, bubbleChart3D} from '@/views/charts/bubble/data'

const anchorNavigation = [
  {
    id: 'simple',
    title: 'Simple Bubble Chart'
  },
  {
    id: '3d-bubble',
    title: '3D Bubble Chart'
  }
]
</script>
