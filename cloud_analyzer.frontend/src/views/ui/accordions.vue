<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="9">
          <UIComponentCard title="Basic Example" id="default">
            <b-accordion id="accordionExample" class="mt-3">
              <b-accordion-item title="Accordion Item #1" visible>
                <strong>This is the first item's accordion body.</strong> It is shown by default, until the collapse
                plugin adds the appropriate classes that we use to style each element. These classes control the overall
                appearance, as well as the showing and hiding via CSS transitions. You can modify any of this with
                custom CSS or overriding our default variables. It's also worth noting that just about any HTML can go
                within the <code>.accordion-body</code>, though the transition does limit
                overflow.
              </b-accordion-item>
              <b-accordion-item title="Accordion Item #2">
                <strong>This is the second item's accordion body.</strong> It is hidden by default, until the collapse
                plugin adds the appropriate classes that we use to style each element. These classes control the overall
                appearance, as well as the showing and hiding via CSS transitions. You can modify any of this with
                custom CSS or overriding our default variables. It's also worth noting that just about any HTML can go
                within the <code>.accordion-body</code>, though the transition does limit
                overflow.
              </b-accordion-item>
              <b-accordion-item title="Accordion Item #3">
                <strong>This is the third item's accordion body.</strong>It is hidden by default, until the collapse
                plugin adds the appropriate classes that we use to style each element. These classes control the overall
                appearance, as well as the showing and hiding via CSS transitions. You can modify any of this with
                custom CSS or overriding our default variables. It's also worth noting that just about any HTML can go
                within the <code>.accordion-body</code>, though the transition does limit
                overflow.
              </b-accordion-item>
            </b-accordion>
          </UIComponentCard>

          <UIComponentCard title="Flush Accordion" id="flush">
            <b-accordion id="accordionFlushExample" flush class="mt-3">
              <b-accordion-item title="Accordion Item #1" visible>
                Placeholder content for this accordion, which is intended to demonstrate the
                <code>.accordion-flush</code> class. This is the first item's accordion body.
              </b-accordion-item>
              <b-accordion-item title="Accordion Item #2">
                Placeholder content for this accordion, which is intended to demonstrate the
                <code>.accordion-flush</code>
                class. This is the second item's accordion body. Let's imagine this being filled with some actual
                content.
              </b-accordion-item>
              <b-accordion-item title="Accordion Item #3">
                Placeholder content for this accordion, which is intended to demonstrate the
                <code>.accordion-flush</code>
                class. This is the third item's accordion body. Nothing more exciting happening here in terms of
                content, but just filling up the space to make it look, at least at first glance, a bit more
                representative of how this would look in a real-world application.
              </b-accordion-item>
            </b-accordion>
          </UIComponentCard>

          <UIComponentCard title="Always Open Accordion" id="always-open">
            <b-accordion id="accordionPanelsStayOpenExample" free class="mt-3">
              <b-accordion-item title="Accordion Item #1" visible>
                <strong>This is the first item's accordion body.</strong>
                It is shown by default, until the collapse plugin adds the appropriate classes that we use to style each
                element. These classes control the overall appearance, as well as the showing and hiding via CSS
                transitions. You can modify any of this with custom CSS or overriding our default variables. It's also
                worth noting that just about any HTML can go within the
                <code>.accordion-body</code>, though the transition does limit overflow.
              </b-accordion-item>
              <b-accordion-item title="Accordion Item #2">
                <strong>This is the second item's accordion body.</strong>
                It is hidden by default, until the collapse plugin adds the appropriate classes that we use to style
                each element. These classes control the overall appearance, as well as the showing and hiding via CSS
                transitions. You can modify any of this with custom CSS or overriding our default variables. It's also
                worth noting that just about any HTML can go within the
                <code>.accordion-body</code>, though the transition does limit overflow.
              </b-accordion-item>
              <b-accordion-item title="Accordion Item #3">
                <strong>This is the third item's accordion body.</strong>
                It is hidden by default, until the collapse plugin adds the appropriate classes that we use to style
                each element. These classes control the overall appearance, as well as the showing and hiding via CSS
                transitions. You can modify any of this with custom CSS or overriding our default variables. It's also
                worth noting that just about any HTML can go within the
                <code>.accordion-body</code>, though the transition does limit overflow.
              </b-accordion-item>
            </b-accordion>
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
    title: 'Default Example'
  },
  {
    id: 'flush',
    title: 'Flush Accordion'
  },
  {
    id: 'always-open',
    title: 'Always Open'
  }
]
</script>
