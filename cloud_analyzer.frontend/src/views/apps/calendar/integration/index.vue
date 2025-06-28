<template>
  <VerticalLayout>
    <b-row class="row-cols-1 row-cols-md-2 row-cols-lg-3 row-cols-xl-4 gx-3">
      <b-col v-for="(integration, idx) in integrationData" :key="idx">
        <IntegrationCard :integration="integration" />
      </b-col>
    </b-row>
  </VerticalLayout>
</template>
<script setup lang="ts">
import VerticalLayout from "@/layouts/VerticalLayout.vue";
import IntegrationCard from '@/views/apps/calendar/integration/components/IntegrationCard.vue';
import { integrationData } from '@/views/apps/calendar/integration/components/data'
</script>