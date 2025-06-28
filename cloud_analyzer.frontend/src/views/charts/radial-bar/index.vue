<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="9">
          <UIComponentCard title="Basic RadialBar Chart" titleClass="mb-4" id="basic">
            <div dir="ltr">
              <ApexChart :chart="basicRadialBarChart" class="apex-charts" id="basic-radialbar"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Multiple RadialBars" titleClass="mb-4" id="multiple">
            <div dir="ltr">
              <ApexChart :chart="multipleRadialBarsChart" class="apex-charts" id="multiple-radialbar"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Circle Chart - Custom Angle" titleClass="mb-4" id="circle-angle">
            <div class="text-center" dir="ltr">
              <ApexChart :chart="customAngleChart" class="apex-charts" id="circle-angle-radial"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Circle Chart with Image" titleClass="mb-4" id="image">
            <div dir="ltr">
              <ApexChart :chart="circleWithImageChart" class="apex-charts" id="image-radial"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Stroked Circular Gauge" titleClass="mb-4" id="stroked-guage">
            <div dir="ltr">
              <ApexChart :chart="strokedCircularGuageChart" class="apex-charts" id="stroked-guage-radial"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Gradient Circular Chart" titleClass="mb-4" id="gradient">
            <div dir="ltr">
              <ApexChart :chart="gradientCircularChart" class="apex-charts" id="gradient-chart"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Semi Circle Gauge" titleClass="mb-4" id="semi-circle">
            <div dir="ltr">
              <ApexChart :chart="semiCircleGaugeChart" class="apex-charts" id="semi-circle-gauge"/>
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
  basicRadialBarChart,
  multipleRadialBarsChart,
  customAngleChart,
  circleWithImageChart,
  strokedCircularGuageChart,
  gradientCircularChart,
  semiCircleGaugeChart
} from '@/views/charts/radial-bar/data'

const anchorNavigation = [
  {
    id: 'basic',
    title: 'Basic RadialBar Chart'
  },
  {
    id: 'multiple',
    title: 'Multiple RadialBars'
  },
  {
    id: 'circle-angle',
    title: 'Circle Chart - Custom Angle'
  },
  {
    id: 'image',
    title: 'Circle Chart with Image'
  },
  {
    id: 'stroked-guage',
    title: 'Stroked Circular Gauge'
  },
  {
    id: 'gradient',
    title: 'Gradient Circular Chart'
  },
  {
    id: 'semi-circle',
    title: 'Semi Circle Gauge'
  }
]
</script>
