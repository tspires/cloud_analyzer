<template>
  <VerticalLayout>
    <b-row>
      <b-col xl="9">
        <UIComponentCard id="basic" title="Basic Rater Example">
          <div>
            <div id="basic-rater" dir="ltr"></div>
          </div>
        </UIComponentCard>

        <UIComponentCard id="step" title="Rater with Step Example">
          <div>
            <div id="rater-step" dir="ltr"></div>
          </div>
        </UIComponentCard>

        <UIComponentCard id="custom-message" title="Custom Messages Example">
          <div>
            <div id="rater-message" dir="ltr"></div>
          </div>
        </UIComponentCard>

        <UIComponentCard id="readOnly" title="ReadOnly Example">
          <div>
            <div id="rater-unlimitedstar" dir="ltr"></div>
          </div>
        </UIComponentCard>

        <UIComponentCard id="onhover" title="On Hover Event Example">
          <div>
            <div dir="ltr">
              <div id="rater-onhover" class="align-middle"></div>
              <span class="ratingnum badge bg-info align-middle ms-2"></span>
            </div>
          </div>
        </UIComponentCard>

        <UIComponentCard id="reset" title="Clear/Reset Rater Example">
          <div>
            <div dir="ltr">
              <div id="raterreset" class="align-middle"></div>
              <span class="clear-rating"></span>
              <b-button variant="light" size="sm" id="raterreset-button" class="ms-2"> Reset</b-button>
            </div>
          </div>
        </UIComponentCard>

      </b-col>

      <b-col xl="3">
        <AnchorNavigation :elements="anchorNavigation" />
      </b-col>
    </b-row>
  </VerticalLayout>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';

import VerticalLayout from "@/layouts/VerticalLayout.vue";
import AnchorNavigation from '@/components/AnchorNavigation.vue';

import raterJs from 'rater-js/index';
import UIComponentCard from "@/components/UIComponentCard.vue";

const anchorNavigation = [
  {
    id: 'basic',
    title: 'Basic Example'
  },
  {
    id: 'step',
    title: 'Rater with Step Example'
  },
  {
    id: 'custom-message',
    title: 'Custom Messages Example'
  },
  {
    id: 'readOnly',
    title: 'ReadOnly Example'
  },
  {
    id: 'onhover',
    title: 'On Hover Event Example'
  },
  {
    id: 'reset',
    title: 'Clear/Reset Rater Example'
  }
];

onMounted(() => {
  // basic-rater
  if (document.querySelector('#basic-rater')) {
    raterJs({
      starSize: 22,
      rating: 3,
      element: document.querySelector('#basic-rater'),
      rateCallback: function rateCallback(rating: number, done: any) {
        this.setRating(rating);
        done();
      }
    });
  }

  // rater-step
  if (document.querySelector('#rater-step')) {
    raterJs({
      starSize: 22,
      rating: 1.5,
      element: document.querySelector('#rater-step'),
      rateCallback: function rateCallback(rating: number, done: any) {
        this.setRating(rating);
        done();
      }
    });
  }

  // rater-message
  let messageDataService = {
    rate: function (rating: number) {
      return {
        then: function (callback: any) {
          setTimeout(function () {
            callback(Math.random() * 5);
          }, 1000);
        }
      };
    }
  };

  if (document.querySelector('#rater-message')) {
    const starRatingMessage = raterJs({
      isBusyText: 'Rating in progress. Please wait...',
      starSize: 22,
      element: document.querySelector('#rater-message'),
      rateCallback: function rateCallback(rating: number, done: any) {
        starRatingMessage.setRating(rating);
        messageDataService.rate(rating).then(function (avgRating: number) {
          starRatingMessage.setRating(avgRating);
          done();
        });
      }
    });
  }

  // rater-unlimitedstar
  if (document.querySelector('#rater-unlimitedstar')) {
    raterJs({
      starSize: 22,
      max: 5,
      readOnly: true,
      rating: 3.5,
      element: document.querySelector('#rater-unlimitedstar')
    });
  }

  // rater-onhover
  if (document.querySelector('#rater-onhover')) {
    raterJs({
      starSize: 22,
      rating: 1,
      element: document.querySelector('#rater-onhover'),
      rateCallback: function rateCallback(rating: number, done: any) {
        this.setRating(rating);
        done();
      },
      onHover: function (currentIndex: number, currentRating: number) {
        document.querySelector('.ratingnum')!.textContent = currentIndex.toString();
      },
      onLeave: function (currentIndex: number, currentRating: number) {
        document.querySelector('.ratingnum')!.textContent = currentRating.toString();
      }
    });
  }

  // rater-reset
  if (document.querySelector('#raterreset')) {
    const starRatingReset = raterJs({
      starSize: 22,
      rating: 2,
      element: document.querySelector('#raterreset'),
      rateCallback: function rateCallback(rating: number, done: any) {
        this.setRating(rating);
        done();
      }
    });

    const resetButton = document.querySelector('#raterreset-button');
    if (resetButton)
      resetButton.addEventListener(
        'click',
        function () {
          starRatingReset.clear();
        },
        false
      );
  }
});
</script>
