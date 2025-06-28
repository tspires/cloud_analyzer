<template>
  <b-card no-body>
    <b-card-header class="d-flex justify-content-between align-items-center">
      <b-card-title tag="h4"> Recent Transactions </b-card-title>
      <div>
        <a href="#!" class="btn btn-sm btn-primary"> <i class="bx bx-plus me-1"></i>Add </a>
      </div>
    </b-card-header>

    <b-card-body class="p-0">
      <simplebar class="px-3" data-simplebar style="max-height: 406px">
        <b-table-simple hover class="mb-0 table-centered">
          <b-tbody>
            <b-tr v-for="(transaction, idx) in recentTransaction" :key="idx">
              <b-td>{{ transaction.date }}</b-td>
              <b-td>{{ transaction.amount }}</b-td>
              <b-td>
                <b-badge :class="transaction.status === 'cr' ? 'bg-success' : 'bg-danger'">{{ toSentenceCase(transaction.status) }} </b-badge>
              </b-td>
              <b-td>{{ transaction.description }}</b-td>
            </b-tr>
          </b-tbody>
        </b-table-simple>
      </simplebar>
    </b-card-body>
  </b-card>
</template>

<script setup lang="ts">
import simplebar from 'simplebar-vue'
import { recentTransaction } from '@/views/widgets/components/data'
import { toSentenceCase } from '@/helpers/change-casing'
</script>
