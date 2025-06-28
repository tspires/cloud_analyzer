<template>
  <VerticalLayout>
    <b-row>
      <b-col xl="9">
        <UIComponentCard title="Live demo" id="live-demo">
          <b-button variant="danger"
            v-b-popover.click.right="`And here's some amazing content. It's very engaging. Right?`"
            title="Popover title"> Click to toggle popover
          </b-button>
        </UIComponentCard>

        <UIComponentCard title="Popover Directions" id="popover-directions"
          caption="Four options are available: top, right, bottom, and left aligned.">
          <div class="d-flex flex-wrap gap-2">
            <!-- Top Position -->
            <b-button variant="primary" v-b-popover.click.top="`Vivamus sagittis lacus vel augue laoreet rutrum faucibus.`"> Popover on top
            </b-button>

            <!-- Bottom Position -->
            <b-button variant="primary" v-b-popover.click.bottom="`Vivamus sagittis lacus vel augue laoreet rutrum faucibus.`"> Popover on bottom
            </b-button>

            <!-- Left Position -->
            <b-button variant="primary" v-b-popover.click.left="`Vivamus sagittis lacus vel augue laoreet rutrum faucibus.`"> Popover on left
            </b-button>

            <!-- Right Position -->
            <b-button variant="primary" v-b-popover.click.right="`Vivamus sagittis lacus vel augue laoreet rutrum faucibus.`"> Popover on right
            </b-button>
          </div>
        </UIComponentCard>

        <UIComponentCard title="Dismiss on Next Click" id="dismiss">
          <b-button variant="success"
            v-b-popover.click.right="`And here's some amazing content. It's very engaging. Right?`" trigger="focus"
            title="Dismissible popover"> Dismissible popover
          </b-button>
        </UIComponentCard>

        <UIComponentCard title="Hover" id="hover">
          <b-button variant="dark"
            v-b-popover.hover.right="`And here's some amazing content. It's very engaging. Right?`" title="Ohh Wow !">
            Please Hover Me
          </b-button>
        </UIComponentCard>

        <UIComponentCard title="Custom Popovers" id="custom-popovers">
          <div class="button-list">
            <b-button variant="primary" id="popover-1"> Primary popover</b-button>
            <b-popover target="popover-1" custom-class="primary-popover" placement="top">
              <template #title>Primary popover</template>
              This popover is themed via CSS variables.
            </b-popover>

            <b-button variant="success" id="popover-2"> Success popover</b-button>
            <b-popover target="popover-2" custom-class="success-popover" placement="top">
              <template #title>Success popover</template>
              This popover is themed via CSS variables.
            </b-popover>

            <b-button variant="danger" id="popover-3"> Danger popover</b-button>
            <b-popover target="popover-3" custom-class="danger-popover" placement="top">
              <template #title>Danger popover</template>
              This popover is themed via CSS variables.
            </b-popover>
            <b-button variant="info" id="popover-4"> Info popover</b-button>
            <b-popover target="popover-4" custom-class="info-popover" placement="top">
              <template #title>Info popover</template>
              This popover is themed via CSS variables.
            </b-popover>
          </div>
        </UIComponentCard>

        <UIComponentCard title="Disabled Elements" id="disabled">
          <span class="d-inline-block" v-b-popover.hover.right="`Disabled popover`">
            <b-button variant="primary" style="pointer-events: none" disabled> Disabled button </b-button>
          </span>
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
    id: 'live-demo',
    title: 'Live demo'
  },
  {
    id: 'popover-directions',
    title: 'Popover Directions'
  },
  {
    id: 'dismiss',
    title: 'Dismiss on Next Click'
  },
  {
    id: 'hover',
    title: 'Hover'
  },
  {
    id: 'custom-popovers',
    title: 'Custom Popovers'
  },
  {
    id: 'disabled',
    title: 'Disabled'
  }
];
</script>
