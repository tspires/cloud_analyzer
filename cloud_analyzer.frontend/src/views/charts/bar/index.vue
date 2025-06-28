<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="9">
          <UIComponentCard title="Basic Bar Chart" id="basic">
            <ApexChart :chart="basicBarChart" class="apex-charts" id="basic-bar"/>
          </UIComponentCard>

          <UIComponentCard title="Grouped Bar Chart" id="grouped">
            <ApexChart :chart="groupedBarChart" class="apex-charts text-white" id="grouped-bar"/>
          </UIComponentCard>

          <UIComponentCard title="Stacked Bar Chart" id="stacked">
            <ApexChart :chart="stackedChart" class="apex-charts" id="stacked-bar" dir="ltr"/>
          </UIComponentCard>

          <UIComponentCard title="100% Stacked Bar Chart" id="full-stacked">
            <ApexChart :chart="fullStackedChart" class="apex-charts" id="full-stacked-bar"/>
          </UIComponentCard>

          <UIComponentCard title="Bar with Negative Values" id="negative">
            <ApexChart :chart="negativeValueChart" class="apex-charts" id="negative-bar"/>
          </UIComponentCard>

          <UIComponentCard title="Reversed Bar Chart" id="reversed">
            <ApexChart :chart="reversedChart" class="apex-charts" id="reversed-bar"/>
          </UIComponentCard>

          <UIComponentCard title="Bar with Image Fill" id="image-fill">
            <ApexChart :chart="imageChart" class="apex-charts" id="image-fill-bar"/>
          </UIComponentCard>

          <UIComponentCard title="Custom DataLabels Bar" id="datalables">
            <ApexChart :chart="customDataLabelsChart" class="apex-charts" id="datalables-bar"/>
          </UIComponentCard>

          <UIComponentCard title="Patterned Bar Chart" id="pattern">
            <ApexChart :chart="patternChart" class="apex-charts" id="pattern-bar"/>
          </UIComponentCard>

          <UIComponentCard title="Bar with Markers" id="markers">
            <ApexChart :chart="chartWithMarker" class="apex-charts" id="bar-bar"/>
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
  basicBarChart,
  groupedBarChart,
  stackedChart,
  fullStackedChart,
  negativeValueChart,
  reversedChart,
  imageChart,
  customDataLabelsChart,
  patternChart,
  chartWithMarker
} from '@/views/charts/bar/data'

const anchorNavigation = [
  {
    id: 'basic',
    title: 'Basic Bar Chart'
  },
  {
    id: 'grouped',
    title: 'Grouped Bar Chart'
  },
  {
    id: 'stacked',
    title: 'Stacked Bar Chart'
  },
  {
    id: 'full-stacked',
    title: '100% Stacked Bar Chart'
  },
  {
    id: 'negative',
    title: 'Bar with Negative Values'
  },
  {
    id: 'reversed',
    title: 'Reversed Bar Chart'
  },
  {
    id: 'image-fill',
    title: 'Bar with Image Fill'
  },
  {
    id: 'datalables',
    title: 'Custom DataLabels Bar'
  },
  {
    id: 'pattern',
    title: 'Patterned Bar Chart'
  },
  {
    id: 'markers',
    title: 'Bar with Markers'
  }
]
</script>
