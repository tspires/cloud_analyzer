<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="9">
          <UIComponentCard title="Slides Only" id="slides-only">
            <div class="w-50 mx-auto mb-3">
              <b-carousel>
                <b-carousel-slide :img-src="smallImg2" />
                <b-carousel-slide :img-src="smallImg3" />
                <b-carousel-slide :img-src="smallImg4" />
              </b-carousel>
            </div>
          </UIComponentCard>

          <UIComponentCard title="With Controls" id="with-controls" caption="Adding in the previous and next controls:">
            <div class="w-50 mx-auto mb-3">
              <b-carousel controls>
                <b-carousel-slide :img-src="smallImg4" />
                <b-carousel-slide :img-src="smallImg2" />
                <b-carousel-slide :img-src="smallImg3" />
              </b-carousel>
            </div>
          </UIComponentCard>

          <UIComponentCard title="With Indicators" id="with-indicators"
            caption="You can also add the indicators to the carousel, alongside the controls, too.">
            <div class="w-50 mx-auto mb-3">
              <div class="mx-auto mb-3">
                <b-carousel controls indicators>
                  <b-carousel-slide :img-src="smallImg5" />
                  <b-carousel-slide :img-src="smallImg6" />
                  <b-carousel-slide :img-src="smallImg7" />
                </b-carousel>
              </div>
            </div>
          </UIComponentCard>

          <UIComponentCard title="With Captions" id="with-captions">
            <div class="w-50 mx-auto mb-3">
              <b-carousel controls>
                <b-carousel-slide :img-src="smallImg6"
                  text="Some representative placeholder content for the first slide."
                  caption-html="<h5 class='text-white'>First slide label</h5>" />

                <b-carousel-slide :img-src="smallImg7"
                  text="Some representative placeholder content for the second slide."
                  caption-html="<h5 class='text-white'>Second slide label</h5>" />

                <b-carousel-slide :img-src="smallImg5"
                  text="Some representative placeholder content for the third slide."
                  caption-html="<h5 class='text-white'>Third slide label</h5>" />
              </b-carousel>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Crossfade" id="crossfade">
            <div class="w-50 mx-auto mb-3">
              <b-carousel fade controls>
                <b-carousel-slide :img-src="smallImg1" />
                <b-carousel-slide :img-src="smallImg2" />
                <b-carousel-slide :img-src="smallImg3" />
              </b-carousel>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Individual interval" id="individual-carousel-item-interval">
            <div class="w-50 mx-auto mb-3">
              <b-carousel controls :interval="1000">
                <b-carousel-slide :img-src="smallImg1" />
                <b-carousel-slide :img-src="smallImg2" />
                <b-carousel-slide :img-src="smallImg3" />
              </b-carousel>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Disable touch swiping interval" id="disable-touch-swiping">
            <div class="w-50 mx-auto mb-3">
              <b-carousel controls no-touch>
                <b-carousel-slide :img-src="smallImg4" />
                <b-carousel-slide :img-src="smallImg5" />
                <b-carousel-slide :img-src="smallImg6" />
              </b-carousel>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Dark Variant interval" id="dark-variant">
            <div class="w-50 mx-auto mb-3">
              <b-carousel controls indicators class="carousel-dark">
                <b-carousel-slide :img-src="smallImg8"
                  text="Some representative placeholder content for the first slide."
                  caption-html="<h5>First slide label</h5>" />

                <b-carousel-slide :img-src="smallImg9"
                  text="Some representative placeholder content for the second slide."
                  caption-html="<h5>Second slide label</h5>" />

                <b-carousel-slide :img-src="smallImg10"
                  text="Some representative placeholder content for the third slide."
                  caption-html="<h5>Third slide label</h5>" />
              </b-carousel>
            </div>
          </UIComponentCard>
        </b-col>

        <b-col xl="3">
          <AnchorNavigation :elements="anchorNavigation" />
        </b-col>
      </b-row>
  </VerticalLayout>
</template>

<script lang="ts" setup>
import VerticalLayout from "@/layouts/VerticalLayout.vue";

import AnchorNavigation from '@/components/AnchorNavigation.vue';
import UIComponentCard from '@/components/UIComponentCard.vue';

import smallImg1 from '@/assets/images/small/img-1.jpg';
import smallImg2 from '@/assets/images/small/img-2.jpg';
import smallImg3 from '@/assets/images/small/img-3.jpg';
import smallImg4 from '@/assets/images/small/img-4.jpg';
import smallImg5 from '@/assets/images/small/img-5.jpg';
import smallImg6 from '@/assets/images/small/img-6.jpg';
import smallImg7 from '@/assets/images/small/img-7.jpg';
import smallImg8 from '@/assets/images/small/img-8.jpg';
import smallImg9 from '@/assets/images/small/img-9.jpg';
import smallImg10 from '@/assets/images/small/img-10.jpg';

const anchorNavigation = [
  {
    id: 'slides-only',
    title: 'Slide Only'
  },
  {
    id: 'with-controls',
    title: 'With Controls'
  },
  {
    id: 'with-indicators',
    title: 'With Indicators'
  },
  {
    id: 'with-captions',
    title: 'With Captions'
  },
  {
    id: 'crossfade',
    title: 'Crossfade'
  },
  {
    id: 'individual-carousel-item-interval',
    title: 'Individual .carousel-item interval'
  },
  {
    id: 'disable-touch-swiping',
    title: 'Disable touch swiping'
  },
  {
    id: 'dark-variant',
    title: 'Dark Variant'
  }
];
</script>
