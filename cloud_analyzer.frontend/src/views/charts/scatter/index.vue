<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="9">
          <UIComponentCard title="Scatter (XY) Chart" id="basic">
            <div dir="ltr">
              <ApexChart :chart="scatterXYChart" class="apex-charts" id="basic-scatter"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Scatter Chart - Datetime" id="datetime">
            <div dir="ltr">
              <ApexChart :chart="dateTimeChart" class="apex-charts" id="datetime-scatter"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Scatter - Images" id="images">
            <div dir="ltr">
              <ApexChart :chart="scatterWithImagesChart" class="apex-charts scatter-images-chart" id="scatter-images"/>
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
import {scatterXYChart, dateTimeChart, scatterWithImagesChart} from '@/views/charts/scatter/data'

const anchorNavigation = [
  {
    id: 'basic',
    title: 'Scatter (XY) Chart'
  },
  {
    id: 'datetime',
    title: 'Scatter Chart - Datetime'
  },
  {
    id: 'images',
    title: 'Scatter - Images'
  }
]
</script>
