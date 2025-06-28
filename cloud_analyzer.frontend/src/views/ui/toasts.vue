<template>
  <VerticalLayout>
    <b-row>
      <b-col xl="9">
        <UIComponentCard title="Basic Examples" id="basic_examples"
          caption="Toasts are as flexible as you need and have very little required markup. At a minimum, we require a single element to contain your “toasted” content and strongly encourage a dismiss button.">
          <b-toast :model-value="true" :noCloseButton="true" header-class="d-flex justify-content-between">
            <template #title>
              <div class="auth-logo">
                <img class="logo-dark" :src="logoDark" alt="logo-dark" height="18">
                <img class="logo-light" :src="logoLight" alt="logo-light" height="18">
              </div>
              <div class="float-end">
                <small>11 mins ago</small>
                <button type="button" class="ms-2 btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
              </div>
            </template>
            Hello, world! This is a toast message.
          </b-toast>
        </UIComponentCard>

        <UIComponentCard title="Live example" id="live_example"
          caption="Click the button below to show a toast (positioned with our utilities in the lower right corner) that has been hidden by default.">
          <b-button variant="primary" id="liveToastDefaultBtn"> Show live toast</b-button>

          <div class="toast-container position-fixed bottom-0 end-0 p-3">
            <b-toast v-model="liveExample" :noCloseButton="true" header-class="d-flex justify-content-between">
              <template #title>
                <div class="auth-logo">
                  <img class="logo-dark" :src="logoDark" alt="logo-dark" height="18" />
                  <img class="logo-light" :src="logoLight" alt="logo-light" height="18" />
                </div>
                <div class="float-end">
                  <small>11 mins ago</small>
                  <button type="button" class="ms-2 btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
              </template>
              Hello, world! This is a toast message.
            </b-toast>
          </div>
        </UIComponentCard>

        <UIComponentCard title="Default Buttons" id="default_buttons"
          caption="Toasts are as flexible as you need and have very little required markup. At a minimum, we require a single element to contain your “toasted” content and strongly encourage a dismiss button.">
          <b-button variant="primary" id="liveToastBtn" class="me-2"> Show live toast</b-button>
          <b-button variant="primary" id="liveToastBtn2"> Show live toast</b-button>

          <div class="toast-container position-fixed end-0 top-0 p-3">
            <div id="liveToast" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
              <div class="toast-header">
                <div class="auth-logo me-auto">
                  <img class="logo-dark" :src="logoDark" alt="logo-dark" height="18" />
                  <img class="logo-light" :src="logoLight" alt="logo-light" height="18" />
                </div>
                <small class="text-muted">just now</small>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
              </div>
              <div class="toast-body">See? Just like this.</div>
            </div>

            <div id="liveToast2" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
              <div class="toast-header">
                <div class="auth-logo me-auto">
                  <img class="logo-dark" :src="logoDark" alt="logo-dark" height="18" />
                  <img class="logo-light" :src="logoLight" alt="logo-light" height="18" />
                </div>
                <small class="text-muted">2 seconds ago</small>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
              </div>
              <div class="toast-body">Heads up, toasts will stack automatically</div>
            </div>
          </div>
        </UIComponentCard>

        <UIComponentCard title="Custom Content" id="custom_content"
          caption="Alternatively, you can also add additional controls and components to toasts.">
          <b-row>
            <b-col md="6">
              <div class="toast fade show align-items-center mb-3" role="alert" aria-live="assertive"
                aria-atomic="true">
                <div class="d-flex">
                  <div class="toast-body">Hello, world! This is a toast message.</div>
                  <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast"
                    aria-label="Close"></button>
                </div>
              </div>
            </b-col>
            <b-col md="6">
              <div class="toast fade show align-items-center text-bg-primary mb-3" role="alert" aria-live="assertive"
                aria-atomic="true">
                <div class="d-flex">
                  <div class="toast-body">Hello, world! This is a toast message.</div>
                  <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"
                    aria-label="Close"></button>
                </div>
              </div>
            </b-col>
          </b-row>

          <b-row>
            <b-col md="6">
              <div class="toast fade show mb-3 mb-md-0" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="toast-body">
                  Hello, world! This is a toast message.
                  <div class="mt-2 pt-2 border-top">
                    <button type="button" class="btn btn-primary btn-sm me-1">Take action</button>
                    <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="toast">Close</button>
                  </div>
                </div>
              </div>
            </b-col>
            <b-col md="6">
              <div class="toast fade show text-bg-primary" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="toast-body">
                  Hello, world! This is a toast message.
                  <div class="mt-2 pt-2 border-top">
                    <button type="button" class="btn btn-light btn-sm me-1">Take action</button>
                    <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="toast">Close</button>
                  </div>
                </div>
              </div>
            </b-col>
          </b-row>
        </UIComponentCard>

        <UIComponentCard title="Transcluent" id="transcluent"
          caption="Toasts are slightly translucent, too, so they blend over whatever they might appear over. For browsers that support the backdrop-filter CSS property, we’ll also attempt to blur the elements under a toast.">
          <div class="p-3 bg-light">
            <b-toast :model-value="true" role="alert" aria-live="assertive" aria-atomic="true" :noCloseButton="true"
              header-class="d-flex justify-content-between">
              <template #title>
                <div class="auth-logo">
                  <img class="logo-dark" :src="logoDark" alt="logo-dark" height="18" />
                  <img class="logo-light" :src="logoLight" alt="logo-light" height="18" />
                </div>
                <div class="float-end">
                  <small>11 mins ago</small>
                  <button type="button" class="ms-2 btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
              </template>
              Hello, world! This is a toast message.
            </b-toast>
          </div>
        </UIComponentCard>

        <UIComponentCard title="Placement" id="placement">
          <div aria-live="polite" aria-atomic="true" class="bg-light position-relative mt-3" style="min-height: 350px">
            <div class="toast-container position-absolute p-3" id="toastPlacement" :class="selected">
              <b-toast :model-value="true" :noCloseButton="true" header-class="d-flex justify-content-between">
                <template #title>
                  <div class="auth-logo">
                    <img class="logo-dark" :src="logoDark" alt="logo-dark" height="18" />
                    <img class="logo-light" :src="logoLight" alt="logo-light" height="18" />
                  </div>
                  <div class="float-end">
                    <small>11 mins ago</small>
                    <button type="button" class="ms-2 btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
                  </div>
                </template>
                Hello, world! This is a toast message.
              </b-toast>
            </div>
          </div>

          <b-form>
            <div class="my-3">
              <label for="selectToastPlacement" class="form-label">Toast placement</label>
              <b-form-select v-model="selected" :options="options" class="mt-2" id="selectToastPlacement" />
            </div>
          </b-form>
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

import { Toast } from 'bootstrap';
import logoDark from '@/assets/images/logo-dark.png';
import logoLight from '@/assets/images/logo-light.png';

import { ref, onMounted } from 'vue';

const anchorNavigation = [
  {
    id: 'basic_examples',
    title: 'Basic Examples'
  },
  {
    id: 'live_example',
    title: 'Live example'
  },
  {
    id: 'default_buttons',
    title: 'Default Buttons'
  },
  {
    id: 'custom_content',
    title: 'Custom Content'
  },
  {
    id: 'transcluent',
    title: 'Transcluent'
  },
  {
    id: 'placement',
    title: 'Placement'
  }
];

const liveExample = ref(false);

onMounted(() => {
  // Default
  const toastDefaultTrigger = document.getElementById('liveToastDefaultBtn');
  if (toastDefaultTrigger) {
    toastDefaultTrigger.addEventListener('click', () => {
      liveExample.value = true;
      setInterval(() => {
        liveExample.value = false;
      }, 3000);
    });
  }

  // Stacking Example
  const toastTrigger = document.getElementById('liveToastBtn');
  const toastLiveExample = document.getElementById('liveToast') as HTMLElement;
  if (toastTrigger) {
    toastTrigger.addEventListener('click', () => {
      const toast = new Toast(toastLiveExample);

      toast.show();
    });
  }

  const toastTrigger2 = document.getElementById('liveToastBtn2');
  const toastLiveExample2 = document.getElementById('liveToast2') as HTMLElement;
  if (toastTrigger2) {
    toastTrigger2.addEventListener('click', () => {
      const toast = new Toast(toastLiveExample2);
      toast.show();
    });
  }
});

const selected = ref(null);
const options = [
  {
    value: null,
    text: 'Select a position...'
  },
  {
    value: 'top-0 start-0',
    text: 'Top left'
  },
  {
    value: 'top-0 start-50 translate-middle-x',
    text: 'Top center'
  },
  {
    value: 'top-0 end-0',
    text: 'Top right'
  },
  {
    value: 'top-50 start-0 translate-middle-y',
    text: 'Middle left'
  },
  {
    value: 'top-50 start-50 translate-middle',
    text: 'Middle center'
  },
  {
    value: 'top-50 end-0 translate-middle-y',
    text: 'Middle right'
  },
  {
    value: 'bottom-0 start-0',
    text: 'Bottom left'
  },
  {
    value: 'bottom-0 start-50 translate-middle-x',
    text: 'Bottom center'
  },
  {
    value: 'bottom-0 end-0',
    text: 'Bottom right'
  }
];
</script>
