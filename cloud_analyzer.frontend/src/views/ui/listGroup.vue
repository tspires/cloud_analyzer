<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="9">
          <UIComponentCard title="Basic" id="basic">
            <b-row class="mt-3">
              <b-col lg="6">
                <b-list-group>
                  <b-list-group-item>An item</b-list-group-item>
                  <b-list-group-item>A second item</b-list-group-item>
                  <b-list-group-item>A third item</b-list-group-item>
                  <b-list-group-item>A fourth item</b-list-group-item>
                  <b-list-group-item>And a fifth one</b-list-group-item>
                </b-list-group>
              </b-col>
            </b-row>
          </UIComponentCard>

          <UIComponentCard title="Active items" id="active">
            <b-row class="mt-3">
              <b-col lg="6">
                <b-list-group>
                  <b-list-group-item active>An active item</b-list-group-item>
                  <b-list-group-item>A second item</b-list-group-item>
                  <b-list-group-item>A third item</b-list-group-item>
                  <b-list-group-item>A fourth item</b-list-group-item>
                  <b-list-group-item>And a fifth one</b-list-group-item>
                </b-list-group>
              </b-col>
            </b-row>
          </UIComponentCard>

          <UIComponentCard title="Disabled items" id="disabled">
            <b-row class="mt-3">
              <b-col lg="6">
                <b-list-group>
                  <b-list-group-item disabled>A disabled item</b-list-group-item>
                  <b-list-group-item>A second item</b-list-group-item>
                  <b-list-group-item>A third item</b-list-group-item>
                  <b-list-group-item>A fourth item</b-list-group-item>
                  <b-list-group-item>And a fifth one</b-list-group-item>
                </b-list-group>
              </b-col>
            </b-row>
          </UIComponentCard>

          <UIComponentCard title="Links and buttons" id="links-buttons">
            <b-row class="p-3">
              <b-col md="6">
                <b-list-group>
                  <b-list-group-item href="#" active>The current link item</b-list-group-item>
                  <b-list-group-item href="#">A second link item</b-list-group-item>
                  <b-list-group-item href="#">A third link item</b-list-group-item>
                  <b-list-group-item href="#">A fourth link item</b-list-group-item>
                  <b-list-group-item href="#" disabled>A disabled link item</b-list-group-item>
                </b-list-group>
              </b-col>
              <b-col md="6">
                <b-list-group>
                  <b-list-group-item active>The current button</b-list-group-item>
                  <b-list-group-item>A second button item</b-list-group-item>
                  <b-list-group-item>A third button item</b-list-group-item>
                  <b-list-group-item>A fourth button item</b-list-group-item>
                  <b-list-group-item disabled>A disabled button item</b-list-group-item>
                </b-list-group>
              </b-col>
            </b-row>
          </UIComponentCard>

          <UIComponentCard title="Flush" id="flush">
            <b-row>
              <b-col lg="6">
                <div class="p-3">
                  <b-list-group flush>
                    <b-list-group-item>An item</b-list-group-item>
                    <b-list-group-item>A second item</b-list-group-item>
                    <b-list-group-item>A third item</b-list-group-item>
                    <b-list-group-item>A fourth item</b-list-group-item>
                    <b-list-group-item>And a fifth one</b-list-group-item>
                  </b-list-group>
                </div>
              </b-col>
            </b-row>
          </UIComponentCard>

          <UIComponentCard title="Numbered" id="numbered">
            <b-row class="p-3">
              <b-col md="6">
                <b-list-group numbered>
                  <b-list-group-item> A list item</b-list-group-item>
                  <b-list-group-item> A list item</b-list-group-item>
                  <b-list-group-item> A list item</b-list-group-item>
                </b-list-group>
              </b-col>
              <b-col md="6">
                <b-list-group numbered>
                  <b-list-group-item class="d-flex justify-content-between align-items-start">
                    <div class="ms-2 me-auto">
                      <div class="fw-bold">Subheading</div>
                      Content for list item
                    </div>
                    <b-badge variant="primary" pill>14</b-badge>
                  </b-list-group-item>
                  <b-list-group-item class="d-flex justify-content-between align-items-start">
                    <div class="ms-2 me-auto">
                      <div class="fw-bold">Subheading</div>
                      Content for list item
                    </div>
                    <b-badge variant="primary" pill>14</b-badge>
                  </b-list-group-item>
                  <b-list-group-item class="d-flex justify-content-between align-items-start">
                    <div class="ms-2 me-auto">
                      <div class="fw-bold">Subheading</div>
                      Content for list item
                    </div>
                    <b-badge variant="primary" pill>14</b-badge>
                  </b-list-group-item>
                </b-list-group>
              </b-col>
            </b-row>
          </UIComponentCard>

          <UIComponentCard title="Horizontal" id="horizontal">
            <b-row class="mt-3">
              <b-col lg="6">
                <div class="d-flex flex-column gap-2">
                  <b-list-group horizontal>
                    <b-list-group-item>An item</b-list-group-item>
                    <b-list-group-item>A second item</b-list-group-item>
                    <b-list-group-item>A third item</b-list-group-item>
                  </b-list-group>
                  <b-list-group horizontal>
                    <b-list-group-item>An item</b-list-group-item>
                    <b-list-group-item>A second item</b-list-group-item>
                    <b-list-group-item>A third item</b-list-group-item>
                  </b-list-group>
                  <b-list-group horizontal>
                    <b-list-group-item>An item</b-list-group-item>
                    <b-list-group-item>A second item</b-list-group-item>
                    <b-list-group-item>A third item</b-list-group-item>
                  </b-list-group>
                  <b-list-group horizontal>
                    <b-list-group-item>An item</b-list-group-item>
                    <b-list-group-item>A second item</b-list-group-item>
                    <b-list-group-item>A third item</b-list-group-item>
                  </b-list-group>
                  <b-list-group horizontal>
                    <b-list-group-item>An item</b-list-group-item>
                    <b-list-group-item>A second item</b-list-group-item>
                    <b-list-group-item>A third item</b-list-group-item>
                  </b-list-group>
                  <b-list-group horizontal>
                    <b-list-group-item>An item</b-list-group-item>
                    <b-list-group-item>A second item</b-list-group-item>
                    <b-list-group-item>A third item</b-list-group-item>
                  </b-list-group>
                </div>
              </b-col>
            </b-row>
          </UIComponentCard>

          <UIComponentCard title="Contextual classes" id="contextual-classes">
            <b-row class="mt-3">
              <b-col lg="6">
                <b-list-group>
                  <b-list-group-item>A simple default list group item</b-list-group-item>
                  <b-list-group-item variant="primary">A simple primary list group item</b-list-group-item>
                  <b-list-group-item variant="secondary">A simple secondary list group item</b-list-group-item>
                  <b-list-group-item variant="success">A simple success list group item</b-list-group-item>
                  <b-list-group-item variant="danger">A simple danger list group item</b-list-group-item>
                  <b-list-group-item variant="warning">A simple warning list group item</b-list-group-item>
                  <b-list-group-item variant="info">A simple info list group item</b-list-group-item>
                  <b-list-group-item variant="light">A simple light list group item</b-list-group-item>
                  <b-list-group-item variant="dark">A simple dark list group item</b-list-group-item>
                </b-list-group>
              </b-col>
            </b-row>
          </UIComponentCard>

          <UIComponentCard title="Custom content" id="custom-content">
            <b-row class="mt-3">
              <b-col lg="6">
                <b-list-group>
                  <b-list-group-item active>
                    <div class="d-flex w-100 justify-content-between">
                      <h5 class="mb-1 text-reset">List group item heading</h5>
                      <small>3 days ago</small>
                    </div>
                    <p class="mb-1">Some placeholder content in a paragraph.</p>
                    <small>And some small print.</small>
                  </b-list-group-item>
                  <b-list-group-item>
                    <div class="d-flex w-100 justify-content-between">
                      <h5 class="mb-1">List group item heading</h5>
                      <small class="text-muted">3 days ago</small>
                    </div>
                    <p class="mb-1">Some placeholder content in a paragraph.</p>
                    <small class="text-muted">And some muted small print.</small>
                  </b-list-group-item>
                  <b-list-group-item>
                    <div class="d-flex w-100 justify-content-between">
                      <h5 class="mb-1">List group item heading</h5>
                      <small class="text-muted">3 days ago</small>
                    </div>
                    <p class="mb-1">Some placeholder content in a paragraph.</p>
                    <small class="text-muted">And some muted small print.</small>
                  </b-list-group-item>
                </b-list-group>
              </b-col>
            </b-row>
          </UIComponentCard>

          <UIComponentCard title="Checkboxes and radios" id="checkboxes-radios">
            <b-row class="mt-3">
              <b-col lg="6">
                <b-list-group>
                  <b-list-group-item>
                    <b-form-checkbox class="me-1" id="checkbox-1" name="checkbox-1"> First checkbox</b-form-checkbox>
                  </b-list-group-item>
                  <b-list-group-item>
                    <b-form-checkbox class="me-1" id="checkbox-2" name="checkbox-2"> Second checkbox</b-form-checkbox>
                  </b-list-group-item>
                  <b-list-group-item>
                    <b-form-checkbox class="me-1" id="checkbox-3" name="checkbox-3"> Third checkbox</b-form-checkbox>
                  </b-list-group-item>
                </b-list-group>
              </b-col>
            </b-row>
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
    id: 'basic',
    title: 'Basic'
  },
  {
    id: 'active',
    title: 'Active items'
  },
  {
    id: 'disabled',
    title: 'Disabled items'
  },
  {
    id: 'links-buttons',
    title: 'Links and buttons'
  },
  {
    id: 'flush',
    title: 'Flush'
  },
  {
    id: 'numbered',
    title: 'Numbered'
  },
  {
    id: 'horizontal',
    title: 'Horizontal'
  },
  {
    id: 'contextual-classes',
    title: 'Contextual classes'
  },
  {
    id: 'custom-content',
    title: 'Custom content'
  },
  {
    id: 'checkboxes-radios',
    title: 'Checkboxes and Radios'
  }
]
</script>
