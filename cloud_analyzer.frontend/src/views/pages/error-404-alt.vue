<template>
  <VerticalLayout>
    <b-row class="justify-content-center">
      <b-col xl="5">
        <b-card no-body>
          <b-card-body class="px-3 py-5">
            <div class="p-4">
              <div class="mx-auto mb-4 text-center">
                <h1 class="mb-3 fw-bold fs-60">404</h1>
                <h2 class="fs-22 lh-base">Page Not Found !</h2>
                <p class="text-muted mt-1 mb-4">The page you're trying to reach seems to have gone <br /> missing in the digital wilderness.</p>
                <div class="text-center">
                  <router-link to="/" class="btn btn-success">Back to Home</router-link>
                </div>
              </div>
            </div>
          </b-card-body>
        </b-card>
      </b-col>
    </b-row>
  </VerticalLayout>
</template>
<script setup lang="ts">
import VerticalLayout from '@/layouts/VerticalLayout.vue';
</script>