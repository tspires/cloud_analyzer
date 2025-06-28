<template>
  <div :class="customClass ?? 'logo-box'">
    <router-link to="/" class="logo-dark">
      <img :src="logoSmall" :height="smLogoHeight" :class="smLogoClass ?? 'logo-sm'" alt="logo sm">
      <img :src="logoDark" :height="logoHeight" :class="logoClass ?? 'logo-lg'" alt="logo dark">
    </router-link>

    <router-link to="/" class="logo-light">
      <img :src="logoSmall" :height="smLogoHeight" :class="smLogoClass ?? 'logo-sm'" alt="logo sm">
      <img :src="logoLight" :height="logoHeight" :class="logoClass ?? 'logo-lg'" alt="logo light">
    </router-link>
  </div>
</template>

<script setup lang="ts">
import logoSmall from "@/assets/images/logo-sm.png";
import logoDark from "@/assets/images/logo-dark.png";
import logoLight from "@/assets/images/logo-light.png";

type PropsType = {
  customClass?: string;
  logoClass?: string;
  smLogoClass?: string;
  logoHeight?: number;
  smLogoHeight?: number;
};

defineProps<PropsType>();
</script>
