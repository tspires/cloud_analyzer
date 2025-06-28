<template>
  <VerticalLayout>
    <b-row>
      <b-col xl="9">
        <UIComponentCard title="Basic Example" id="overview">
          <div class="mt-3">
            <b-alert :model-value="true" variant="primary">A simple primary alert—check it out!</b-alert>
            <b-alert :model-value="true" variant="secondary">A simple secondary alert—check it out!</b-alert>
            <b-alert :model-value="true" variant="success">A simple success alert—check it out!</b-alert>
            <b-alert :model-value="true" variant="danger">A simple danger alert—check it out!</b-alert>
            <b-alert :model-value="true" variant="warning">A simple warning alert—check it out!</b-alert>
            <b-alert :model-value="true" variant="info">A simple info alert—check it out!</b-alert>
            <b-alert :model-value="true" variant="light">A simple light alert—check it out!</b-alert>
            <b-alert :model-value="true" variant="dark" class="mb-0">A simple dark alert—check it out!</b-alert>
          </div>
        </UIComponentCard>

        <UIComponentCard title="Dismissible Alerts Example" id="alert-dismissible">
          <div class="mt-3">
            <b-alert :model-value="true" dismissible variant="primary">A simple primary alert—check it out!</b-alert>
            <b-alert :model-value="true" dismissible variant="secondary">A simple secondary alert—check it out!</b-alert>
            <b-alert :model-value="true" dismissible variant="success">A simple success alert—check it out!</b-alert>
            <b-alert :model-value="true" dismissible variant="danger">A simple danger alert—check it out!</b-alert>
            <b-alert :model-value="true" dismissible variant="warning">A simple warning alert—check it out!</b-alert>
            <b-alert :model-value="true" dismissible variant="info">A simple info alert—check it out!</b-alert>
            <b-alert :model-value="true" dismissible variant="light">A simple light alert—check it out!</b-alert>
            <b-alert :model-value="true" dismissible variant="dark" class="mb-0">A simple dark alert—check it out!
            </b-alert>
          </div>
        </UIComponentCard>

        <UIComponentCard title="Alert Link Example" id="alert-link">
          <div class="mt-3">
            <b-alert :model-value="true" variant="primary">A simple primary alert with <a href="javascript:void(0);" class="alert-link">an example link</a>. Give it a click if you like. </b-alert>
            <b-alert :model-value="true" variant="secondary">A simple secondary alert with <a href="javascript:void(0);" class="alert-link">an example link</a>. Give it a click if you like. </b-alert>
            <b-alert :model-value="true" variant="success">A simple success alert with <a href="javascript:void(0);" class="alert-link">an example link</a>. Give it a click if you like. </b-alert>
            <b-alert :model-value="true" variant="danger" class="mb-0">A simple danger alert with <a href="javascript:void(0);" class="alert-link">an example link</a>. Give it a click if you like. </b-alert>
          </div>
        </UIComponentCard>

        <UIComponentCard title="Icons Alerts Example" id="alert-icon">
          <div class="mt-3">
            <b-alert :model-value="true" variant="primary" class="alert-icon">
              <div class="d-flex align-items-center">
                <div
                  class="avatar-sm rounded bg-primary d-flex justify-content-center align-items-center fs-18 me-2 flex-shrink-0">
                  <i class="bx bx-info-circle text-white"></i>
                </div>
                <div class="flex-grow-1">A simple primary alert—check it out!</div>
              </div>
            </b-alert>
            <b-alert :model-value="true" variant="secondary" class="alert-icon">
              <div class="d-flex align-items-center">
                <div
                  class="avatar-sm rounded bg-secondary d-flex justify-content-center align-items-center fs-18 me-2 flex-shrink-0">
                  <i class="bx bx-x-circle text-white"></i>
                </div>
                <div class="flex-grow-1">A simple secondary alert—check it out!</div>
              </div>
            </b-alert>
            <b-alert :model-value="true" variant="success" class="alert-icon">
              <div class="d-flex align-items-center">
                <div
                  class="avatar-sm rounded bg-success d-flex justify-content-center align-items-center fs-18 me-2 flex-shrink-0">
                  <i class="bx bx-check-shield text-white"></i>
                </div>
                <div class="flex-grow-1">A simple success alert—check it out!</div>
              </div>
            </b-alert>
            <b-alert :model-value="true" variant="danger" class="alert-icon">
              <div class="d-flex align-items-center">
                <div
                  class="avatar-sm rounded bg-danger d-flex justify-content-center align-items-center fs-18 me-2 flex-shrink-0">
                  <i class="bx bx-info-circle text-white"></i>
                </div>
                <div class="flex-grow-1">A simple danger alert—check it out!</div>
              </div>
            </b-alert>
          </div>
        </UIComponentCard>

        <UIComponentCard title="Additional Content Alert Example" id="alert-additional">
          <b-row class="mt-3">
            <b-col xl="6">
              <b-alert :model-value="true" variant="primary" class="mb-3 p-3 mb-xl-0">
                <h4 class="alert-heading">Well done!</h4>
                <p class="mb-0">Aww yeah, you successfully read this important alert message. This example text is
                  going to run a bit longer so that you can see how spacing within an alert works with this kind of
                  content.</p>
                <hr />
                <p class="mb-0">Whenever you need to, be sure to use margin utilities to keep things nice and tidy.</p>
              </b-alert>
            </b-col>
            <b-col xl="6">
              <b-alert :model-value="true" variant="secondary" class="p-3 mb-0">
                <h4 class="alert-heading">Well done!</h4>
                <p class="mb-0">Aww yeah, you successfully read this important alert message. This example text is
                  going to run a bit longer so that you can see how spacing within an alert works with this kind of
                  content.</p>
                <hr />
                <p class="mb-0">Whenever you need to, be sure to use margin utilities to keep things nice and tidy.</p>
              </b-alert>
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
    id: 'overview',
    title: 'Basic Example'
  },
  {
    id: 'alert-dismissible',
    title: 'Alert Dismissible'
  },
  {
    id: 'alert-link',
    title: 'Alert Link'
  },
  {
    id: 'alert-icon',
    title: 'Icons Alert'
  },
  {
    id: 'alert-additional',
    title: 'Additional Content Alert'
  }
];
</script>
