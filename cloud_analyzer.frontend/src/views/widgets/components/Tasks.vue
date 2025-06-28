<template>
  <b-card no-body>
    <b-card-header class="d-flex justify-content-between align-items-center">
      <b-card-title tag="h4">My Tasks</b-card-title>
      <div>
        <a href="#!" class="btn btn-sm btn-primary"> <i class="bx bx-plus me-1"></i>Create Task </a>
      </div>
    </b-card-header>
    <b-card-body class="p-0 pb-3 ps-2">
      <simplebar class="p-3" data-simplebar style="max-height: 386px">
        <b-form-group class="form-todo">
          <div v-for="(option, idx) in options" :key="option.value"
               :class="{ 'my-3': idx !== 0 && idx !== options.length - 1 }">
            <b-form-checkbox size="md" v-model="selected" :value="option.value" class="rounded-circle mt-0 fs-14">
              {{ option.text }}
            </b-form-checkbox>
          </div>
        </b-form-group>
      </simplebar>
    </b-card-body>
  </b-card>
</template>

<script setup lang="ts">
import simplebar from 'simplebar-vue'
import {ref} from 'vue'

const selected = ref(['2', '9'])

const options = [
  {text: 'Review system logs for any reported errors', value: '1'},
  {text: 'Conduct user testing to identify potential bugs', value: '2'},
  {text: 'Gather feedback from stakeholders', value: '3'},
  {text: 'Prioritize bugs based on severity and impact', value: '4'},
  {text: 'Investigate and analyze the root cause of each bug', value: '5'},
  {text: 'Develop and implement fixes for the identified bugs', value: '6'},
  {text: 'Complete any recurring tasks', value: '7'},
  {text: 'Check emails and respond', value: '8'},
  {text: 'Review schedule for the day', value: '9'},
  {text: 'Daily stand-up meeting', value: '10'}
]
</script>
