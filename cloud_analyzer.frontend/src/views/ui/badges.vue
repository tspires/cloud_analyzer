<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="9">
          <UIComponentCard title="Heading" id="heading">
            <div class="mt-3">
              <h1>
                h1.Example heading
                <b-badge variant="primary">New</b-badge>
              </h1>
              <h2>
                h2.Example heading
                <b-badge variant="secondary">New</b-badge>
              </h2>
              <h3>
                h3.Example heading
                <b-badge variant="success">New</b-badge>
              </h3>
              <h4>
                h4.Example heading
                <b-badge variant="info">New</b-badge>
              </h4>
              <h5>
                h5.Example heading
                <b-badge variant="warning">New</b-badge>
              </h5>
              <h6 class="mb-0">
                h6.Example heading
                <b-badge variant="danger">New</b-badge>
              </h6>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Default & Pill Badges" id="default_pill_badges">
            <div class="my-3">
              <b-badge variant="primary" class="me-1">Primary</b-badge>
              <b-badge variant="secondary" class="me-1">Secondary</b-badge>
              <b-badge variant="success" class="me-1">Success</b-badge>
              <b-badge variant="info" class="me-1">Info</b-badge>
              <b-badge variant="warning" class="me-1">Warning</b-badge>
              <b-badge variant="danger" class="me-1">Danger</b-badge>
              <b-badge variant="dark" class="me-1">Dark</b-badge>
              <b-badge :variant="null" class="bg-purple me-1">Purple</b-badge>
              <b-badge :variant="null" class="bg-pink me-1">Pink</b-badge>
              <b-badge :variant="null" class="bg-orange me-1">Orange</b-badge>
            </div>

            <div>
              <b-badge pill variant="primary" class="me-1">Primary</b-badge>
              <b-badge pill variant="secondary" class="me-1">Secondary</b-badge>
              <b-badge pill variant="success" class="me-1">Success</b-badge>
              <b-badge pill variant="info" class="me-1">Info</b-badge>
              <b-badge pill variant="warning" class="me-1">Warning</b-badge>
              <b-badge pill variant="danger" class="me-1">Danger</b-badge>
              <b-badge pill variant="dark" class="me-1">Dark</b-badge>
              <b-badge pill :variant="null" class="bg-purple me-1">Purple</b-badge>
              <b-badge pill :variant="null" class="bg-pink me-1">Pink</b-badge>
              <b-badge pill :variant="null" class="bg-orange me-1">Orange</b-badge>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Outline & Outline Pill Badges" id="outline_badges">
            <div class="my-3">
              <b-badge :variant="null" class="badge-outline-primary me-1">Primary</b-badge>
              <b-badge :variant="null" class="badge-outline-secondary me-1">Secondary</b-badge>
              <b-badge :variant="null" class="badge-outline-success me-1">Success</b-badge>
              <b-badge :variant="null" class="badge-outline-info me-1">Info</b-badge>
              <b-badge :variant="null" class="badge-outline-warning me-1">Warning</b-badge>
              <b-badge :variant="null" class="badge-outline-danger me-1">Danger</b-badge>
              <b-badge :variant="null" class="badge-outline-dark me-1">Dark</b-badge>
              <b-badge :variant="null" class="badge-outline-purple me-1">Purple</b-badge>
              <b-badge :variant="null" class="badge-outline-pink me-1">Pink</b-badge>
              <b-badge :variant="null" class="badge-outline-orange me-1">Orange</b-badge>
            </div>
            <div>
              <b-badge :variant="null" pill class="badge-outline-primary me-1">Primary</b-badge>
              <b-badge :variant="null" pill class="badge-outline-secondary me-1">Secondary</b-badge>
              <b-badge :variant="null" pill class="badge-outline-success me-1">Success</b-badge>
              <b-badge :variant="null" pill class="badge-outline-info me-1">Info</b-badge>
              <b-badge :variant="null" pill class="badge-outline-warning me-1">Warning</b-badge>
              <b-badge :variant="null" pill class="badge-outline-danger me-1">Danger</b-badge>
              <b-badge :variant="null" pill class="badge-outline-dark me-1">Dark</b-badge>
              <b-badge :variant="null" pill class="badge-outline-purple me-1">Purple</b-badge>
              <b-badge :variant="null" pill class="badge-outline-pink me-1">Pink</b-badge>
              <b-badge :variant="null" pill class="badge-outline-orange me-1">Orange</b-badge>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Soft & Soft Pill Badges" id="soft_badges">
            <div class="my-3">
              <b-badge :variant="null" class="badge-soft-primary me-1">Primary</b-badge>
              <b-badge :variant="null" class="badge-soft-secondary me-1">Secondary</b-badge>
              <b-badge :variant="null" class="badge-soft-success me-1">Success</b-badge>
              <b-badge :variant="null" class="badge-soft-info me-1">Info</b-badge>
              <b-badge :variant="null" class="badge-soft-warning me-1">Warning</b-badge>
              <b-badge :variant="null" class="badge-soft-danger me-1">Danger</b-badge>
              <b-badge :variant="null" class="badge-soft-dark me-1">Dark</b-badge>
              <b-badge :variant="null" class="badge-soft-purple me-1">Purple</b-badge>
              <b-badge :variant="null" class="badge-soft-pink me-1">Pink</b-badge>
              <b-badge :variant="null" class="badge-soft-orange me-1">Orange</b-badge>
            </div>
            <div>
              <b-badge :variant="null" pill class="badge-soft-primary me-1">Primary</b-badge>
              <b-badge :variant="null" pill class="badge-soft-secondary me-1">Secondary</b-badge>
              <b-badge :variant="null" pill class="badge-soft-success me-1">Success</b-badge>
              <b-badge :variant="null" pill class="badge-soft-info me-1">Info</b-badge>
              <b-badge :variant="null" pill class="badge-soft-warning me-1">Warning</b-badge>
              <b-badge :variant="null" pill class="badge-soft-danger me-1">Danger</b-badge>
              <b-badge :variant="null" pill class="badge-soft-dark me-1">Dark</b-badge>
              <b-badge :variant="null" pill class="badge-soft-purple me-1">Purple</b-badge>
              <b-badge :variant="null" pill class="badge-soft-pink me-1">Pink</b-badge>
              <b-badge :variant="null" pill class="badge-soft-orange me-1">Orange</b-badge>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Buttons & Position" id="component_badges">
            <div class="my-3">
              <b-button variant="primary" class="me-1 mb-1">
                Notifications
                <b-badge variant="danger" class="ms-1">4</b-badge>
              </b-button>
              <b-button variant="outline-primary" class="me-1 mb-1">
                Notifications
                <b-badge variant="primary" class="ms-1">new</b-badge>
              </b-button>
              <b-button :variant="null" class="btn-soft-primary me-1 mb-1">
                Notifications
                <b-badge variant="primary" class="ms-1">11</b-badge>
              </b-button>
              <a href="javascript:void(0);" class="btn me-1 mb-1">
                Notifications
                <b-badge variant="primary" class="ms-1">90+</b-badge>
              </a>
            </div>

            <div>
              <b-button variant="primary" class="position-relative me-3">
                Inbox
                <span
                    class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger border border-light">99+</span>
              </b-button>
              <b-button variant="primary" class="position-relative">
                Profile
                <span
                    class="position-absolute top-0 start-100 translate-middle p-1 bg-danger border border-light rounded-circle"></span>
              </b-button>
            </div>
          </UIComponentCard>
        </b-col>

        <b-col xl="3">
          <AnchorNavigation :elements="anchorNavigation"/>
        </b-col>
      </b-row>
  </VerticalLayout>
</template>

<script lang="ts" setup>
import VerticalLayout from "@/layouts/VerticalLayout.vue";

import AnchorNavigation from '@/components/AnchorNavigation.vue'
import UIComponentCard from '@/components/UIComponentCard.vue'

const anchorNavigation = [
  {
    id: 'heading',
    title: 'Heading'
  },
  {
    id: 'default_pill_badges',
    title: 'Default & Pill Badges'
  },
  {
    id: 'outline_badges',
    title: 'Outline & Outline Pill Badges'
  },
  {
    id: 'soft_badges',
    title: 'Soft & Soft Pill Badges'
  },
  {
    id: 'component_badges',
    title: 'Buttons & Position'
  }
]
</script>
