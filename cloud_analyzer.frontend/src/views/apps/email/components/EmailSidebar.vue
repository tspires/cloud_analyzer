<template>
  <simplebar class="card h-100 mb-0" data-simplebar>
    <b-card-body>
      <div class="d-grid">
        <b-button type="button" variant="danger" @click="toggleModal">Compose</b-button>
      </div>

      <div class="nav flex-column mt-3" id="email-tab" role="tablist" aria-orientation="vertical">
        <template v-for="(item, idx) in navLinkData" :key="idx">
          <a class="nav-link px-0 py-1" :class="showTab === item.link && 'active'" :id="`${item.link}-tab`" href="#" @click="props.filterMails(item.category, item.link)" v-if="!item.isLabel && !item.isTitle">
            <template v-if="!idx">
              <span class="text-danger fw-bold">
                <i class="bx bxs-inbox fs-16 me-2 align-middle"></i>{{ item.title }}
                <b-badge :variant="null" class="float-end ms-2" :class="`badge-soft-${item.badgeVariant}`" v-if="item.badge">
                  {{ item.badge }}
                </b-badge>
              </span>
            </template>
            <template v-else>
              <i class="bx fs-16 align-middle me-2" :class="item.icon"></i>{{ item.title }}
              <b-badge :variant="null" class="float-end ms-2" :class="`badge-soft-${item.badgeVariant}`" v-if="item.badge">
                {{ item.badge }}
              </b-badge>
            </template>
          </a>
          <h6 class="text-uppercase mt-4" v-if="item.isTitle">{{ item.title }}</h6>
          <a class="nav-link px-0 py-1" :class="showTab === item.link && 'active'" :id="`${item.link}-tab`" href="#" @click="props.filterMails(item.category, item.link)" v-if="item.isLabel"> <i class="bx bxs-circle font-13 me-2" :class="`text-${item.variant}`"></i>{{ item.title }} </a>
        </template>
      </div>

      <div class="mt-5">
        <h4><b-badge pill :variant="null" class="p-1 px-2 badge-soft-secondary">FREE</b-badge></h4>
        <h6 class="text-uppercase mt-3">Storage</h6>
        <b-progress value="46" variant="success" class="progress-sm my-2" />
        <p class="text-muted font-13 mb-0">7.02 GB (46%) of 15 GB used</p>
      </div>
    </b-card-body>
  </simplebar>

  <b-modal v-model="modal" modal-class="compose-mail" size="lg" title="New Message" header-class="overflow-hidden bg-primary p-2" dialog-class="modal-lg" title-class="text-white" body-class="p-4" hide-footer>
    <div class="overflow-hidden">
      <div class="mb-2">
        <input type="email" class="form-control" id="toEmail" placeholder="To: " />
      </div>
      <div class="mb-2">
        <input type="text" class="form-control" id="subject" placeholder="Subject " />
      </div>

      <div class="my-2">
        <QuillEditor theme="snow" :toolbar="toolbar" style="height: 200px" content="" content-type="html" />
      </div>

      <div class="d-flex float-end">
        <DropDown custom-class="dropdown me-1">
          <a href="javascript:void(0);" class="dropdown-toggle arrow-none btn btn-light" data-bs-toggle="dropdown" aria-expanded="false">
            <i class="bx bx-dots-vertical-rounded fs-18"></i>
          </a>
          <div class="dropdown-menu dropdown-menu-up">
            <a href="javascript:void(0);" class="dropdown-item">Default to full screen</a>
            <div class="dropdown-divider"></div>
            <a href="javascript:void(0);" class="dropdown-item">Label</a>
            <a href="javascript:void(0);" class="dropdown-item">Palin text mode</a>
            <div class="dropdown-divider"></div>
            <a href="javascript:void(0);" class="dropdown-item">Smart Compose Feedback</a>
          </div>
        </DropDown>
        <a href="javascript: void(0);" class="btn btn-light compose-close"><i class="bx bxs-trash fs-18"></i></a>
      </div>
      <div>
        <a href="javascript: void(0);" class="btn btn-primary">Send</a>
      </div>
    </div>
  </b-modal>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import simplebar from 'simplebar-vue'
import { QuillEditor } from '@vueup/vue-quill'
import { navLinkData } from '@/views/apps/email/components/data'
import DropDown from '@/components/DropDown.vue'

const toolbar = [[{ font: [] }, { size: [] }], ['bold', 'italic', 'underline', 'strike'], [{ color: [] }, { background: [] }], [{ script: 'super' }, { script: 'sub' }], [{ header: [false, 1, 2, 3, 4, 5, 6] }, 'blockquote', 'code-block'], [{ list: 'ordered' }, { list: 'bullet' }, { indent: '-1' }, { indent: '+1' }], ['direction', { align: [] }], ['link', 'image', 'video'], ['clean']]

const modal = ref(false)

const toggleModal = () => {
  modal.value = !modal.value
}

const props = defineProps(['filterMails', 'showTab'])
</script>
