<template>
  <div>
    <b-offcanvas placement="end" class="border-0" header-class="d-flex align-items-center bg-primary p-3"
      body-class="p-0" id="theme-settings">
      <template v-slot:header>
        <h5 class="text-white m-0">Theme Settings</h5>
        <button type="button" class="btn-close btn-close-white ms-auto" v-b-toggle="'theme-settings'"></button>
      </template>

      <div class="p-0">
        <simplebar class="h-100">
          <div class="p-3 settings-bar">
            <div>
              <h5 class="mb-3 font-16 fw-semibold">Color Scheme</h5>
              <b-form-radio-group stacked v-model="layout.theme" name="theme" @change="setTheme(layout.theme)">
                <b-form-radio value="light">Light</b-form-radio>
                <b-form-radio value="dark">Dark</b-form-radio>
              </b-form-radio-group>
            </div>

            <div>
              <h5 class="my-3 font-16 fw-semibold">Topbar Color</h5>
              <b-form-radio-group stacked v-model="layout.topBarColor" name="topbar-color"
                @change="setTopBarColor(layout.topBarColor)">
                <b-form-radio value="light">Light</b-form-radio>
                <b-form-radio value="dark">Dark</b-form-radio>
              </b-form-radio-group>
            </div>

            <div>
              <h5 class="my-3 font-16 fw-semibold">Menu Color</h5>
              <b-form-radio-group stacked v-model="layout.leftSideBarColor" name="menu-color"
                @change="setLeftSideBarColor(layout.leftSideBarColor)">
                <b-form-radio value="light">Light</b-form-radio>
                <b-form-radio value="dark">Dark</b-form-radio>
              </b-form-radio-group>
            </div>

            <div>
              <h5 class="my-3 font-16 fw-semibold">Sidebar Size</h5>
              <b-form-radio-group stacked v-model="layout.leftSideBarSize" name="menu-size" @change="setLeftSideBarSize(layout.leftSideBarSize)">
                <b-form-radio value="default">Default</b-form-radio>
                <b-form-radio value="condensed">Condensed</b-form-radio>
                <b-form-radio value="hidden">Hidden</b-form-radio>
                <b-form-radio value="sm-hover-active">Small Hover Active</b-form-radio>
                <b-form-radio value="sm-hover">Small Hover</b-form-radio>
              </b-form-radio-group>
            </div>

          </div>
        </simplebar>
      </div>
      <template v-slot:footer>
        <div class="border-top p-3 text-center">
          <b-row>
            <b-col>
              <b-button type="button" variant="danger" class="w-100" id="reset-layout" @click="reset">Reset</b-button>
            </b-col>
          </b-row>
        </div>
      </template>
    </b-offcanvas>
  </div>
</template>

<script setup lang="ts">
import simplebar from 'simplebar-vue';

import { useLayoutStore } from '@/stores/layout';

const useLayout = useLayoutStore();

const { layout, setTheme, setTopBarColor, setLeftSideBarColor, setLeftSideBarSize, reset } = useLayout;
</script>

<style scoped>
.form-check {
  margin: 10px 0;
}
</style>