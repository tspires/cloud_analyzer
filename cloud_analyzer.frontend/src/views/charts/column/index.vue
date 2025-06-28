<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="9">
          <UIComponentCard title="Basic Column Chart" id="basic">
            <div dir="ltr">
              <ApexChart :chart="basicChart" class="apex-charts" id="basic-column"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Column Chart with Datalabels" id="datalabels">
            <div dir="ltr">
              <ApexChart :chart="dataLabelsChart" class="apex-charts" id="datalabels-column"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Stacked Column Chart" id="stacked">
            <div dir="ltr">
              <ApexChart :chart="stackedChart" class="apex-charts" id="stacked-column"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="100% Stacked Column Chart" id="full-stacked">
            <div dir="ltr">
              <ApexChart :chart="fullStackedChart" class="apex-charts" id="full-stacked-column"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Column with Markers" id="markers">
            <div dir="ltr">
              <ApexChart :chart="markersChart" class="apex-charts" id="column-with-markers"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Column with Group Label" id="group">
            <div dir="ltr">
              <ApexChart :chart="groupLabelChart" class="apex-charts" id="column-with-group-label"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Column Chart with rotated labels & Annotations" id="rotate-labels">
            <div dir="ltr">
              <ApexChart :chart="columnWithRotatedLabels" class="apex-charts" id="rotate-labels-column"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Column Chart with negative values" id="negative-value">
            <div dir="ltr">
              <ApexChart :chart="columnWithNegativeValue" class="apex-charts" id="negative-value-column"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Distributed Column Chart" id="distributed">
            <div dir="ltr">
              <ApexChart :chart="distributedColumn" class="apex-charts" id="distributed-column"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Range Column Chart" id="range">
            <div dir="ltr">
              <ApexChart :chart="rangeColumn" class="apex-charts" id="range-column"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Dynamic Loaded Chart" id="dynamic">
            <div dir="ltr">
              <ApexChart :chart="yearChartOptions" @dataPointSelection="dataPointSelectionHandler" class="apex-charts"
                         id="chart-year"/>
              <ApexChart :chart="quarterChartOptions" class="apex-charts" id="chart-quarter"/>
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

import UIComponentCard from '@/components/UIComponentCard.vue'
import AnchorNavigation from '@/components/AnchorNavigation.vue'
import ApexChart from '@/components/ApexChart.vue'
import {
  basicChart,
  dataLabelsChart,
  stackedChart,
  fullStackedChart,
  markersChart,
  groupLabelChart,
  columnWithRotatedLabels,
  columnWithNegativeValue,
  distributedColumn,
  rangeColumn,
  yearChartOptions,
  quarterChartOptions,
  dataPointSelectionHandler
} from '@/views/charts/column/data'

const anchorNavigation = [
  {
    id: 'basic',
    title: 'Basic Column Chart'
  },
  {
    id: 'datalabels',
    title: 'Column Chart with Datalabels'
  },
  {
    id: 'stacked',
    title: 'Stacked Column Chart'
  },
  {
    id: 'full-stacked',
    title: '100% Stacked Column Chart'
  },
  {
    id: 'markers',
    title: 'Column with Markers'
  },
  {
    id: 'group',
    title: 'Column with Group Label'
  },
  {
    id: 'rotate-labels',
    title: 'Column Chart with rotated labels & Annotations'
  },
  {
    id: 'negative-value',
    title: 'Column Chart with negative values'
  },
  {
    id: 'distributed',
    title: 'Distributed Column Chart'
  },
  {
    id: 'range',
    title: 'Range Column Chart'
  },
  {
    id: 'dynamic',
    title: 'Dynamic Loaded Chart'
  }
]
</script>
