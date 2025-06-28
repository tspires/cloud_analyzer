<template>
  <b-card no-body>
    <b-card-body>
      <DropDown custom-class="float-end">
        <a href="javascript:void(0);" class="dropdown-toggle arrow-none" data-bs-toggle="dropdown"
          aria-expanded="false">
          <i class="bx bx-dots-vertical-rounded fs-18 text-dark"></i>
        </a>
        <div class="dropdown-menu dropdown-menu-end">
          <a href="javascript:void(0);" class="dropdown-item">
            <i class="bx bx-list-ul me-2"></i>To Do
          </a>
          <a href="javascript:void(0);" class="dropdown-item">
            <i class="bx bx-line-chart me-2"></i>In Progress
          </a>
          <a href="javascript:void(0);" class="dropdown-item">
            <i class="bx bx-check-square me-2"></i>Completed
          </a>
        </div>
      </DropDown>
      <b-card-title tag="h5" class="mb-3"> Today's Schedules</b-card-title>
      <b-row v-for="(schedule, idx) in scheduleData" :key="idx" class="align-items-center">
        <b-col cols="3" sm="2">
          <p :class="{ 'mb-0': idx === scheduleData.length - 1 }">{{ schedule.time.startAt }}</p>
        </b-col>
        <b-col sm="10" cols="9">
          <b-alert :variant="schedule.variant" :model-value="true" class="px-2" :class="{ 'mb-0': idx === scheduleData.length - 1 }" role="alert">
            <p class="mb-0"> {{ schedule.task }} </p>
            <p class="mb-0">{{ schedule.time.startAt }} - {{ schedule.time.endAt }}</p>
          </b-alert>
        </b-col>
      </b-row>
    </b-card-body>
  </b-card>
</template>

<script setup lang="ts">
import { scheduleData } from '@/views/widgets/components/data';
import DropDown from '@/components/DropDown.vue';
</script>
