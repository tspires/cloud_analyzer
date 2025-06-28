<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="9">

          <UIComponentCard title="Checkbox" id="checkbox-basic">
            <b-form-group class="mt-3">
              <b-form-checkbox>Check this custom checkbox</b-form-checkbox>
              <b-form-checkbox>Check this custom checkbox</b-form-checkbox>
            </b-form-group>
          </UIComponentCard>

          <UIComponentCard title="Inline Checkbox" id="inline-checkbox">
            <b-form-group class="mt-3">
              <b-form-checkbox inline>Check this custom checkbox</b-form-checkbox>
              <b-form-checkbox inline>Check this custom checkbox</b-form-checkbox>
            </b-form-group>
          </UIComponentCard>

          <UIComponentCard title="Disabled Checkbox" id="disabled-checkbox">
            <b-form-group class="mt-3">
              <b-form-checkbox v-model="checked" inline disabled>Check this custom checkbox</b-form-checkbox>
              <b-form-checkbox inline disabled>Check this custom checkbox</b-form-checkbox>
            </b-form-group>
          </UIComponentCard>

          <UIComponentCard title="Colors Checkbox" id="colors-checkbox">
            <div class="mt-3">
              <b-form-checkbox id="customCheckcolor1" class="mb-2" checked> Default Checkbox </b-form-checkbox>
              <b-form-checkbox id="customCheckcolor2" class="form-checkbox-success mb-2" checked> Success Checkbox </b-form-checkbox>
              <b-form-checkbox id="customCheckcolor3" class="form-checkbox-info mb-2" checked> Info Checkbox </b-form-checkbox>
              <b-form-checkbox id="customCheckcolor6" class="form-checkbox-secondary mb-2" checked> Secondary Checkbox </b-form-checkbox>
              <b-form-checkbox id="customCheckcolor4" class="form-checkbox-warning mb-2" checked> Warning Checkbox </b-form-checkbox>
              <b-form-checkbox id="customCheckcolor5" class="form-checkbox-danger mb-2" checked> Danger Checkbox </b-form-checkbox>
              <b-form-checkbox id="customCheckcolor7" class="form-checkbox-dark" checked> Dark Checkbox </b-form-checkbox>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Radio" id="radio-basic">
            <b-form-group class="mt-3">
              <b-form-radio name="radioDefault" value="1">Default radio</b-form-radio>
              <b-form-radio name="radioDefault" value="2">Default checked radio</b-form-radio>
            </b-form-group>
          </UIComponentCard>

          <UIComponentCard title="Inline Radio" id="inline-radio">
            <b-form-radio-group class="mt-3">
              <b-form-radio name="radio-inline" value="1">Check this custom checkbox</b-form-radio>
              <b-form-radio name="radio-inline" value="2">Check this custom checkbox</b-form-radio>
            </b-form-radio-group>
          </UIComponentCard>

          <UIComponentCard title="Disabled Radio" id="disabled-radio">
            <b-form-radio-group class="mt-3">
              <b-form-radio name="radio-disable" value="1" disabled>Check this custom checkbox</b-form-radio>
              <b-form-radio name="radio-disable" value="2" disabled>Check this custom checkbox</b-form-radio>
            </b-form-radio-group>
          </UIComponentCard>

          <UIComponentCard title="Colors Radio" id="colors-radio">
            <div class="mt-3">
              <div class="mb-2">
                <b-form-radio id="customRadiocolor1" checked> Default Radio </b-form-radio>
              </div>
              <div class="form-radio-success mb-2">
                <b-form-radio id="customRadiocolor2" checked> Success Radio </b-form-radio>
              </div>
              <div class="form-radio-info mb-2">
                <b-form-radio id="customRadiocolor3" checked> Info Radio </b-form-radio>
              </div>
              <div class="form-radio-secondary mb-2">
                <b-form-radio id="customRadiocolor4" checked> Secondary Radio </b-form-radio>
              </div>
              <div class="form-radio-warning mb-2">
                <b-form-radio id="customRadiocolor5" checked> Warning Radio </b-form-radio>
              </div>
              <div class="form-radio-danger mb-2">
                <b-form-radio id="customRadiocolor6" checked> Danger Radio </b-form-radio>
              </div>
              <div class="form-radio-dark">
                <b-form-radio id="customRadiocolor7" checked> Dark Radio </b-form-radio>
              </div>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Switch" id="switch-basic">
            <b-form-group class="mt-3">
              <b-form-checkbox switch>Default switch checkbox input</b-form-checkbox>
              <b-form-checkbox switch v-model="checked">Checked switch checkbox input</b-form-checkbox>
              <b-form-checkbox switch disabled>Disabled switch checkbox input</b-form-checkbox>
              <b-form-checkbox switch v-model="checked" disabled>Disabled checked switch checkbox input
              </b-form-checkbox>
            </b-form-group>
          </UIComponentCard>

        </b-col>

        <b-col xl="3">
          <AnchorNavigation :elements="anchorNavigation"/>
        </b-col>
      </b-row>
  </VerticalLayout>
</template>

<script setup lang="ts">
import VerticalLayout from "@/layouts/VerticalLayout.vue";
import AnchorNavigation from '@/components/AnchorNavigation.vue'
import {ref} from 'vue'
import UIComponentCard from "@/components/UIComponentCard.vue";

const checked = ref(true)

const anchorNavigation = [
  {
    id: 'checkbox-basic',
    title: 'Checkbox'
  },
  {
    id: 'inline-checkbox',
    title: 'Inline Checkbox'
  },
  {
    id: 'disabled-checkbox',
    title: 'Disabled Checkbox'
  },
  {
    id: 'colors-checkbox',
    title: 'Colors Checkbox'
  },
  {
    id: 'radio-basic',
    title: 'Radio'
  },
  {
    id: 'inline-radio',
    title: 'Inline Radio'
  },
  {
    id: 'disabled-radio',
    title: 'Disabled Radio'
  },
  {
    id: 'colors-radio',
    title: 'Colors Radio'
  },
  {
    id: 'switch-basic',
    title: 'Switch'
  }
]
</script>
