<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="9">
          <UIComponentCard id="basic" title="Basic">
            <b-row>
              <b-col lg="6">
                <FlatPicker id="basic-datepicker" placeholder="Basic datepicker" v-model="basic" />
              </b-col>
            </b-row>
          </UIComponentCard>

          <UIComponentCard id="datetime" title="DateTime">
            <b-row>
              <b-col lg="6">
                <FlatPicker id="datetime-datepicker" placeholder="Date and Time"
                  :options="{ enableTime: true, dateFormat: 'Y-m-d H:i' }" />
              </b-col>
            </b-row>
          </UIComponentCard>

          <UIComponentCard id="human-friendly-dates" title="Human-friendly Dates">
            <b-row>
              <b-col lg="6">
                <FlatPicker id="humanfd-datepicker" placeholder="October 9, 2018"
                  :options="{ altInput: true, altFormat: 'F j, Y', dateFormat: 'Y-m-d' }" />
              </b-col>
            </b-row>
          </UIComponentCard>

          <UIComponentCard id="minmax" title="MinDate and MaxDate">
            <b-row>
              <b-col lg="6">
                <FlatPicker id="minmax-datepicker" placeholder="mindate - maxdate"
                  :options="{ minDate: '2020-01', maxDate: '2020-03' }" />
              </b-col>
            </b-row>
          </UIComponentCard>

          <UIComponentCard id="disable" title="Disabling dates">
            <b-row>
              <b-col lg="6">
                <FlatPicker id="disable-datepicker" placeholder="Disabling dates" :options="{
                  disable: ['2025-01-10', '2025-01-21', '2025-01-30', new Date(2025, 4, 9)],
                  dateFormat: 'Y-m-d'
                }" />
              </b-col>
            </b-row>
          </UIComponentCard>

          <UIComponentCard id="multiple" title="Selecting multiple dates">
            <b-row>
              <b-col lg="6">
                <FlatPicker id="multiple-datepicker" placeholder="Multiple dates"
                  :options="{ mode: 'multiple', dateFormat: 'Y-m-d' }" />
              </b-col>
            </b-row>
          </UIComponentCard>

          <UIComponentCard id="conjunction" title="Selecting multiple dates - Conjunction">
            <b-row>
              <b-col lg="6">
                <FlatPicker id="conjunction-datepicker" placeholder="2018-10-10 :: 2018-10-11"
                  :options="{ mode: 'multiple', dateFormat: 'Y-m-d', conjunction: ' :: ' }" />
              </b-col>
            </b-row>
          </UIComponentCard>

          <UIComponentCard id="range-calendar" title="Range Calendar">
            <b-row>
              <b-col lg="6">
                <FlatPicker id="range-datepicker" placeholder="2018-10-03 to 2018-10-10" :options="{ mode: 'range' }" />
              </b-col>
            </b-row>
          </UIComponentCard>

          <UIComponentCard id="inline-calendar" title="Inline Calendar">
            <b-row>
              <b-col lg="6">
                <FlatPicker id="inline-datepicker" placeholder="Inline calendar" :options="{ inline: true }" />
              </b-col>
            </b-row>
          </UIComponentCard>

          <UIComponentCard id="timepicker-basic" title="Basic Timepicker">
            <b-row>
              <b-col lg="6">
                <FlatPicker id="basic-timepicker" placeholder="Basic timepicker"
                  :options="{ enableTime: true, noCalendar: true, dateFormat: 'H:i' }" />
              </b-col>
            </b-row>
          </UIComponentCard>

          <UIComponentCard id="24hours" title="24-hour Time Picker">
            <b-row>
              <b-col lg="6">
                <FlatPicker id="24hours-timepicker" placeholder="16:21"
                  :options="{ enableTime: true, noCalendar: true, dateFormat: 'H:i', time_24hr: true }" />
              </b-col>
            </b-row>
          </UIComponentCard>

          <UIComponentCard id="timepicker-minmax" title="Time Picker w/ Limits">
            <b-row>
              <b-col lg="6">
                <FlatPicker id="minmax-timepicker" placeholder="Limits"
                  :options="{ enableTime: true, noCalendar: true, dateFormat: 'H:i', minDate: '16:00', maxDate: '22:30' }" />
              </b-col>
            </b-row>
          </UIComponentCard>

          <UIComponentCard id="preloading-time" title="Preloading Time">
            <b-row>
              <b-col lg="6">
                <FlatPicker id="preloading-timepicker" placeholder="Pick a time"
                  :options="{ enableTime: true, noCalendar: true, dateFormat: 'H:i', defaultDate: '01:45' }" />
              </b-col>
            </b-row>
          </UIComponentCard>
        </b-col>

        <b-col xl="3">
          <AnchorNavigation :elements="anchorNavigation" />
        </b-col>
      </b-row>
  </VerticalLayout>
</template>

<script setup lang="ts">
import VerticalLayout from "@/layouts/VerticalLayout.vue";
import UIComponentCard from "@/components/UIComponentCard.vue";
import FlatPicker from '@/components/FlatPicker.vue';
import AnchorNavigation from '@/components/AnchorNavigation.vue';
import { ref } from "vue";

const anchorNavigation = [
  {
    id: 'basic',
    title: 'Basic'
  },
  {
    id: 'datetime',
    title: 'DateTime'
  },
  {
    id: 'human-friendly-dates',
    title: 'Human-friendly Dates'
  },
  {
    id: 'minmax',
    title: 'MinDate and MaxDate'
  },
  {
    id: 'disable',
    title: 'Disabling dates'
  },
  {
    id: 'multiple',
    title: 'Selecting multiple dates'
  },
  {
    id: 'conjunction',
    title: 'Selecting multiple dates - Conjunction'
  },
  {
    id: 'range-calendar',
    title: 'Range Calendar'
  },
  {
    id: 'inline-calendar',
    title: 'Inline Calendar'
  },
  {
    id: 'timepicker-basic',
    title: 'Basic Timepicker'
  },
  {
    id: '24hours',
    title: '24-hour Time Picker'
  },
  {
    id: 'timepicker-minmax',
    title: 'Time Picker w/ Limits'
  },
  {
    id: 'preloading-time',
    title: 'Preloading Time'
  }
];

const basic = ref();
</script>
