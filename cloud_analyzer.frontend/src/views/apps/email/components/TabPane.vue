<template>
  <div class="tab-pane fade" id="email-starred" :class="showTab === tab && 'show active'">
    <template v-if="tab === 'email-trash'">
      <hr />
      <div class="text-center mt-2">
        <p class="mb-0">
          Messages that have been in Trash more than 30 days will be automatically deleted.
          <a href="javascript: void(0);" class="text-primary ms-2">Empty Trash Now</a>
        </p>
      </div>
      <hr class="mb-3" />
    </template>

    <template v-if="tab === 'email-draft'">
      <hr />
      <div class="text-center mt-2">
        <p class="mb-0">You don't have any saved drafts.</p>
        <p class="mb-0">Saving a draft allows you to keep a message you aren't ready to send yet.</p>
      </div>
      <hr class="mb-0" />
    </template>

    <template v-else>
      <ul class="message-list mb-0">
        <template v-for="(mail, idx) in filteredMails" :key="idx">
          <MailCard :mail="mail" :toggleReadOffcanvas="toggleReadOffcanvas" />
        </template>
      </ul>
    </template>
  </div>
</template>
<script setup lang="ts">
import MailCard from '@/views/apps/email/components/MailCard.vue'

defineProps(['tab', 'filteredMails', 'showTab', 'toggleReadOffcanvas'])
</script>
