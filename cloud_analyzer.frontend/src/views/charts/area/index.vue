<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="9">
          <UIComponentCard title="Basic Area Chart" id="basic">
            <div dir="ltr">
              <div id="basic-area" class="apex-charts">
                <ApexChart :chart="basicAreaChart" class="apex-charts" id="basic-area"/>
              </div>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Spline Area" id="spline">
            <div dir="ltr">
              <ApexChart :chart="spilineChart" class="apex-charts" id="spline-area"/>
            </div>
          </UIComponentCard>

          <b-card no-body>
            <b-card-body>
              <div class="d-flex flex-wrap align-items-center justify-content-between gap-2 mb-3">
                <b-card-title tag="h5" class="anchor" id="datetime"> Area Chart - Datetime X-axis<a class="anchor-link"
                                                                                                    href="#datetime">#</a>
                </b-card-title>
                <div class="toolbar apex-toolbar hstack gap-1">
                  <b-button id="one_month" size="sm" :variant="null" class="btn-soft-secondary"> 1M</b-button>
                  <b-button id="six_months" size="sm" :variant="null" class="btn-soft-secondary"> 6M</b-button>
                  <b-button id="one_year" size="sm" :variant="null" class="btn-soft-secondary active"> 1Y</b-button>
                  <b-button id="ytd" size="sm" :variant="null" class="btn-soft-secondary"> YTD</b-button>
                  <b-button id="all" size="sm" :variant="null" class="btn-soft-secondary"> ALL</b-button>
                </div>
              </div>
              <div dir="ltr">
                <ApexChart :chart="dateTimeChart" class="apex-charts" id="area-chart-datetime"/>
              </div>
            </b-card-body>
          </b-card>

          <UIComponentCard title="Area with Negative Values" id="negative">
            <div dir="ltr">
              <ApexChart :chart="negativeValuesChart" class="apex-charts" id="area-chart-negative"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Stacked Area" id="stacked">
            <div dir="ltr">
              <ApexChart :chart="stackedChart" class="apex-charts" id="stacked-area"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Irregular TimeSeries" id="timeSeries">
            <div dir="ltr">
              <ApexChart :chart="irregularTimeSeries" class="apex-charts" id="area-timeSeries"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Area Chart with Null values" id="chart-nullvalues">
            <div dir="ltr">
              <ApexChart :chart="areaNullValueChart" class="apex-charts" id="area-chart-nullvalues"/>
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
  basicAreaChart,
  spilineChart,
  dateTimeChart,
  negativeValuesChart,
  stackedChart,
  irregularTimeSeries,
  areaNullValueChart
} from '@/views/charts/area/data'

const anchorNavigation = [
  {
    id: 'basic',
    title: 'Basic Area Chart'
  },
  {
    id: 'spline',
    title: 'Spline Area'
  },
  {
    id: 'datetime',
    title: 'Area Chart - Datetime X-axis'
  },
  {
    id: 'negative',
    title: 'Area with Negative Values'
  },
  {
    id: 'stacked',
    title: 'Stacked Area'
  },
  {
    id: 'timeSeries',
    title: 'Irregular TimeSeries'
  },
  {
    id: 'chart-nullvalues',
    title: 'Area Chart with Null values'
  }
]
</script>
