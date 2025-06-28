<template>
  <VerticalLayout>
    <b-row>
      <b-col xl="9">
        <UIComponentCard title="Default Buttons" id="default">
          <div class="button-list mt-3">
            <a class="btn btn-primary" @click="defaultOffcanvas = !defaultOffcanvas"> Link with href </a>
            <b-button variant="secondary" type="button" @click="defaultOffcanvas = !defaultOffcanvas"> Button with
              data-bs-target
            </b-button>
          </div>
        </UIComponentCard>

        <UIComponentCard title="Static Backdrop" id="static-backdrop">
          <div class="button-list mt-3">
            <b-button variant="primary" type="button" @click="offcanvasScrolling = !offcanvasScrolling"> Enable Body
              Scrolling
            </b-button>
            <b-button variant="secondary" type="button" @click="offcanvasBackdrop = !offcanvasBackdrop"> Enable
              Backdrop (Default)
            </b-button>
            <b-button variant="success" type="button" @click="offcanvasScrollingBackdrop = !offcanvasScrollingBackdrop">
              Enable Both Scrolling & Backdrop
            </b-button>
          </div>
        </UIComponentCard>

        <UIComponentCard title="Offcanvas Position" id="offcanvas-position">
          <div class="button-list mt-3">
            <b-button variant="primary" type="button" @click="offcanvasStart = !offcanvasStart"> Left Offcanvas</b-button>
            <b-button variant="secondary" type="button" @click="offcanvasEnd = !offcanvasEnd"> Right Offcanvas</b-button>
            <b-button variant="success" type="button" @click="offcanvasTop = !offcanvasTop"> Top Offcanvas</b-button>
            <b-button variant="info" type="button" @click="offcanvasBottom = !offcanvasBottom"> Bottom Offcanvas</b-button>
          </div>
        </UIComponentCard>
      </b-col>

      <b-col xl="3">
        <AnchorNavigation :elements="anchorNavigation" />
      </b-col>
    </b-row>

    <!-- Default offcanvas -->
    <b-offcanvas v-model="defaultOffcanvas" placement="start" title="Offcanvas" title-class="mt-0"
      id="offcanvasExample">
      <p>Some text as placeholder. In real life you can have the elements you have chosen. Like, text, images, lists,
        etc.</p>

      <b-dropdown variant="primary" class="mt-3" text="Dropdown button">
        <b-dropdown-item>Action</b-dropdown-item>
        <b-dropdown-item>Another action</b-dropdown-item>
        <b-dropdown-item>Something else here</b-dropdown-item>
      </b-dropdown>
    </b-offcanvas>

    <!-- Scrolling offcanvas -->
    <b-offcanvas v-model="offcanvasScrolling" placement="start" title="Offcanvas" title-class="mt-0"
      id="offcanvasExample" :backdrop="false" :bodyScrolling="true">
      <p>Some text as placeholder. In real life you can have the elements you have chosen. Like, text, images, lists,
        etc.</p>
      <b-dropdown variant="primary" class="mt-3" text="Dropdown button">
        <b-dropdown-item>Action</b-dropdown-item>
        <b-dropdown-item>Another action</b-dropdown-item>
        <b-dropdown-item>Something else here</b-dropdown-item>
      </b-dropdown>
    </b-offcanvas>

    <!-- Backdrop offcanvas -->
    <b-offcanvas v-model="offcanvasBackdrop" placement="start" title="Offcanvas" title-class="mt-0"
      id="offcanvasExample">
      <p>Some text as placeholder. In real life you can have the elements you have chosen. Like, text, images, lists,
        etc.</p>
      <b-dropdown variant="primary" class="mt-3" text="Dropdown button">
        <b-dropdown-item>Action</b-dropdown-item>
        <b-dropdown-item>Another action</b-dropdown-item>
        <b-dropdown-item>Something else here</b-dropdown-item>
      </b-dropdown>
    </b-offcanvas>

    <!-- scrolling & Backdrop offcanvas -->
    <b-offcanvas v-model="offcanvasScrollingBackdrop" placement="start" title="Offcanvas" title-class="mt-0"
      id="offcanvasExample" :bodyScrolling="true">
      <p>Some text as placeholder. In real life you can have the elements you have chosen. Like, text, images, lists,
        etc.</p>
      <b-dropdown variant="primary" class="mt-3" text="Dropdown button">
        <b-dropdown-item>Action</b-dropdown-item>
        <b-dropdown-item>Another action</b-dropdown-item>
        <b-dropdown-item>Something else here</b-dropdown-item>
      </b-dropdown>
    </b-offcanvas>

    <!-- Left offcanvas -->
    <b-offcanvas v-model="offcanvasStart" placement="start" title="Offcanvas" title-class="mt-0" id="offcanvasExample">
      <p>Some text as placeholder. In real life you can have the elements you have chosen. Like, text, images, lists,
        etc.</p>
      <b-dropdown variant="primary" class="mt-3" text="Dropdown button">
        <b-dropdown-item>Action</b-dropdown-item>
        <b-dropdown-item>Another action</b-dropdown-item>
        <b-dropdown-item>Something else here</b-dropdown-item>
      </b-dropdown>
    </b-offcanvas>

    <!-- Right offcanvas -->
    <b-offcanvas v-model="offcanvasEnd" placement="end" title="Offcanvas" title-class="mt-0" id="offcanvasExample">
      <p>Some text as placeholder. In real life you can have the elements you have chosen. Like, text, images, lists,
        etc.</p>
      <b-dropdown variant="primary" class="mt-3" text="Dropdown button">
        <b-dropdown-item>Action</b-dropdown-item>
        <b-dropdown-item>Another action</b-dropdown-item>
        <b-dropdown-item>Something else here</b-dropdown-item>
      </b-dropdown>
    </b-offcanvas>

    <!-- Top offcanvas -->
    <b-offcanvas v-model="offcanvasTop" placement="top" title="Offcanvas" title-class="mt-0" id="offcanvasExample">
      <p>Some text as placeholder. In real life you can have the elements you have chosen. Like, text, images, lists,
        etc.</p>
      <b-dropdown variant="primary" class="mt-3" text="Dropdown button">
        <b-dropdown-item>Action</b-dropdown-item>
        <b-dropdown-item>Another action</b-dropdown-item>
        <b-dropdown-item>Something else here</b-dropdown-item>
      </b-dropdown>
    </b-offcanvas>

    <!-- Bottom offcanvas -->
    <b-offcanvas v-model="offcanvasBottom" placement="bottom" title="Offcanvas" title-class="mt-0"
      id="offcanvasExample">
      <p>Some text as placeholder. In real life you can have the elements you have chosen. Like, text, images, lists,
        etc.</p>
      <b-dropdown variant="primary" class="mt-3" text="Dropdown button">
        <b-dropdown-item>Action</b-dropdown-item>
        <b-dropdown-item>Another action</b-dropdown-item>
        <b-dropdown-item>Something else here</b-dropdown-item>
      </b-dropdown>
    </b-offcanvas>
  </VerticalLayout>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import VerticalLayout from "@/layouts/VerticalLayout.vue";

import AnchorNavigation from '@/components/AnchorNavigation.vue';
import UIComponentCard from '@/components/UIComponentCard.vue';

const defaultOffcanvas = ref(false);
const offcanvasEnd = ref(false);
const offcanvasStart = ref(false);
const offcanvasTop = ref(false);
const offcanvasBottom = ref(false);

const offcanvasScrolling = ref(false);
const offcanvasBackdrop = ref(false);
const offcanvasScrollingBackdrop = ref(false);

const anchorNavigation = [
  {
    id: 'default',
    title: 'Default Buttons'
  },
  {
    id: 'static-backdrop',
    title: 'Static Backdrop'
  },
  {
    id: 'offcanvas-position',
    title: 'Offcanvas Position'
  }
];
</script>
