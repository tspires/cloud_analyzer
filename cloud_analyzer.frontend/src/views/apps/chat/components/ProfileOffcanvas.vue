<template>
  <simplebar class="p-0 h-100" data-simplebar>
    <div class="p-3">
      <div class="text-center">
        <img :src="avatar4" alt="shreyu" class="img-thumbnail avatar-lg rounded-circle mb-1" />
        <h4>Gilbert Chicoine</h4>
        <b-button variant="primary" size="sm" class="mt-1"> <i class="bi bi-envelope me-1"></i>Send Email </b-button>
        <p class="text-muted mt-2 fs-14">
          Last Interacted:
          <strong class="text-success">Online</strong>
        </p>
      </div>

      <div class="mt-3">
        <hr />

        <p class="mt-3 mb-1">
          <strong><i class="bi bi-phone"></i>Phone Number:</strong>
        </p>
        <p>+1 456 9595 9594</p>

        <p class="mt-3 mb-1">
          <strong><i class="bi bi-geo-alt"></i>Location:</strong>
        </p>
        <p>California, USA</p>

        <p class="mt-3 mb-1">
          <strong><i class="bi bi-globe"></i>Languages:</strong>
        </p>
        <p>English, German, Spanish</p>

        <p class="mt-3 mb-2">
          <strong><i class="bi bi-people"></i>Groups:</strong>
        </p>
        <p class="mb-0">
          <b-badge :variant="null" class="badge-soft-success p-1 fs-14 me-1">Work</b-badge>
          <b-badge :variant="null" class="badge-soft-primary p-1 fs-14">Friends</b-badge>
        </p>
      </div>

      <h5 class="mt-3">
        <a href="javascript:void(0);" class="my-0">
          <span class="float-end">See All</span>
          Shared Photoes
        </a>
      </h5>
      <b-row class="gx-1 pt-2">
        <b-col cols="4">
          <a href="javascript:void(0);">
            <img :src="smallImg1" alt="img-1" class="img-fluid rounded" />
          </a>
        </b-col>
        <b-col cols="4">
          <a href="javascript:void(0);">
            <img :src="smallImg2" alt="img-2" class="img-fluid rounded" />
          </a>
        </b-col>
        <b-col cols="4">
          <div class="position-relative overflow-hidden rounded">
            <a href="javascript:void(0);">
              <img :src="smallImg3" alt="img-3" class="img-fluid rounded" />
              <div class="bg-overlay bg-dark"></div>
              <h3 class="position-absolute top-50 start-50 translate-middle my-0 text-white">+3</h3>
            </a>
          </div>
        </b-col>
      </b-row>
    </div>
  </simplebar>
</template>

<script setup lang="ts">
import simplebar from 'simplebar-vue'

import smallImg1 from '@/assets/images/small/img-1.jpg'
import smallImg2 from '@/assets/images/small/img-2.jpg'
import smallImg3 from '@/assets/images/small/img-3.jpg'
import avatar4 from '@/assets/images/users/avatar-4.jpg'
</script>
