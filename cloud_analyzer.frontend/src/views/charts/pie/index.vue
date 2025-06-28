<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="9">
          <UIComponentCard title="Simple Pie Chart" id="simple_pie">
            <div dir="ltr">
              <ApexChart :chart="simplePie" class="apex-charts" id="simple-pie"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Simple Donut Chart" id="simple_donut">
            <div dir="ltr">
              <ApexChart :chart="simpleDonut" class="apex-charts" id="simple-donut"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Monochrome Pie Chart" id="monochrome">
            <div dir="ltr">
              <ApexChart :chart="monochromePie" class="apex-charts" id="monochrome-pie"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Gradient Donut Chart" id="gradient">
            <div dir="ltr">
              <ApexChart :chart="gradientDonut" class="apex-charts" id="gradient-donut"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Patterned Donut Chart" id="patterned">
            <div dir="ltr">
              <ApexChart :chart="patternedDonut" class="apex-charts" id="patterned-donut"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Pie Chart with Image fill" id="image">
            <div dir="ltr">
              <ApexChart :chart="imageFill" class="apex-charts" id="image-pie"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Donut Update" id="update">
            <div dir="ltr">
              <apexchart type="donut" height="320" :options="donutUpdate" :series="series" class="apex-charts"/>
            </div>
            <div class="text-center mt-2 d-flex justify-content-center gap-1">
              <b-button variant="primary" size="sm" id="randomize" @click="randomize"> RANDOMIZE</b-button>
              <b-button variant="primary" size="sm" id="add" @click="appendData"> ADD</b-button>
              <b-button variant="primary" size="sm" id="remove" @click="removeData"> REMOVE</b-button>
              <b-button variant="primary" size="sm" id="reset" @click="reset"> RESET</b-button>
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
import {ref} from 'vue'
import VerticalLayout from "@/layouts/VerticalLayout.vue";

import AnchorNavigation from '@/components/AnchorNavigation.vue'
import UIComponentCard from '@/components/UIComponentCard.vue'
import ApexChart from '@/components/ApexChart.vue'
import {
  simplePie,
  simpleDonut,
  monochromePie,
  gradientDonut,
  patternedDonut,
  imageFill,
  donutUpdate
} from '@/views/charts/pie/data'

const series = ref([44, 55, 13, 33])

const appendData = () => {
  let arr = series.value.slice()
  arr.push(Math.floor(Math.random() * (100 - 1 + 1)) + 1)
  series.value = arr
}

const removeData = () => {
  if (series.value.length === 1) return
  let arr = series.value.slice()
  arr.pop()
  series.value = arr
}

const randomize = () => {
  series.value = series.value.map(function () {
    return Math.floor(Math.random() * (100 - 1 + 1)) + 1
  })
}

const reset = () => {
  series.value = [44, 55, 13, 33]
}

const anchorNavigation = [
  {
    id: 'simple_pie',
    title: 'Simple Pie Chart'
  },
  {
    id: 'simple_donut',
    title: 'Simple Donut Chart'
  },
  {
    id: 'monochrome',
    title: 'Monochrome Pie Area'
  },
  {
    id: 'gradient',
    title: 'Gradient Donut Chart'
  },
  {
    id: 'patterned',
    title: 'Patterned Donut Chart'
  },
  {
    id: 'image',
    title: 'Pie Chart with Image fill'
  },
  {
    id: 'update',
    title: 'Donut Update'
  }
]
</script>
