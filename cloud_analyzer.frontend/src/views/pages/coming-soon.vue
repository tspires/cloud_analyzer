<template>
     <AuthLayout>
          <b-row class="justify-content-center">
               <b-col lg="8">
                    <b-card no-body class="auth-card text-center">
                         <b-card-body>
                              <LogoBox customClass="mx-auto my-5 text-center" :smLogoHeight="30" :logoHeight="24" smLogoClass="me-1" />
                              <h2 class="fw-bold text-uppercase">We Are Launching Soon...</h2>
                              <p class="lead mt-3 w-75 mx-auto pb-4 fst-italic">Exciting news is on the
                                   horizon! We're thrilled to announce that something incredible is coming
                                   your way very soon.</p>
                              <b-row class="my-5">
                                   <b-col>
                                        <h3 id="days" class="fw-bold fs-60">{{ days }}</h3>
                                        <p class="text-uppercase fw-semibold">Days</p>
                                   </b-col>
                                   <b-col>
                                        <h3 id="hours" class="fw-bold fs-60">{{ hours }}</h3>
                                        <p class="text-uppercase fw-semibold">Hours</p>
                                   </b-col>
                                   <b-col>
                                        <h3 id="minutes" class="fw-bold fs-60">{{ minutes }}</h3>
                                        <p class="text-uppercase fw-semibold">Minutes</p>
                                   </b-col>
                                   <b-col>
                                        <h3 id="seconds" class="fw-bold fs-60">{{ seconds }}</h3>
                                        <p class="text-uppercase fw-semibold">Seconds</p>
                                   </b-col>
                              </b-row>
                         </b-card-body>
                    </b-card>
               </b-col>
          </b-row>
     </AuthLayout>
</template>
<script setup lang="ts">
import { ref, onMounted } from "vue";
import AuthLayout from '@/layouts/AuthLayout.vue';

import LogoBox from '@/components/LogoBox.vue';

const currentDate = new Date();
const countDown = currentDate.setDate(currentDate.getDate() + 5);
const timeRemaining = ref(countDown - currentDate.getTime());

const updateCountdown = () => {
     timeRemaining.value = countDown - new Date().getTime();
};

const days = ref(0);
const hours = ref(0);
const minutes = ref(0);
const seconds = ref(0);

const calculateTime = () => {
     days.value = Math.floor(timeRemaining.value / (1000 * 60 * 60 * 24));
     hours.value = Math.floor((timeRemaining.value % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
     minutes.value = Math.floor((timeRemaining.value % (1000 * 60 * 60)) / (1000 * 60));
     seconds.value = Math.floor((timeRemaining.value % (1000 * 60)) / 1000);
};

onMounted(() => {
     const intervalId = setInterval(() => {
          updateCountdown();
          calculateTime();
     }, 1000);

     return () => clearInterval(intervalId);
});
</script>