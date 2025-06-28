<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="9">
          <UIComponentCard title="Basic Radar Chart" id="basic">
            <div dir="ltr">
              <ApexChart :chart="basicRadarChart" class="apex-charts" id="basic-radar"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Radar with Polygon-fill" id="polygon">
            <div dir="ltr">
              <ApexChart :chart="polygonFillChart" class="apex-charts" id="radar-polygon"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Radar – Multiple Series" id="multiple-series">
            <div dir="ltr">
              <apexchart type="radar" height="350" :options="multipleSeriesChart" :series="series" class="apex-charts"/>
              <div class="text-center mt-2">
                <b-button @click="update" variant="primary" size="sm"> Update</b-button>
              </div>
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
import {basicRadarChart, polygonFillChart, multipleSeriesChart} from '@/views/charts/radar/data'
import {ref} from 'vue'

const series = ref([
  {
    name: 'Series 1',
    data: [80, 50, 30, 40, 100, 20]
  },
  {
    name: 'Series 2',
    data: [20, 30, 40, 80, 20, 80]
  },
  {
    name: 'Series 3',
    data: [44, 76, 78, 13, 43, 10]
  }
])

const update = () => {
  function randomSeries() {
    const arr = []
    for (let i = 0; i < 6; i++) {
      arr.push(Math.floor(Math.random() * 100))
    }
    return arr
  }

  series.value = [
    {
      name: 'Series 1',
      data: randomSeries()
    },
    {
      name: 'Series 2',
      data: randomSeries()
    },
    {
      name: 'Series 3',
      data: randomSeries()
    }
  ]
}

const anchorNavigation = [
  {
    id: 'basic',
    title: 'Basic Radar Chart'
  },
  {
    id: 'polygon',
    title: 'Radar with Polygon-fill'
  },
  {
    id: 'multiple-series',
    title: 'Radar – Multiple Series'
  }
]
</script>
