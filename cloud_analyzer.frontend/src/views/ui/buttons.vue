<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="9">
          <UIComponentCard title="Default Buttons" id="default">
            <div class="button-list mt-3">
              <b-button variant="primary">Primary</b-button>
              <b-button variant="secondary">Secondary</b-button>
              <b-button variant="success">Success</b-button>
              <b-button variant="info">Info</b-button>
              <b-button variant="warning">Warning</b-button>
              <b-button variant="danger">Danger</b-button>
              <b-button variant="dark">Dark</b-button>
              <b-button :variant="null" class="btn-purple">Purple</b-button>
              <b-button :variant="null" class="btn-pink">Pink</b-button>
              <b-button :variant="null" class="btn-orange">Orange</b-button>
              <b-button variant="light">Light</b-button>
              <b-button variant="link">Link</b-button>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Rounded Buttons" id="rounded">
            <div class="button-list mt-3">
              <b-button variant="primary" pill>Primary</b-button>
              <b-button variant="secondary" pill>Secondary</b-button>
              <b-button variant="success" pill>Success</b-button>
              <b-button variant="info" pill>Info</b-button>
              <b-button variant="warning" pill>Warning</b-button>
              <b-button variant="danger" pill>Danger</b-button>
              <b-button variant="dark" pill>Dark</b-button>
              <b-button :variant="null" pill class="btn-purple">Purple</b-button>
              <b-button :variant="null" pill class="btn-pink">Pink</b-button>
              <b-button :variant="null" pill class="btn-orange">Orange</b-button>
              <b-button variant="light" pill>Light</b-button>
              <b-button variant="link" pill>Link</b-button>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Outline Buttons" id="outline">
            <div class="button-list mt-3">
              <b-button variant="outline-primary">Primary</b-button>
              <b-button variant="outline-secondary">Secondary</b-button>
              <b-button variant="outline-success">Success</b-button>
              <b-button variant="outline-info">Info</b-button>
              <b-button variant="outline-warning">Warning</b-button>
              <b-button :variant="null" class="btn-outline-purple">Purple</b-button>
              <b-button :variant="null" class="btn-outline-pink">Pink</b-button>
              <b-button :variant="null" class="btn-outline-orange">Orange</b-button>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Outline Rounded Buttons" id="outline-rounded">
            <div class="button-list mt-3">
              <b-button variant="outline-primary" pill>Primary</b-button>
              <b-button variant="outline-secondary" pill>Secondary</b-button>
              <b-button variant="outline-success" pill>Success</b-button>
              <b-button variant="outline-info" pill>Info</b-button>
              <b-button variant="outline-warning" pill>Warning</b-button>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Soft Buttons" id="soft">
            <div class="button-list mt-3">
              <b-button type="button" :variant="null" class="btn-soft-primary">Primary</b-button>
              <b-button type="button" :variant="null" class="btn-soft-secondary">Secondary</b-button>
              <b-button type="button" :variant="null" class="btn-soft-success">Success</b-button>
              <b-button type="button" :variant="null" class="btn-soft-info">Info</b-button>
              <b-button type="button" :variant="null" class="btn-soft-warning">Warning</b-button>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Soft Rounded Buttons" id="soft-rounded">
            <div class="button-list mt-3">
              <b-button type="button" :variant="null" class="btn-soft-primary rounded-pill">Primary</b-button>
              <b-button type="button" :variant="null" class="btn-soft-secondary rounded-pill">Secondary</b-button>
              <b-button type="button" :variant="null" class="btn-soft-success rounded-pill">Success</b-button>
              <b-button type="button" :variant="null" class="btn-soft-info rounded-pill">Info</b-button>
              <b-button type="button" :variant="null" class="btn-soft-warning rounded-pill">Warning</b-button>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Button Width" id="width">
            <div class="button-list mt-3">
              <b-button variant="primary" class="width-xl">Extra Large</b-button>
              <b-button variant="secondary" class="width-lg">Large</b-button>
              <b-button variant="success" class="width-md">Middle</b-button>
              <b-button variant="info" class="width-sm">Small</b-button>
              <b-button variant="warning" class="width-xs">Xs</b-button>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Button Sizes" id="sizes">
            <div class="button-list mt-3">
              <b-button variant="primary" size="lg">Large</b-button>
              <b-button variant="secondary">Normal</b-button>
              <b-button variant="success" size="sm">Small</b-button>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Disabled Button" id="disabled">
            <div class="button-list mt-3">
              <b-button variant="primary" disabled>Primary</b-button>
              <b-button variant="secondary" disabled>Secondary</b-button>
              <b-button variant="success" disabled>Success</b-button>
              <b-button variant="info" disabled>Info</b-button>
              <b-button variant="warning" disabled>Warning</b-button>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Icon Button" id="icon">
            <div class="button-list mt-3">
              <b-button variant="primary">
                <i class="bx bx-heart"></i>
              </b-button>
              <b-button variant="secondary">
                <i class="bx bx-user-voice"></i>
              </b-button>
              <b-button variant="success">
                <i class="bx bx-check-double"></i>
              </b-button>
              <b-button variant="info"><i class="bx bx-cloud me-1"></i>Cloud Hosting</b-button>
              <b-button variant="warning"><i class="bx bx-info-circle me-1"></i>Warning</b-button>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Button Group" id="group">
            <b-row class="mt-3">
              <b-col md="6">
                <b-button-group class="mb-1 me-1">
                  <b-button variant="light">Left</b-button>
                  <b-button variant="light">Middle</b-button>
                  <b-button variant="light">Right</b-button>
                </b-button-group>
                <b-button-group class="mb-1 me-1">
                  <b-button variant="light">1</b-button>
                  <b-button variant="light">2</b-button>
                  <b-button variant="secondary">3</b-button>
                  <b-button variant="light">4</b-button>
                </b-button-group>
                <b-button-group class="mb-1 me-1">
                  <b-button variant="light">5</b-button>
                  <b-button variant="secondary">6</b-button>
                  <b-button variant="light">7</b-button>
                  <button id="dropdown" type="button" class="btn btn-light dropdown-toggle" data-bs-toggle="dropdown"
                    aria-expanded="false">
                    Dropdown
                  </button>
                  <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="dropdown" style="">
                    <li><a class="dropdown-item" href="javascript:void(0);">Dropdown link</a></li>
                    <li><a class="dropdown-item" href="javascript:void(0);">Dropdown link</a></li>
                  </ul>
                </b-button-group>
              </b-col>
              <b-col md="6">
                <b-button-group vertical class="me-4">
                  <b-button variant="light">Top</b-button>
                  <b-button variant="light">Middle</b-button>
                  <b-button variant="light">Bottom</b-button>
                </b-button-group>

                <b-button-group vertical>
                  <b-button type="button" variant="light">Button 1</b-button>
                  <b-button type="button" variant="light">Button 2</b-button>
                  <button id="verticalDropdown" type="button" class="btn btn-light dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                    Button 3
                  </button>
                  <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="verticalDropdown">
                    <li><a class="dropdown-item" href="javascript:void(0);">Dropdown link</a></li>
                    <li><a class="dropdown-item" href="javascript:void(0);">Dropdown link</a></li>
                  </ul>
                </b-button-group>
              </b-col>
            </b-row>
          </UIComponentCard>

          <UIComponentCard title="Block Button" id="block">
            <div class="d-grid gap-2 mt-3">
              <b-button variant="primary" size="lg">Block Button</b-button>
              <b-button variant="secondary">Block Button</b-button>
              <b-button variant="light" size="sm">Block Button</b-button>
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

const anchorNavigation = [
  {
    id: 'default',
    title: 'Default Example'
  },
  {
    id: 'rounded',
    title: 'Rounded Buttons'
  },
  {
    id: 'outline',
    title: 'Outline Buttons'
  },
  {
    id: 'outline-rounded',
    title: 'Outline Rounded Buttons'
  },
  {
    id: 'soft',
    title: 'Soft Buttons'
  },
  {
    id: 'soft-rounded',
    title: 'Soft Rounded Buttons'
  },
  {
    id: 'width',
    title: 'Button Width'
  },
  {
    id: 'sizes',
    title: 'Button Sizes'
  },
  {
    id: 'disabled',
    title: 'Disabled Button'
  },
  {
    id: 'icon',
    title: 'Icon Button'
  },
  {
    id: 'group',
    title: 'Button Group'
  },
  {
    id: 'block',
    title: 'Block Button'
  }
];
</script>
