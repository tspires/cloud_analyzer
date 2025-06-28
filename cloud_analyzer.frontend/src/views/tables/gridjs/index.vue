<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="10">
          <UIComponentCard id="basic" title="Basic">
            <GridJsTable id="table-gridjs" :options="basicTableOptions"/>
          </UIComponentCard>

          <UIComponentCard id="pagination" title="Pagination">
            <GridJsTable id="table-pagination" :options="paginationTableOptions"/>
          </UIComponentCard>

          <UIComponentCard id="search" title="Search">
            <GridJsTable id="table-search" :options="searchTableOptions"/>
          </UIComponentCard>

          <UIComponentCard id="sorting" title="Sorting">
            <GridJsTable id="table-sorting" :options="sortingTableOptions"/>
          </UIComponentCard>

          <UIComponentCard id="loading_state" title="Loading State">
            <GridJsTable id="table-loading-state" :options="loadingStateTableOptions"/>
          </UIComponentCard>

          <UIComponentCard id="fixed_header" title="Fixed Header">
            <GridJsTable id="table-fixed-header" :options="fixedHeaderTableOptions"/>
          </UIComponentCard>

          <UIComponentCard id="hidden_column" title="Hidden Columns">
            <GridJsTable id="table-hidden-column" :options="hiddenColumnsTableOptions"/>
          </UIComponentCard>
        </b-col>

        <b-col xl="2">
          <AnchorNavigation :elements="anchorNavigation"/>
        </b-col>
      </b-row>
  </VerticalLayout>
</template>

<script setup lang="ts">
import VerticalLayout from "@/layouts/VerticalLayout.vue";
import AnchorNavigation from '@/components/AnchorNavigation.vue'
import UIComponentCard from '@/components/UIComponentCard.vue'
import GridJsTable from '@/components/GridJsTable.vue'

import {
  basicTableOptions,
  fixedHeaderTableOptions,
  hiddenColumnsTableOptions,
  loadingStateTableOptions,
  paginationTableOptions,
  searchTableOptions,
  sortingTableOptions
} from '@/views/tables/gridjs/components/data'

const anchorNavigation = [
  {
    id: 'basic',
    title: 'Basic'
  },
  {
    id: 'pagination',
    title: 'Pagination'
  },
  {
    id: 'search',
    title: 'Search'
  },
  {
    id: 'sorting',
    title: 'Sorting'
  },
  {
    id: 'loading_state',
    title: 'Loading State'
  },
  {
    id: 'fixed_header',
    title: 'Fixed Header'
  },
  {
    id: 'hidden_column',
    title: 'Hidden Columns'
  }
]
</script>
