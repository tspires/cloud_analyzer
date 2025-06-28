<template>
  <b-card no-body>
    <b-card-body class="p-0">
      <div class="pt-3 px-3">
        <div class="float-end">
          <a href="javascript:void(0);" class="text-primary"
            >Export
            <i class="bx bx-export ms-1"></i>
          </a>
        </div>
        <b-card-title tag="h5" class="mb-3"> Recent Project Summary </b-card-title>
      </div>
      <simplebar class="mb-3" data-simplebar style="max-height: 324px">
        <b-table-simple hover responsive class="mb-0 table-centered table-nowrap px-3">
          <b-thead>
            <b-tr>
              <b-th v-for="(header, idx) in recentProjectsSummaryTableData.header" :key="idx">{{ header }}</b-th>
            </b-tr>
          </b-thead>

          <b-tbody>
            <b-tr v-for="(item, idx) in recentProjectsSummaryTableData.body" :key="idx">
              <b-td>{{ item.project }}</b-td>
              <b-td>{{ item.client }}</b-td>
              <b-td class="avatar-group">
                <a v-for="(member, idx) in item.team" :key="idx" href="javascript:void(0);" class="avatar-group-item">
                  <img :src="member.avatar" alt="" class="img-fluid avatar-xs rounded-circle avatar-border" />
                </a>
              </b-td>
              <b-td>{{ item.deadline }}</b-td>
              <td>
                <b-progress height="5px">
                  <b-progress-bar :variant="item.progress.variant" :value="item.progress.data" />
                </b-progress>
              </td>
            </b-tr>
          </b-tbody>
        </b-table-simple>
      </simplebar>
    </b-card-body>
  </b-card>
</template>

<script setup lang="ts">
import simplebar from 'simplebar-vue'
import { recentProjectsSummaryTableData } from '@/views/widgets/components/data'
</script>
