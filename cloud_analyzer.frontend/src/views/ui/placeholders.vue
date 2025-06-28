<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="9">
          <UIComponentCard title="Default" id="default"
                           caption="A progress bar can be used to show a user how far along he/she is in a process.">
            <b-row class="g-4">
              <b-col md="4">
                <b-card no-body>
                  <svg class="bd-placeholder-img card-img-top" width="100%" height="180"
                       xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Placeholder"
                       preserveAspectRatio="xMidYMid slice" focusable="false">
                    <title>Placeholder</title>
                    <rect width="100%" height="100%" fill="#20c997"></rect>
                  </svg>

                  <b-card-body>
                    <b-card-title tag="h5" class="mb-2"> Card title</b-card-title>
                    <p class="card-text">Some quick example text to build on the card title and make up the bulk of the
                      card's content.</p>
                    <a href="#" class="btn btn-primary">Go somewhere</a>
                  </b-card-body>
                </b-card>
              </b-col>

              <b-col md="4">
                <b-card no-body aria-hidden="true">
                  <svg class="bd-placeholder-img card-img-top" width="100%" height="180"
                       xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Placeholder"
                       preserveAspectRatio="xMidYMid slice" focusable="false">
                    <title>Placeholder</title>
                    <rect width="100%" height="100%" fill="#868e96"></rect>
                  </svg>

                  <b-card-body>
                    <div class="h5 card-title placeholder-glow">
                      <span class="placeholder col-6"></span>
                    </div>
                    <p class="card-text placeholder-glow">
                      <b-placeholder cols="7"/>
                      <b-placeholder cols="4"/>
                      <b-placeholder cols="4"/>
                      <b-placeholder cols="6"/>
                      <b-placeholder cols="8"/>
                    </p>
                    <b-placeholder-button cols="6"/>
                  </b-card-body>
                </b-card>
              </b-col>
            </b-row>
          </UIComponentCard>

          <UIComponentCard title="How it works" id="how-works"
                           caption="Create placeholders with the <code>.placeholder</code> class and a grid column class (e.g., <code>.col-6</code>) to set the <code>width</code>. They can replace the text inside an element or be added as a modifier class to an existing component.">
            <p aria-hidden="true">
              <b-placeholder cols="6"/>
            </p>

            <b-placeholder-button cols="4"/>
          </UIComponentCard>

          <UIComponentCard title="Width" id="width"
                           caption="You can change the <code>width</code> through grid column classes, width utilities, or inline styles.">
            <b-placeholder cols="6"/>
            <b-placeholder class="w-75"/>
            <b-placeholder width="25%"/>
          </UIComponentCard>

          <UIComponentCard title="Color" id="color"
                           caption="By default, the <code>placeholder</code> uses <code>currentColor</code>. This can be overridden with a custom color or utility class.">
            <b-placeholder cols="12"/>
            <b-placeholder cols="12" variant="primary"/>
            <b-placeholder cols="12" variant="secondary"/>
            <b-placeholder cols="12" variant="success"/>
            <b-placeholder cols="12" variant="danger"/>
            <b-placeholder cols="12" variant="warning"/>
            <b-placeholder cols="12" variant="info"/>
            <b-placeholder cols="12" variant="light"/>
            <b-placeholder cols="12" variant="dark"/>
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
import UIComponentCard from '@/components/UIComponentCard.vue'

const anchorNavigation = [
  {
    id: 'default',
    title: 'Overview'
  },
  {
    id: 'how-works',
    title: 'How it works'
  },
  {
    id: 'width',
    title: 'Width'
  },
  {
    id: 'color',
    title: 'Color'
  }
]
</script>
