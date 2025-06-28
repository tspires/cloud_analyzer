<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="9">
          <UIComponentCard title="How it works" id="how-works"
                           caption="A progress bar can be used to show a user how far along he/she is in a process.">
            <b-progress class="mb-2" :value="0"/>
            <b-progress class="mb-2" :value="35"/>
            <b-progress class="mb-2" :value="50"/>
            <b-progress class="mb-2" :value="75"/>
            <b-progress :value="25" show-value/>
          </UIComponentCard>

          <UIComponentCard title="Backgrounds Color" id="backgrounds-color"
                           caption="Use background utility classes to change the appearance of individual progress bars.">
            <b-progress class="mb-2" variant="primary" :value="25"/>
            <b-progress class="mb-2" variant="secondary" :value="35"/>
            <b-progress class="mb-2" variant="success" :value="50"/>
            <b-progress class="mb-2" variant="info" :value="100"/>
            <b-progress>
              <b-progress-bar :value="15"/>
              <b-progress-bar :value="30" variant="secondary"/>
              <b-progress-bar :value="20" variant="success"/>
            </b-progress>
          </UIComponentCard>

          <UIComponentCard title="Striped Progress Bar" id="progress-bar">
            <div class="mt-3">
              <b-progress class="mb-2" variant="primary" striped :value="25"/>
              <b-progress class="mb-2" variant="secondary" striped :value="50"/>
              <b-progress class="mb-2" variant="success" striped :value="75"/>
              <b-progress class="mb-2" variant="info" striped animated :value="65"/>
              <b-progress variant="warning" striped animated :value="100"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Height" id="height">
            <div class="mt-3">
              <b-progress class="mb-2 progress-xs" variant="primary" :value="25"/>
              <b-progress class="mb-2 progress-sm" variant="secondary" :value="50"/>
              <b-progress class="mb-2 progress-md" variant="success" :value="75"/>
              <b-progress class="mb-2 progress-lg" variant="info" :value="35"/>
              <b-progress class="progress-xl" variant="warning" :value="60"/>
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

const anchorNavigation = [
  {
    id: 'how-works',
    title: 'How it works'
  },
  {
    id: 'backgrounds-color',
    title: 'Backgrounds Color'
  },
  {
    id: 'progress-bar',
    title: 'Progress Bar'
  },
  {
    id: 'height',
    title: 'Height'
  }
]
</script>
