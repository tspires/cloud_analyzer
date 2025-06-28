<template>
  <li :class="className">
    <a class="menu-arrow" :class="`${menuItemActive(item.key, currentRouteName) && 'active'} ${linkClassName}`" v-b-toggle="item.key" role="button">
      <span v-if="item.icon" class="nav-icon">
        <Icon :icon="item.icon" />
      </span>
      <span class="nav-text"> {{ item.label }} </span>
      <span v-if="item.badge" :class="`badge badge-pill text-end bg-${item.badge.variant}`">{{ item.badge.text }}</span>
    </a>
    <b-collapse :id="item.key" :visible="menuItemActive(item.key, currentRouteName)">
      <ul :class="subMenuClassName">
        <template v-for="(link, idx) in item.children || []" :key="idx">
          <MenuItemWithChildren v-if="link.children" :item="link" className="sub-nav-item"
            subMenuClassName="nav sub-navbar-nav" linkClassName="sub-nav-link" />
          <MenuItem v-else :item="link" className="sub-nav-item" linkClassName="sub-nav-link" />
        </template>
      </ul>
    </b-collapse>
  </li>
</template>

<script setup lang="ts">
import MenuItem from '@/components/AppMenu/MenuItem.vue';
import { menuItemActive } from '@/helpers/menu';
import type { SubMenus } from '@/types/menu';
import { Icon } from '@iconify/vue';
import router from '@/router';

defineProps<SubMenus>();

const currentRouteName = router.currentRoute.value.name;
</script>
