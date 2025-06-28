<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="9">

          <UIComponentCard title="Basic Example" id="basic">
            <div class="mt-3">
              <b-form-group label="Text" label-for="example-input" class="mb-3">
                <b-form-input type="text" id="example-input"/>
              </b-form-group>

              <b-form-group label="Email" label-for="example-email" class="mb-3">
                <b-form-input type="email" id="example-email"/>
              </b-form-group>

              <b-form-group label="Password" label-for="example-password" class="mb-3">
                <b-form-input type="password" id="example-password"/>
              </b-form-group>

              <b-form-group label="Placeholder" label-for="example-palaceholder" class="mb-3">
                <b-form-input type="text" id="example-palaceholder" placeholder="placeholder"/>
              </b-form-group>

              <b-form-group label="Text area" label-for="example-textarea">
                <b-form-textarea type="text" id="example-textarea" rows="5"/>
              </b-form-group>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Input Sizing" id="size">
            <div class="mt-3">
              <b-row>
                <b-col lg="6">
                  <div class="d-flex flex-column gap-2">
                    <b-form-input size="lg" type="text" placeholder="Lg"/>
                    <b-form-input size="md" type="text" placeholder="Md"/>
                    <b-form-input size="sm" type="text" placeholder="Sm"/>
                  </div>
                </b-col>
              </b-row>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Disabled Input" id="disabled">
            <div class="mt-3">
              <b-row>
                <b-col lg="6">
                  <div class="d-flex flex-column gap-2">
                    <b-form-input type="text" placeholder="Disabled input" disabled/>
                    <b-form-input type="text" placeholder="Disabled readonly input" disabled readonly/>
                  </div>
                </b-col>
              </b-row>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Readonly Input" id="readonly">
            <div class="mt-3">
              <b-row>
                <b-col lg="6">
                  <div class="d-flex flex-column gap-2">
                    <b-form-input type="text" placeholder="Readonly input here..." readonly/>
                    <input type="text" readonly class="form-control-plaintext" id="staticEmail"
                           value="email@example.com"/>
                  </div>
                </b-col>
              </b-row>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Datalists Input" id="datalists">
            <div class="mt-3">
              <b-row>
                <b-col lg="6">
                  <div>
                    <b-form-group label="Datalist example" label-for="exampleDataList">
                      <b-form-input list="datalistOptions" id="exampleDataList" placeholder="Type to search..."/>
                      <datalist id="datalistOptions">
                        <option value="San Francisco"></option>
                        <option value="New York"></option>
                        <option value="Seattle"></option>
                        <option value="Los Angeles"></option>
                        <option value="Chicago"></option>
                      </datalist>
                    </b-form-group>
                  </div>
                </b-col>
              </b-row>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Select" id="select">
            <b-row>
              <b-col lg="6">
                <div class="mt-3">
                  <b-form-group label="Default Input Select" label-for="example-select" class="mb-3">
                    <b-form-select id="example-select" v-model="selected" :options="options"/>
                  </b-form-group>

                  <p class="text-muted">The <code>multiple</code> attribute is also supported:</p>

                  <b-form-group label="Multiple Select" label-for="example-multiselect" class="mb-3">
                    <b-form-select id="example-multiselect" v-model="multipleSelected" :options="options" multiple/>
                  </b-form-group>

                  <p class="text-muted">As is the <code>size</code> attribute:</p>

                  <b-form-group label="Multiple Select Size" label-for="example-multiselectsize">
                    <b-form-select id="example-multiselectsize" v-model="multipleSelected" :options="options" multiple
                                   :select-size="3"/>
                  </b-form-group>
                </div>
              </b-col>
            </b-row>
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

const anchorNavigation = [
  {
    id: 'basic',
    title: 'Basic Example'
  },
  {
    id: 'size',
    title: 'Input Sizing'
  },
  {
    id: 'disabled',
    title: 'Disabled Input'
  },
  {
    id: 'readonly',
    title: 'Readonly Input'
  },
  {
    id: 'datalists',
    title: 'Datalists input'
  },
  {
    id: 'select',
    title: 'Select input'
  }
]

const selected = ref('1')
const multipleSelected = ref(['1', '3'])

const options = [
  {value: '1', text: 1},
  {value: '2', text: 2},
  {value: '3', text: 3},
  {value: '4', text: 4},
  {value: '5', text: 5}
]
</script>
