<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="9">
          <UIComponentCard title="Tooltip Direction" id="direction"
                           caption="Four options are available: top, right, bottom, and left aligned.">
            <div class="d-flex flex-wrap gap-2">
              <b-button variant="primary" v-b-tooltip.hover.top="'Tooltip on top'"> Tooltip on top</b-button>
              <b-button variant="primary" v-b-tooltip.hover.right="'Tooltip on right'"> Tooltip on right</b-button>
              <b-button variant="primary" v-b-tooltip.hover.bottom="'Tooltip on bottom'"> Tooltip on bottom</b-button>
              <b-button variant="primary" v-b-tooltip.hover.left="'Tooltip on left'"> Tooltip on left</b-button>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Color Tooltip" id="color_tooltip">
            <div class="d-flex flex-wrap gap-1">
              <b-button variant="primary" id="tooltip1"> Primary tooltip</b-button>
              <b-tooltip target="tooltip1" class="primary-tooltip">This top tooltip is themed via CSS variables.
              </b-tooltip>

              <b-button variant="danger" id="tooltip2"> Danger tooltip</b-button>
              <b-tooltip target="tooltip2" class="danger-tooltip">This top tooltip is themed via CSS variables.
              </b-tooltip>

              <b-button variant="info" id="tooltip3"> Info tooltip</b-button>
              <b-tooltip target="tooltip3" class="info-tooltip">This top tooltip is themed via CSS variables.
              </b-tooltip>

              <b-button variant="success" id="tooltip4"> Success tooltip</b-button>
              <b-tooltip target="tooltip4" class="success-tooltip">This top tooltip is themed via CSS variables.
              </b-tooltip>
            </div>
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
    id: 'direction',
    title: 'Direction'
  },
  {
    id: 'color_tooltip',
    title: 'Color Tooltip'
  }
]
</script>
