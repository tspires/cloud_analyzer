<template>
  <li :class="!mail.isRead && 'unread'">
    <div class="col-mail col-mail-1">
      <div class="checkbox-wrapper-mail">
        <input type="checkbox" :id="mail.id" />
        <label :for="mail.id" class="toggle"></label>
      </div>
      <span class="star-toggle bx bxs-star text-warning" v-if="mail.isStarred"></span>
      <span class="star-toggle bx bx-star" v-else></span>
      <span class="bx bxs-tag-alt important-toggle text-warning" v-if="mail.isImportant"></span>
      <span class="bx bx-tag-alt important-toggle" v-else></span>
      <a @click="toggleReadOffcanvas" class="title" role="button">{{ mail.sender }}</a>
    </div>
    <div class="col-mail col-mail-2">
      <a @click="toggleReadOffcanvas" class="subject" role="button">
        {{ mail.subject }} &nbsp;&ndash;&nbsp;
        <span v-if="mail.message">
          {{ mail.message }}
        </span>
        <b-badge variant="light" class="border text-dark fw-semibold ms-1" v-for="(attach, idx) in mail.attachments" :key="idx">
          <i class="bx bx-images text-primary me-2" v-if="mail.attachType === 'image'" />
          <i class="bx bxs-file-pdf text-danger text-primary me-2" v-if="mail.attachType === 'pdf'" />
          <i class="bx bxs-file-doc text-blue me-2" v-if="mail.attachType === 'doc'" />
          {{ attach }}
        </b-badge>
        <b-badge variant="light" class="border text-dark fw-semibold rounded-circle" v-if="mail.badge">
          {{ mail.badge }}
        </b-badge>
      </a>
      <div class="date">{{ mail.date }}</div>
    </div>
  </li>
</template>
<script setup lang="ts">
defineProps(['toggleReadOffcanvas', 'mail'])
</script>
