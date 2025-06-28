<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="9">
          <UIComponentCard title="Default Example" id="default">
            <nav aria-label="breadcrumb" class="mt-3">
              <ol class="breadcrumb py-0">
                <li class="breadcrumb-item active" aria-current="page">Home</li>
              </ol>
            </nav>

            <nav aria-label="breadcrumb">
              <ol class="breadcrumb py-0">
                <li class="breadcrumb-item">
                  <a href="javascript:void(0);">Home</a>
                </li>
                <li class="breadcrumb-item active" aria-current="page">Library</li>
              </ol>
            </nav>

            <nav aria-label="breadcrumb">
              <ol class="breadcrumb mb-0 py-0">
                <li class="breadcrumb-item">
                  <a href="javascript:void(0);">Home</a>
                </li>
                <li class="breadcrumb-item">
                  <a href="javascript:void(0);">Library</a>
                </li>
                <li class="breadcrumb-item active" aria-current="page">Data</li>
              </ol>
            </nav>
          </UIComponentCard>

          <UIComponentCard title="Dividers Breadcrumb" id="dividers_breadcrumb">
            <nav style="--bs-breadcrumb-divider: '>'" aria-label="breadcrumb" class="mt-3">
              <ol class="breadcrumb py-0">
                <li class="breadcrumb-item active" aria-current="page">Home</li>
              </ol>
            </nav>

            <nav style="--bs-breadcrumb-divider: '>'" aria-label="breadcrumb">
              <ol class="breadcrumb py-0">
                <li class="breadcrumb-item">
                  <a href="javascript:void(0);">Home</a>
                </li>
                <li class="breadcrumb-item active" aria-current="page">Library</li>
              </ol>
            </nav>

            <nav style="--bs-breadcrumb-divider: '>'" aria-label="breadcrumb">
              <ol class="breadcrumb mb-0 py-0">
                <li class="breadcrumb-item">
                  <a href="javascript:void(0);">Home</a>
                </li>
                <li class="breadcrumb-item">
                  <a href="javascript:void(0);">Library</a>
                </li>
                <li class="breadcrumb-item active" aria-current="page">Data</li>
              </ol>
            </nav>
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
    id: 'default',
    title: 'Default Example'
  },
  {
    id: 'dividers_breadcrumb',
    title: 'Dividers Breadcrumb'
  }
]
</script>
