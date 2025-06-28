<template>
  <VerticalLayout>
    <b-row>
      <b-col xl="9">
        <UIComponentCard title="Default Example" id="default">
          <div class="hstack gap-2 mt-3">
            <b-button variant="primary" class="mb-2" v-b-toggle.collapseExample aria-controls="collapseExample"> 
              Link with href
            </b-button>
            <b-button variant="primary" class="mb-2" v-b-toggle.collapseExample aria-controls="collapseExample">
              Button with data-bs-target
            </b-button>
          </div>
          <b-collapse id="collapseExample">
            <b-card no-body class="mb-0">
              <b-card-body> Some placeholder content for the collapse component. This panel is hidden by default but
                revealed when the user activates the relevant trigger.
              </b-card-body>
            </b-card>
          </b-collapse>
        </UIComponentCard>

        <UIComponentCard title="Horizontal" id="horizontal">
          <b-button class="mb-2" variant="primary" v-b-toggle.collapseWidthExample aria-controls="collapseWidthExample">
            Toggle width collapse
          </b-button>
          <div>
            <b-collapse horizontal id="collapseWidthExample">
              <b-card no-body class="card-body mb-0" style="width: 300px"> This is some placeholder content for a
                horizontal collapse. It's hidden by default and shown when triggered.
              </b-card>
            </b-collapse>
          </div>
        </UIComponentCard>

        <UIComponentCard title="Multiple Targets" id="multiple-targets">
          <div class="hstack gap-2 my-3">
            <b-button variant="primary" v-b-toggle.multiCollapseExample1>Toggle first element</b-button>
            <b-button variant="primary" v-b-toggle.multiCollapseExample2>Toggle second element</b-button>
            <b-button variant="primary" v-b-toggle="['multiCollapseExample1', 'multiCollapseExample2']"> Toggle both elements </b-button>
          </div>
          <b-row>
            <b-col>
              <b-collapse class="multi-collapse" id="multiCollapseExample1">
                <b-card no-body class="card-body"> Some placeholder content for the first collapse component of this
                  multi-collapse example. This panel is hidden by default but revealed when the user activates the
                  relevant trigger.
                </b-card>
              </b-collapse>
            </b-col>
            <b-col>
              <b-collapse class="multi-collapse" id="multiCollapseExample2">
                <b-card no-body class="card-body"> Some placeholder content for the second collapse component of this
                  multi-collapse example. This panel is hidden by default but revealed when the user activates the
                  relevant trigger.
                </b-card>
              </b-collapse>
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

import AnchorNavigation from '@/components/AnchorNavigation.vue';
import UIComponentCard from '@/components/UIComponentCard.vue';

const anchorNavigation = [
  {
    id: 'default',
    title: 'Default Example'
  },
  {
    id: 'horizontal',
    title: 'Horizontal Collapse'
  },
  {
    id: 'multiple-targets',
    title: 'Multiple Targets'
  }
];
</script>
