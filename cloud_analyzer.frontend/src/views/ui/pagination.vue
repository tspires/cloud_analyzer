<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="9">
          <UIComponentCard title="Default Buttons" id="default-buttons">
            <b-pagination v-model="currentPage" :total-rows="15" :per-page="perPageItem" prev-text="Previous"
                          next-text="Next" class="mt-3"/>

            <b-pagination v-model="currentPage" :total-rows="15" :per-page="perPageItem" class="mb-0"/>
          </UIComponentCard>

          <UIComponentCard title="Rounded Pagination" id="rounded-pagination">
            <b-pagination pills v-model="currentPage" :total-rows="15" :per-page="perPageItem" prev-text="Previous"
                          next-text="Next" class="mt-3" :hideEllipsis="true"/>

            <b-pagination pills v-model="currentPage" :total-rows="15" :per-page="perPageItem" class="mb-0"/>
          </UIComponentCard>

          <UIComponentCard title="Alignment" id="alignment">
            <b-pagination v-model="currentPage" :total-rows="15" :per-page="perPageItem" prev-text="Previous"
                          next-text="Next" class="justify-content-center mt-3"/>

            <b-pagination v-model="currentPage" :total-rows="15" :per-page="perPageItem" prev-text="Previous"
                          next-text="Next" class="justify-content-end mb-0"/>
          </UIComponentCard>

          <UIComponentCard title="Sizing" id="sizing">
            <b-pagination v-model="currentPage" :total-rows="15" :per-page="perPageItem" size="lg" class="mt-3"/>

            <b-pagination v-model="currentPage" :total-rows="15" :per-page="perPageItem"/>

            <b-pagination v-model="currentPage" :total-rows="15" :per-page="perPageItem" size="sm" class="mb-0"/>
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

const perPageItem = ref(5)
const currentPage = ref(1)

const anchorNavigation = [
  {
    id: 'default-buttons',
    title: 'Default Buttons'
  },
  {
    id: 'rounded-pagination',
    title: 'Rounded Pagination'
  },
  {
    id: 'alignment',
    title: 'Alignment'
  },
  {
    id: 'sizing',
    title: 'Sizing'
  }
]
</script>
