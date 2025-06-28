<template>
  <b-card no-body>
    <b-card-header class="d-flex justify-content-between align-items-center">
      <b-card-title tag="h4"> Friends Request (10) </b-card-title>
    </b-card-header>

    <b-card-body class="p-0 pb-3">
      <simplebar class="p-3 pb-0" data-simplebar style="max-height: 400px">
        <div v-for="(friend, idx) in friendRequests" :key="idx" class="d-flex align-items-center" :class="{ 'mb-3': idx !== friendRequests.length - 1 }">
          <div class="flex-shrink-0">
            <img :src="friend.avatar" class="img-fluid avatar-sm rounded me-2" alt="avatar-5" />
          </div>
          <div class="flex-grow-1">
            <h5 class="mb-1 fs-14">
              <a href="#!">{{ friend.name }}</a>
            </h5>
            <p v-if="friend.mutualFriends === 0" class="mb-0">no mutual friends</p>
            <p v-else class="mb-0">{{ friend.mutualFriends }} mutual friends</p>
          </div>

          <DropDown>
            <a href="javascript:void(0);" class="dropdown-toggle arrow-none text-dark" data-bs-toggle="dropdown" aria-expanded="false">
              <i class="bx bx-dots-vertical-rounded fs-18"></i>
            </a>
            <div class="dropdown-menu dropdown-menu-end">
              <a href="javascript:void(0);" class="dropdown-item"> <i class="bx bxs-user-detail me-1"></i>See Profile </a>
              <a href="javascript:void(0);" class="dropdown-item"> <i class="bx bxl-telegram me-1"></i>Message to Victoria </a>
              <a href="javascript:void(0);" class="dropdown-item"> <i class="bx bx-user-x me-1"></i>Unfriend Victoria </a>
              <a href="javascript:void(0);" class="dropdown-item"> <i class="bx bx-block me-1"></i>Block Victoria </a>
            </div>
          </DropDown>
        </div>
      </simplebar>
    </b-card-body>
  </b-card>
</template>

<script setup lang="ts">
import simplebar from 'simplebar-vue'
import DropDown from '@/components/DropDown.vue'
import { friendRequests } from '@/views/widgets/components/data'
</script>
