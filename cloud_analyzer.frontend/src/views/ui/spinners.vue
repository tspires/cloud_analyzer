<template>
  <VerticalLayout>
    <b-row>
      <b-col xl="9">
        <UIComponentCard title="Border Spinners" id="border_spinner"
          caption="Use the border spinners for a lightweight loading indicator.">
          <b-spinner variant="primary" />
        </UIComponentCard>

        <UIComponentCard title="Color Spinners" id="color_spinners"
          caption="You can use any of our text color utilities on the standard spinner.">
          <b-spinner variant="primary" class="me-3" />
          <b-spinner variant="secondary" class="me-3" />
          <b-spinner variant="success" class="me-3" />
          <b-spinner variant="info" class="me-3" />
          <b-spinner variant="warning" class="me-3" />
          <b-spinner variant="danger" class="me-3" />
        </UIComponentCard>

        <UIComponentCard title="Growing Spinners" id="growing_spinners"
          caption="If you don’t fancy a border spinner, switch to the grow spinner. While it doesn’t technically spin, it does repeatedly grow!">
          <b-spinner variant="primary" type="grow" />
        </UIComponentCard>

        <UIComponentCard title="Color Growing Spinners" id="color_growing"
          caption="You can use any of our text color utilities on the standard spinner.">
          <b-spinner variant="primary" type="grow" class="me-3" />
          <b-spinner variant="secondary" type="grow" class="me-3" />
          <b-spinner variant="success" type="grow" class="me-3" />
          <b-spinner variant="info" type="grow" class="me-3" />
          <b-spinner variant="warning" type="grow" class="me-3" />
          <b-spinner variant="danger" type="grow" class="me-3" />
        </UIComponentCard>

        <UIComponentCard title="Alignment" id="alignment"
          caption="Use flexbox utilities, float utilities, or text alignment utilities to place spinners exactly where you need them in any situation.">
          <div class="d-flex justify-content-center border p-2">
            <b-spinner variant="primary" type="grow" class="me-3" />
          </div>
        </UIComponentCard>

        <UIComponentCard title="Size" id="size">
          <div class="mt-3">
            <b-spinner variant="primary" class="me-3" small />
            <b-spinner variant="primary" type="grow" class="me-3" small />
            <b-spinner variant="primary" class="me-3" />
            <b-spinner variant="primary" type="grow" class="me-3" />
          </div>
        </UIComponentCard>

        <UIComponentCard title="Placement" id="placement"
          caption="Use <code>flexbox utilities</code>, <code>float utilities</code>, or <code>text alignment</code> utilities to place spinners exactly where you need them in any situation.">
          <div class="d-flex align-items-center border p-2">
            <strong>Loading...</strong>
            <b-spinner variant="primary" class="ms-auto" />
          </div>
        </UIComponentCard>

        <UIComponentCard title="Buttons Spinner" id="button_spinner"
          caption="Use spinners within buttons to indicate an action is currently processing or taking place. You may also swap the text out of the spinner element and utilize button text as needed.">
          <b-button variant="primary" class="me-1" disabled>
            <b-spinner small />
            Loading...
          </b-button>

          <b-button variant="primary" disabled>
            <b-spinner type="grow" small />
            Loading...
          </b-button>
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

import AnchorNavigation from '@/components/AnchorNavigation.vue';
import UIComponentCard from '@/components/UIComponentCard.vue';

const anchorNavigation = [
  {
    id: 'border_spinner',
    title: 'Border Spinner'
  },
  {
    id: 'color_spinners',
    title: 'Color Spinners'
  },
  {
    id: 'growing_spinners',
    title: 'Growing Spinners'
  },
  {
    id: 'color_growing',
    title: 'Color Growing Spinners'
  },
  {
    id: 'alignment',
    title: 'Alignment'
  },
  {
    id: 'size',
    title: 'Size'
  },
  {
    id: 'placement',
    title: 'Placement'
  },
  {
    id: 'button_spinner',
    title: 'Buttons Spinner'
  }
];
</script>
