<template>
  <VerticalLayout>
    <b-row>
      <b-col md="6" xl="3" v-for="(item, idx) in statistics1" :key="idx">
        <StatisticsCard1 :item="item" />
      </b-col>
    </b-row>

    <b-row>
      <b-col v-for="(item, idx) in statistics2" :key="idx">
        <StatisticsCard2 :item="item" />
      </b-col>
    </b-row>

    <b-row>
      <b-col md="6" xl="3" v-for="(item, idx) in statistics3" :key="idx">
        <StatisticsCard3 :item="item" />
      </b-col>
    </b-row>

    <b-row>
      <b-col xl="6">
        <ProjectSummary />
      </b-col>

      <b-col xl="6">
        <Schedule />
      </b-col>
    </b-row>

    <b-row>
      <b-col cols="12">
        <b-card no-body>
          <div class="p-0">
            <b-row class="g-0">
              <b-col lg="4">
                <div class="p-3">
                  <b-card-title tag="h4"> Conversions</b-card-title>
                  <ApexChart :chart="conversionsChart" class="apex-charts mb-2 mt-n2" />
                  <b-row class="text-center">
                    <b-col cols="6">
                      <p class="text-muted mb-2">This Week</p>
                      <h3 class="text-dark mb-3">23.5k</h3>
                    </b-col>
                    <b-col cols="6">
                      <p class="text-muted mb-2">Last Week</p>
                      <h3 class="text-dark mb-3">41.05k</h3>
                    </b-col>
                  </b-row>
                  <div class="text-center">
                    <b-button variant="light" type="button" class="shadow-none w-100"> View Details</b-button>
                  </div>
                </div>
              </b-col>
              <b-col lg="8" class="border-start border-5">
                <div class="p-3">
                  <div class="d-flex justify-content-between align-items-center">
                    <b-card-title tag="h4"> Performance</b-card-title>
                    <div>
                      <b-button variant="outline-light" size="sm" class="me-1">ALL</b-button>
                      <b-button variant="outline-light" size="sm" class="me-1">1M</b-button>
                      <b-button variant="outline-light" size="sm" class="me-1">6M</b-button>
                      <b-button variant="outline-light" size="sm" class="active">1Y</b-button>
                    </div>
                  </div>
                  <b-alert v-model="performanceAlert" variant="info" class="mt-3 text text-truncate mb-0"> We regret
                    to inform you that our server is currently experiencing technical difficulties.
                  </b-alert>
                  <div dir="ltr">
                    <ApexChart :chart="performanceChart" class="apex-charts" />
                  </div>
                </div>
              </b-col>
            </b-row>
          </div>
        </b-card>
      </b-col>
    </b-row>

    <b-row>
      <b-col xl="4">
        <Tasks />
      </b-col>

      <b-col xl="4">
        <FriendRequests />
      </b-col>

      <b-col xl="4">
        <RecentTransactions />
      </b-col>
    </b-row>
  </VerticalLayout>
</template>

<script setup lang="ts">
import VerticalLayout from "@/layouts/VerticalLayout.vue";
import ApexChart from '@/components/ApexChart.vue';
import StatisticsCard1 from '@/views/widgets/components/StatisticsCard1.vue';
import StatisticsCard2 from '@/views/widgets/components/StatisticsCard2.vue';
import StatisticsCard3 from '@/views/widgets/components/StatisticsCard3.vue';
import ProjectSummary from '@/views/widgets/components/ProjectSummary.vue';
import Schedule from '@/views/widgets/components/Schedule.vue';
import Tasks from '@/views/widgets/components/Tasks.vue';
import FriendRequests from '@/views/widgets/components/FriendRequests.vue';
import RecentTransactions from '@/views/widgets/components/RecentTransactions.vue';

import {
  statistics1,
  statistics2,
  statistics3,
  conversionsChart,
  performanceChart
} from '@/views/widgets/components/data';

import { ref } from 'vue';

const performanceAlert = ref<boolean>(true);
</script>
