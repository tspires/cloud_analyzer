<template>
  <div class="main-nav">
    <LogoBox />

    <!-- Menu Toggle Button (sm-hover) -->
    <button type="button" class="button-sm-hover" aria-label="Show Full Sidebar" @click="toggleMenuSize">
      <Icon icon="solar:hamburger-menu-broken" class="button-sm-hover-icon mt-1 me-1"
        style="height: 25px; width: 25px" />
    </button>

    <simplebar class="scrollbar">
      <AppMenu :menu-items="getMenuItems()" />
    </simplebar>
  </div>
</template>

<script setup lang="ts">
import { Icon } from "@iconify/vue";
import simplebar from 'simplebar-vue';
import AppMenu from '@/components/AppMenu/index.vue';
import { getMenuItems } from '@/helpers/menu';
import { useLayoutStore } from '@/stores/layout';
import { onMounted } from 'vue';

const useLayout = useLayoutStore();

const { layout, setLeftSideBarSize } = useLayout;

const toggleMenuSize = () => {
  if (layout.leftSideBarSize === 'sm-hover-active') return setLeftSideBarSize('sm-hover');
  return setLeftSideBarSize('sm-hover-active');
};

const resize = () => {
  if (window.innerWidth < 1140) {
    setLeftSideBarSize('hidden');
  } else {
    setLeftSideBarSize(layout.leftSideBarSize === 'hidden' ? 'sm-hover-active' : layout.leftSideBarSize);
  }
};

onMounted(() => {
  resize();
  window.addEventListener('resize', () => {
    resize();
  });
});

import logoSm from '@/assets/images/logo-sm.png';
import logoDark from '@/assets/images/logo-dark.png';
import logoLight from '@/assets/images/logo-light.png';
</script>