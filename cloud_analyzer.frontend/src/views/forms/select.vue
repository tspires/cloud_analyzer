<template>
  <VerticalLayout>
    <b-row>
      <b-col xl="9">
        <UIComponentCard title="Basic Example" id="basic">
          <b-row>
            <b-col lg="6">
              <b-form-group>
                <ChoicesSelect id="choices-single-default" v-model="basicSelected" :options="options1"
                  class="form-control" />
              </b-form-group>
            </b-col>
          </b-row>
        </UIComponentCard>

        <UIComponentCard title="Option Groups Example" id="options-group">
          <b-row>
            <b-col lg="6">
              <b-form-group>
                <ChoicesSelect id="choices-single-groups" label="Option Groups" class="form-control"
                  v-model="optionGrpSelected">
                  <option value="">Choose a city</option>
                  <optgroup label="UK">
                    <option value="London">London</option>
                    <option value="Manchester">Manchester</option>
                    <option value="Liverpool">Liverpool</option>
                  </optgroup>
                  <optgroup label="FR">
                    <option value="Paris">Paris</option>
                    <option value="Lyon">Lyon</option>
                    <option value="Marseille">Marseille</option>
                  </optgroup>
                  <optgroup label="DE" disabled>
                    <option value="Hamburg">Hamburg</option>
                    <option value="Munich">Munich</option>
                    <option value="Berlin">Berlin</option>
                  </optgroup>
                  <optgroup label="US">
                    <option value="New York">New York</option>
                    <option value="Washington" disabled>Washington</option>
                    <option value="Michigan">Michigan</option>
                  </optgroup>
                  <optgroup label="SP">
                    <option value="Madrid">Madrid</option>
                    <option value="Barcelona">Barcelona</option>
                    <option value="Malaga">Malaga</option>
                  </optgroup>
                  <optgroup label="CA">
                    <option value="Montreal">Montreal</option>
                    <option value="Toronto">Toronto</option>
                    <option value="Vancouver">Vancouver</option>
                  </optgroup>
                </ChoicesSelect>
              </b-form-group>
            </b-col>
          </b-row>
        </UIComponentCard>

        <UIComponentCard title="Options added via config with no search" id="options-add-no-search">
          <b-row>
            <b-col lg="6">
              <b-form-group>
                <ChoicesSelect id="choices-single-no-search" v-model="noSearchSelected" :options="options2"
                  :choice-options="{ searchEnabled: false }" class="form-control" />
              </b-form-group>
            </b-col>
          </b-row>
        </UIComponentCard>

        <UIComponentCard title="Options added via config with no sorting" id="options-add-no-sorting">
          <b-row>
            <b-col lg="6">
              <b-form-group>
                <ChoicesSelect id="choices-single-no-sorting" v-model="noSortingSelected" :options="options3"
                  :choice-options="{ shouldSort: false, shouldSortItems: false }" class="form-control" />
              </b-form-group>
            </b-col>
          </b-row>
        </UIComponentCard>

        <UIComponentCard title="Multiple select input" id="multiple-select">
          <b-row>
            <b-col lg="6">
              <b-form-group>
                <ChoicesSelect id="choices-multiple-default" v-model="multipleSelected" :options="options4"
                  class="form-control" multiple />
              </b-form-group>
            </b-col>
          </b-row>
        </UIComponentCard>

        <UIComponentCard title="Multiple select input" id="multiple-select-remove">
          <b-row>
            <b-col lg="6">
              <b-form-group>
                <ChoicesSelect id="choices-multiple-remove-button" v-model="multipleWithRemoveSelected"
                  :options="options4" :choice-options="{ removeItemButton: true }" class="form-control" multiple />
              </b-form-group>
            </b-col>
          </b-row>
        </UIComponentCard>

        <UIComponentCard title="Multiple select With Option groups" id="multiple-groups">
          <b-row>
            <b-col lg="6">
              <b-form-group>
                <ChoicesSelect id="choices-multiple-groups" v-model="multipleWithOptionGrpSelected" class="form-control"
                  multiple>
                  <optgroup label="UK">
                    <option value="London">London</option>
                    <option value="Manchester">Manchester</option>
                    <option value="Liverpool">Liverpool</option>
                  </optgroup>
                  <optgroup label="FR">
                    <option value="Paris">Paris</option>
                    <option value="Lyon">Lyon</option>
                    <option value="Marseille">Marseille</option>
                  </optgroup>
                  <optgroup label="DE" disabled>
                    <option value="Hamburg">Hamburg</option>
                    <option value="Munich">Munich</option>
                    <option value="Berlin">Berlin</option>
                  </optgroup>
                  <optgroup label="US">
                    <option value="New York">New York</option>
                    <option value="Washington" disabled>Washington</option>
                    <option value="Michigan">Michigan</option>
                  </optgroup>
                  <optgroup label="SP">
                    <option value="Madrid">Madrid</option>
                    <option value="Barcelona">Barcelona</option>
                    <option value="Malaga">Malaga</option>
                  </optgroup>
                  <optgroup label="CA">
                    <option value="Montreal">Montreal</option>
                    <option value="Toronto">Toronto</option>
                    <option value="Vancouver">Vancouver</option>
                  </optgroup>
                </ChoicesSelect>
              </b-form-group>
            </b-col>
          </b-row>
        </UIComponentCard>

        <UIComponentCard title="Text inputs" id="text-input">
          <b-row>
            <b-col lg="6">
              <b-form-group>
                <ChoicesInput id="choices-text-remove-button" label="Set limit values with remove button"
                  class="form-control" :choice-options="{ removeItemButton: true, maxItemCount: 3 }" />
              </b-form-group>
            </b-col>
          </b-row>
        </UIComponentCard>

        <UIComponentCard title="Text inputs in Unique values only, no pasting" id="unique-values">
          <b-row>
            <b-col lg="6">
              <b-form-group>
                <ChoicesInput id="choices-text-unique-values" label="Unique values only, no pasting"
                  class="form-control" value="Project-A, Project-B"
                  :choice-options="{ duplicateItemsAllowed: false, paste: false }" />
              </b-form-group>
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
import AnchorNavigation from '@/components/AnchorNavigation.vue';
import ChoicesInput from '@/components/ChoicesInput.vue';
import ChoicesSelect from '@/components/ChoicesSelect.vue';
import { ref } from 'vue';
import VerticalLayout from "@/layouts/VerticalLayout.vue";
import UIComponentCard from "@/components/UIComponentCard.vue";

const anchorNavigation = [
  {
    id: 'basic',
    title: 'Basic Example'
  },
  {
    id: 'options-group',
    title: 'Option Groups Example'
  },
  {
    id: 'options-add-no-search',
    title: 'Options added via config with no search'
  },
  {
    id: 'options-add-no-sorting',
    title: 'Options added via config with no sorting'
  },
  {
    id: 'multiple-select',
    title: 'Multiple select input'
  },
  {
    id: 'multiple-select-remove',
    title: 'Multiple select With remove button input '
  },
  {
    id: 'multiple-groups',
    title: 'Multiple select With Option groups '
  },
  {
    id: 'text-input',
    title: 'Text inputs'
  },
  {
    id: 'unique-values',
    title: 'Text inputs in Unique values only, no pasting'
  }
];

const basicSelected = ref('');
const optionGrpSelected = ref('');
const noSearchSelected = ref('Zero');
const noSortingSelected = ref('Madrid');
const multipleSelected = ref('choice-1');
const multipleWithRemoveSelected = ref('choice-3');
const multipleWithOptionGrpSelected = ref('');

const options1 = [
  { value: '', text: 'This is a placeholder' },
  { value: 'choice-1', text: 'Choice 1' },
  { value: 'choice-2', text: 'Choice 2' },
  { value: 'choice-3', text: 'Choice 3' },
  { value: 'choice-4', text: 'Choice 4' }
];

const options2 = [
  { value: 'Zero', text: 'Zero' },
  { value: 'One', text: 'One' },
  { value: 'Two', text: 'Two' },
  { value: 'Three', text: 'Three' },
  { value: 'Four', text: 'Four' },
  { value: 'Five', text: 'Five' },
  { value: 'Six', text: 'Six' }
];

const options3 = [
  { value: 'Madrid', text: 'Madrid' },
  { value: 'Toronto', text: 'Toronto' },
  { value: 'Vancouver', text: 'Vancouver' },
  { value: 'London', text: 'London' },
  { value: 'Manchester', text: 'Manchester' },
  { value: 'Liverpool', text: 'Liverpool' },
  { value: 'Paris', text: 'Paris' },
  { value: 'Malaga', text: 'Malaga' },
  { value: 'Washington', text: 'Washington' },
  { value: 'Lyon', text: 'Lyon' },
  { value: 'Marseille', text: 'Marseille' },
  { value: 'Hamburg', text: 'Hamburg' },
  { value: 'Munich', text: 'Munich' },
  { value: 'Madrid', text: 'Madrid' },
  { value: 'Barcelona', text: 'Barcelona' },
  { value: 'Berlin', text: 'Berlin' },
  { value: 'Montreal', text: 'Montreal' },
  { value: 'New York', text: 'New York' },
  { value: 'Michigan', text: 'Michigan' }
];

const options4 = [
  { value: 'choice-1', text: 'Choice 1' },
  { value: 'choice-2', text: 'Choice 2' },
  { value: 'choice-3', text: 'Choice 3' },
  { value: 'choice-4', text: 'Choice 4' }
];
</script>
