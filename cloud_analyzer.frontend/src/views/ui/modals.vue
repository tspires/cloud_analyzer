<template>
  <VerticalLayout>
    <b-row>
      <b-col xl="9">
        <UIComponentCard title="Default Modals" id="default" caption="Toggle a working modal demo by clicking the button below. It will slide down and fade in from the top of the page.">
          <b-button variant="primary" @click="modal = !modal"> Launch demo modal</b-button>
        </UIComponentCard>

        <UIComponentCard title="Static Backdrop" id="static-backdrop" caption="When backdrop is set to static, the modal will not close when clicking outside of it. Click the button below to try it.">
          <b-button variant="primary" @click="staticBackdropModal = !staticBackdropModal"> Launch static backdrop modal </b-button>
        </UIComponentCard>

        <UIComponentCard title="Scrolling Long Content" id="scrolling-long-content" caption="When modals become too long for the user&rsquo;s viewport or device, they scroll independent of the page itself. Try the demo below to see what we mean.">
          <!-- Button trigger modal -->
          <b-button type="button" variant="primary" class="me-2" @click="scrollingLongModal = !scrollingLongModal">
            Launch demo modal
          </b-button>

          <!-- Button trigger modal -->
          <b-button variant="primary" @click="scrollingLongModal1 = !scrollingLongModal1"> Launch demo modal </b-button>
        </UIComponentCard>

        <UIComponentCard title="Modal Position" id="modal-position">
          <div class="d-flex flex-wrap gap-2 mt-3">
            <!-- Button trigger modal -->
            <b-button variant="primary" @click="verticalCenteredModal = !verticalCenteredModal"> Vertically centered
              modal
            </b-button>

            <!-- Button trigger modal -->
            <b-button variant="primary" @click="verticalCenteredScrollableModal = !verticalCenteredScrollableModal">
              Vertically centered scrollable modal
            </b-button>
          </div>

          <div class="d-flex flex-wrap gap-2 mt-3">
            <!-- Button trigger modal -->
            <div class="hstack gap-2">
              <b-button variant="primary" @click="topModal = !topModal"> Top Modal</b-button>
              <b-button variant="primary" @click="bottomModal = !bottomModal"> Bottom Modal</b-button>
            </div>
          </div>
        </UIComponentCard>

        <UIComponentCard title="Toggle Between Modals" id="toggle-between-modals">
          <a class="btn btn-primary mt-3" @click="toggleModal1 = !toggleModal1">Open first modal</a>
        </UIComponentCard>

        <UIComponentCard title="Optional Sizes" id="optional-sizes">
          <div class="hstack gap-2 mt-3">
            <!-- Button trigger modal -->
            <b-button variant="primary" @click="extraLargeModal = !extraLargeModal"> Extra large modal</b-button>
            <b-button variant="primary" @click="largeModal = !largeModal"> Large modal</b-button>
            <b-button variant="primary" @click="smallModal = !smallModal"> Small modal</b-button>
          </div>
        </UIComponentCard>

        <UIComponentCard title="Fullscreen Modal" id="fullscreen-modal">
          <div class="hstack flex-wrap gap-2 mt-3">
            <!-- Button trigger modal -->
            <b-button variant="primary" @click="fsModal = !fsModal"> Full screen</b-button>
            <b-button variant="primary" @click="fsBSMModal = !fsBSMModal"> Full screen below sm</b-button>
            <b-button variant="primary" @click="fsBMDModal = !fsBMDModal"> Full screen below md</b-button>
            <b-button variant="primary" @click="fsBLGModal = !fsBLGModal"> Full screen below lg</b-button>
            <b-button variant="primary" @click="fsBXLModal = !fsBXLModal"> Full screen below xl</b-button>
            <b-button variant="primary" @click="fsBXXLModal = !fsBXXLModal"> Full screen below xxl</b-button>
          </div>
        </UIComponentCard>

        <UIComponentCard title="Modal Based Alerts" id="modal-alerts">
          <div class="hstack flex-wrap gap-2 mt-3">
            <b-button variant="primary" @click="primaryAlertModal = !primaryAlertModal"> Primary Alert</b-button>
            <b-button variant="secondary" @click="secondaryAlertModal = !secondaryAlertModal"> Secondary Alert</b-button>
            <b-button variant="success" @click="successAlertModal = !successAlertModal"> Success Alert</b-button>
            <b-button variant="info" @click="infoAlertModal = !infoAlertModal"> Info Alert</b-button>
          </div>
        </UIComponentCard>
      </b-col>

      <b-col xl="3">
        <AnchorNavigation :elements="anchorNavigation" />
      </b-col>
    </b-row>

    <!-- Default Modals  -->
    <b-modal v-model="modal" title="Modal title" ok-title="Save changes" cancel-title="Close">
      <p>Woo-hoo, you're reading this text in a modal!</p>
    </b-modal>

    <!-- Static Backdrop  -->
    <b-modal v-model="staticBackdropModal" title="Modal title" ok-title="Understood" cancel-title="Close"
      :noCloseOnBackdrop="true">
      <p>I will not close if you click outside of me. Don't even try to press escape key.</p>
    </b-modal>

    <!-- Scrolling Long Content -->
    <b-modal v-model="scrollingLongModal" title="Modal title" ok-title="Save changes" cancel-title="Close"
      :bodyScrolling="true">
      <div style="min-height: 1500px">
        <p>This is some placeholder content to show the scrolling behavior for modals. Instead of repeating the text the
          modal, we use an inline style set a minimum height, thereby extending the length of the overall modal and
          demonstrating the overflow scrolling. When content becomes longer than the height of the viewport, scrolling
          will move the modal as needed.</p>
      </div>
    </b-modal>

    <b-modal v-model="scrollingLongModal1" title="Modal title" ok-title="Save changes" cancel-title="Close"
      :bodyScrolling="true" :scrollable="true">
      <p>This is some placeholder content to show the scrolling behavior for modals. We use repeated line breaks to
        demonstrate how content can exceed minimum inner height, thereby showing inner scrolling. When content becomes
        longer than the predefined max-height of modal, content will be cropped and scrollable within the modal.</p>
      <br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br />
      <p>This content should appear at the bottom after you scroll.</p>
    </b-modal>

    <!-- Modal Position  -->
    <b-modal v-model="verticalCenteredModal" title="Modal title" ok-title="Save changes" cancel-title="Close" centered>
      <p>This is a vertically centered modal.</p>
    </b-modal>

    <b-modal v-model="verticalCenteredScrollableModal" title="Modal title" ok-title="Save changes" cancel-title="Close"
      centered>
      <p>This is some placeholder content to show a vertically centered modal. We've added some extra copy here to show
        how vertically centering the modal works when combined with scrollable modals. We also use some repeated line
        breaks to quickly extend the height of the content, thereby triggering the scrolling. When content becomes
        longer than the predefined max-height of modal, content will be cropped and scrollable within the modal.</p>
      <br /><br /><br /><br /><br /><br /><br /><br /><br /><br />
      <p>Just like that.</p>
    </b-modal>

    <!-- Top Modal -->
    <b-modal v-model="topModal" title="Modal Heading" ok-title="Save changes" cancel-title="Close"
      dialog-class="modal-top">
      <h6>Text in a modal</h6>
      <p class="mb-0">Duis mollis, est non commodo luctus, nisi erat porttitor ligula.</p>
    </b-modal>

    <!-- Bottom Modal -->
    <b-modal v-model="bottomModal" title="Modal Heading" ok-title="Save changes" cancel-title="Close"
      dialog-class="modal-bottom">
      <h6>Text in a modal</h6>
      <p class="mb-0">Duis mollis, est non commodo luctus, nisi erat porttitor ligula.</p>
    </b-modal>

    <!-- Toggle Between Modals -->
    <!-- First Modal -->
    <b-modal v-model="toggleModal1" title="Modal 1" @ok="toggleModal" ok-title="Open second modal" ok-only centered>
      Show a second modal and hide this one with the button below.
    </b-modal>

    <!-- Second Modal -->
    <b-modal v-model="toggleModal2" title="Modal 2" ok-title="Back to first" cancel-title="Close" @ok="toggleModal"
      centered> Hide this modal and show the first with the button below.
    </b-modal>

    <!-- Optional Sizes -->
    <b-modal v-model="extraLargeModal" title="Extra large modal" size="xl" hide-footer> ...</b-modal>
    <b-modal v-model="largeModal" title="Large modal" size="lg" hide-footer> ...</b-modal>
    <b-modal v-model="smallModal" title="Small modal" size="sm" hide-footer> ...</b-modal>

    <!-- Fullscreen Modal -->
    <b-modal v-model="fsModal" title="Full screen modal" ok-only ok-title="Close" ok-variant="secondary" fullscreen>
      ...
    </b-modal>
    <b-modal v-model="fsBSMModal" title="Full screen below sm" ok-only ok-title="Close" ok-variant="secondary"
      fullscreen="sm"> ...
    </b-modal>
    <b-modal v-model="fsBMDModal" title="Full screen below md" ok-only ok-title="Close" ok-variant="secondary"
      fullscreen="md"> ...
    </b-modal>
    <b-modal v-model="fsBLGModal" title="Full screen below lg" ok-only ok-title="Close" ok-variant="secondary"
      fullscreen="lg"> ...
    </b-modal>
    <b-modal v-model="fsBXLModal" title="Full screen below xl" ok-only ok-title="Close" ok-variant="secondary"
      fullscreen="xl"> ...
    </b-modal>
    <b-modal v-model="fsBXXLModal" title="Full screen below xxl" ok-only ok-title="Close" ok-variant="secondary"
      fullscreen="xxl"> ...
    </b-modal>

    <!-- Modal Based Alerts -->
    <b-modal v-model="primaryAlertModal" hide-header hide-footer size="sm" content-class="bg-primary">
      <div class="text-center">
        <i class="bx bx-check-double display-6 mt-0 text-white"></i>
        <h4 class="mt-3 text-white">Well Done!</h4>
        <p class="mt-3 text-white">Cras mattis consectetur purus sit amet fermentum. Cras justo odio, dapibus ac
          facilisis in, egestas eget quam.</p>
        <b-button type="button" variant="light" class="mt-3" @click="primaryAlertModal = !primaryAlertModal"> Continue
        </b-button>
      </div>
    </b-modal>

    <b-modal v-model="secondaryAlertModal" hide-header hide-footer size="sm" content-class="modal-filled bg-secondary">
      <div class="text-center">
        <i class="bx bx-check-double display-6 mt-0 text-white"></i>
        <h4 class="mt-3 text-white">Well Done!</h4>
        <p class="mt-3">Cras mattis consectetur purus sit amet fermentum. Cras justo odio, dapibus ac facilisis in,
          egestas eget quam.</p>
        <b-button type="button" variant="light" class="mt-3" @click="secondaryAlertModal = !secondaryAlertModal">
          Continue
        </b-button>
      </div>
    </b-modal>

    <b-modal v-model="successAlertModal" hide-header hide-footer size="sm" content-class="modal-filled bg-success">
      <div class="text-center">
        <i class="bx bx-check-double display-6 mt-0 text-white"></i>
        <h4 class="mt-3 text-white">Well Done!</h4>
        <p class="mt-3">Cras mattis consectetur purus sit amet fermentum. Cras justo odio, dapibus ac facilisis in,
          egestas eget quam.</p>
        <b-button type="button" variant="light" class="mt-3" @click="successAlertModal = !successAlertModal"> Continue
        </b-button>
      </div>
    </b-modal>

    <b-modal v-model="infoAlertModal" hide-header hide-footer size="sm" content-class="modal-filled bg-info">
      <div class="text-center">
        <i class="bx bx-check-double display-6 mt-0 text-white"></i>
        <h4 class="mt-3 text-white">Well Done!</h4>
        <p class="mt-3">Cras mattis consectetur purus sit amet fermentum. Cras justo odio, dapibus ac facilisis in,
          egestas eget quam.</p>
        <b-button type="button" variant="light" class="mt-3" @click="infoAlertModal = !infoAlertModal"> Continue
        </b-button>
      </div>
    </b-modal>
  </VerticalLayout>
</template>

<script lang="ts" setup>
import VerticalLayout from "@/layouts/VerticalLayout.vue";

import AnchorNavigation from '@/components/AnchorNavigation.vue';
import UIComponentCard from '@/components/UIComponentCard.vue';

import { ref } from 'vue';

const modal = ref(false);
const staticBackdropModal = ref(false);
const scrollingLongModal = ref(false);
const scrollingLongModal1 = ref(false);
const verticalCenteredModal = ref(false);
const verticalCenteredScrollableModal = ref(false);
const topModal = ref(false);
const bottomModal = ref(false);

const toggleModal1 = ref(false);
const toggleModal2 = ref(false);

const toggleModal = () => {
  toggleModal2.value = !toggleModal2.value;
  toggleModal1.value = !toggleModal1.value;
};

const extraLargeModal = ref(false);
const largeModal = ref(false);
const smallModal = ref(false);

const fsModal = ref(false);
const fsBSMModal = ref(false);
const fsBMDModal = ref(false);
const fsBLGModal = ref(false);
const fsBXLModal = ref(false);
const fsBXXLModal = ref(false);

const primaryAlertModal = ref(false);
const secondaryAlertModal = ref(false);
const successAlertModal = ref(false);
const infoAlertModal = ref(false);

const anchorNavigation = [
  {
    id: 'default',
    title: 'Default Example'
  },
  {
    id: 'static-backdrop',
    title: 'Static Backdrop'
  },
  {
    id: 'scrolling-long-content',
    title: 'Scrolling Long Content'
  },
  {
    id: 'modal-position',
    title: 'Modal Position'
  },
  {
    id: 'toggle-between-modals',
    title: 'Toggle Between Modals'
  },
  {
    id: 'optional-sizes',
    title: 'Optional Sizes'
  },
  {
    id: 'fullscreen-modal',
    title: 'Fullscreen Modal'
  },
  {
    id: 'modal-alerts',
    title: 'Modal Based Alerts'
  }
];
</script>
