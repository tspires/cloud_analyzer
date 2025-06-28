<template>
  <VerticalLayout>
      <b-row class="g-1">
        <b-col xxl="3">
          <div class="offcanvas-xxl offcanvas-start h-100" id="contactOffcanvas">
            <ContactOffcanvas/>
          </div>

          <div class="d-block d-xl-none">
            <b-offcanvas v-model="contactOffcanvas" class="offcanvas-xxl h-100" placement="start" body-class="p-0 h-100"
                         no-header>
              <ContactOffcanvas/>
            </b-offcanvas>
          </div>
        </b-col>

        <b-col xxl="9">
          <b-card no-body class="position-relative overflow-hidden">
            <b-card-header class="d-flex align-items-center mh-100">
              <b-button variant="light" class="d-xxl-none d-flex align-items-center px-2 me-2" type="button"
                        @click="contactOffcanvas = !contactOffcanvas">
                <i class="bx bx-menu fs-18"></i>
              </b-button>

              <div class="d-flex align-items-center">
                <img :src="avatar4" class="me-2 rounded" height="36" alt="avatar-4"/>
                <div class="d-none d-md-flex flex-column">
                  <h5 class="my-0 fs-16 fw-semibold">
                    <a href="#" class="text-dark" @click="profileOffcanvas = !profileOffcanvas"> Gilbert Chicoine </a>
                  </h5>
                  <p class="mb-0 text-success fw-semibold fst-italic">typing...</p>
                </div>
              </div>

              <div class="flex-grow-1">
                <ul class="list-inline float-end d-flex gap-3 mb-0">
                  <li class="list-inline-item fs-20 d-flex align-items-center mt-1">
                    <a href="javascript: void(0);" class="text-dark" @click="videoToggleModal">
                      <i class="bx bx-video"></i>
                    </a>
                  </li>

                  <li class="list-inline-item fs-20 d-flex align-items-center mt-1">
                    <a href="javascript: void(0);" class="text-dark" @click="voiceToggleModal">
                      <i class="bx bx-phone-call"></i>
                    </a>
                  </li>

                  <li class="list-inline-item fs-20 d-flex align-items-center mt-1">
                    <a href="#" class="text-dark" @click="profileOffcanvas = !profileOffcanvas">
                      <i class="bx bx-user"></i>
                    </a>
                  </li>

                  <li class="list-inline-item fs-20 d-none d-md-flex">
                    <b-dropdown :variant="null" toggle-class="arrow-none text-dark p-0 m-0" menu-class="dropdown-menu-end">
                      <template #button-content>
                        <i class="bx bx-dots-vertical-rounded fs-20"/>
                      </template>
                      <b-dropdown-item><i class="bx bx-user-circle me-2"></i>View Profile</b-dropdown-item>
                      <b-dropdown-item><i class="bx bx-music me-2"></i>Media, Links and Docs</b-dropdown-item>
                      <b-dropdown-item><i class="bx bx-search me-2"></i>Search</b-dropdown-item>
                      <b-dropdown-item><i class="bx bx-image me-2"></i>Wallpaper</b-dropdown-item>
                      <b-dropdown-item><i class="bx bx-right-arrow-circle me-2"></i>More</b-dropdown-item>
                    </b-dropdown>
                  </li>
                </ul>
              </div>
            </b-card-header>

            <div class="chat-box">
              <simplebar class="chat-conversation-list p-3 chatbox-height">
                <template v-for="(content, idx) in chatMessages" :key="idx">
                  <li class="clearfix" :class="content.isSender && 'odd'">
                    <div class="chat-conversation-text ms-0" v-for="(msg, idx) in content.msg" :key="idx">
                      <template v-if="content.isSender">
                        <div class="d-flex justify-content-end">
                          <DropDown customClass="chat-conversation-actions dropstart">
                            <a href="javascript: void(0);" class="ps-1" data-bs-toggle="dropdown" aria-expanded="false">
                              <i class="bx bx-dots-vertical-rounded fs-18"></i>
                            </a>
                            <div class="dropdown-menu">
                              <a class="dropdown-item" href="javascript: void(0);" v-for="(item, idx) in dropdownItem"
                                 :key="idx">
                                <i class="bx me-2" :class="item.icon"></i>
                                {{ item.title }}
                              </a>
                            </div>
                          </DropDown>
                          <div class="chat-ctext-wrap" v-if="!msg.isMedia">
                            <p>{{ msg.text }}</p>
                          </div>
                          <div class="chat-ctext-wrap text-start" v-if="msg.isMedia && msg.mediaContend">
                            <div class="d-flex align-items-center justify-content-center">
                              <div class="flex-shrink-0">
                                <i class="bx fs-24 me-1" :class="msg.mediaContend.type"></i>
                              </div>
                              <div class="flex-grow-1">
                                <a href="javascript:void(0);" class="text-white">{{ msg.mediaContend.title }}</a>
                                <p class="mb-0">
                                  {{ msg.mediaContend.size }}
                                </p>
                              </div>
                            </div>
                          </div>
                        </div>
                      </template>

                      <template v-else>
                        <div class="d-flex">
                          <div class="chat-ctext-wrap">
                            <p v-if="msg.text">{{ msg.text }}</p>
                            <a href="javascript:void(0);" v-if="msg.img" v-for="(image, idx) in msg.img" :key="idx">
                              <img :src="image" alt="attachment" style="height: 84px" class="img-thumbnail me-1"/>
                            </a>
                          </div>
                          <DropDown customClass="chat-conversation-actions dropend">
                            <a href="javascript: void(0);" class="ps-1" data-bs-toggle="dropdown" aria-expanded="false"><i
                                class="bx bx-dots-vertical-rounded fs-18"></i></a>
                            <div class="dropdown-menu">
                              <a class="dropdown-item" href="javascript: void(0);" v-for="(item, idx) in dropdownItem"
                                 :key="idx">
                                <i class="bx me-2" :class="item.icon"></i>
                                {{ item.title }}
                              </a>
                            </div>
                          </DropDown>
                        </div>
                      </template>
                      <p class="text-muted fs-12 mb-0 mt-1" :class="!content.isSender && 'ms-2'"
                         v-if="content.timeStamp && content.msg.length - 1 === idx">{{ content.timeStamp }}<i
                          class="bx bx-check-double ms-1 text-primary" v-if="content.isRead"></i></p>
                    </div>
                  </li>
                </template>
              </simplebar>
              <div class="bg-light bg-opacity-50 p-2">
                <form class="needs-validation" name="chat-form" id="chat-form" @submit.prevent="handleYupSubmit">
                  <b-row class="align-items-center">
                    <div class="col mb-2 mb-sm-0 d-flex">
                      <div class="input-group">
                        <a href="javascript: void(0);"
                           class="btn btn-sm btn-light d-flex align-items-center input-group-text">
                          <i class="bx bx-smile fs-18"></i>
                        </a>
                        <input type="text" class="form-control border-0" placeholder="Enter your message"
                               v-model="messageState.message"/>
                      </div>
                    </div>
                    <div class="col-sm-auto">
                      <div class="">
                        <b-button-group class="btn-toolbar">
                          <a href="javascript: void(0);" class="btn btn-sm btn-light">
                            <i class="bx bx-paperclip fs-18"></i>
                          </a>
                          <a href="javascript: void(0);" class="btn btn-sm btn-light"><i
                              class="bx bx-video fs-18"></i></a>
                          <b-button type="submit" variant="primary" size="sm" class="chat-send">
                            <i class="bx bx-send fs-18"></i>
                          </b-button>
                        </b-button-group>
                      </div>
                    </div>
                    <span v-if="error.length > 0" class="text-danger mt-2">{{ error }}</span>
                  </b-row>
                </form>
              </div>
            </div>
          </b-card>
        </b-col>
      </b-row>
    <!-- Profile Start -->
    <b-offcanvas v-model="profileOffcanvas" class="border-start" :body-scrolling="true" placement="end" body-class="p-0 h-100">
      <template #header>
        <h5 class="text-truncate w-50" id="user-profileLabel">Profile</h5>
        <button type="button" class="btn-close" @click="toggleProfileOffcanvas"></button>
      </template>
      <ProfileOffcanvas/>
    </b-offcanvas>

    <!-- Voice Call Modal -->
    <b-modal v-model="voiceModal" size="sm" content-class="voice-call" body-class="pt-0 text-center"
             header-class="border-0 mt-5 justify-content-center" hide-footer centered>
      <template #header>
        <div class="voice-call-head">
          <img :src="avatar4" class="rounded-circle" alt="avatar-4"/>
        </div>
      </template>
      <h5>Gaston Lapierre</h5>
      <p class="mb-5">Calling...</p>
      <div class="voice-call-action pt-4 pb-2">
        <ul class="list-inline">
          <li class="list-inline-item avatar-sm fw-bold me-2">
            <a href="javascript: void(0);" class="avatar-title rounded-circle bg-soft-secondary text-dark fs-16">
              <i class="bx bx-microphone-off"></i>
            </a>
          </li>
          <li class="list-inline-item avatar fw-bold me-2" data-bs-dismiss="modal">
            <a href="javascript: void(0);" class="avatar-title rounded-circle bg-danger text-white fs-18">
              <i class="bx bx-phone-off"></i>
            </a>
          </li>
          <li class="list-inline-item avatar-sm fw-bold">
            <a href="javascript: void(0);" class="avatar-title rounded-circle bg-soft-secondary text-dark fs-16">
              <i class="bx bx-volume-full"></i>
            </a>
          </li>
        </ul>
      </div>
    </b-modal>

    <!-- Video Call Modal -->
    <b-modal v-model="videoModal" size="sm" content-class="video-call" header-class="border-0 mb-5 justify-content-end"
             hide-footer centered>
      <template #header>
        <div class="video-call-head">
          <img :src="avatar4" class="rounded" alt="avatar-4"/>
        </div>
      </template>
      <div class="video-call-action text-center pt-4 pb-2">
        <ul class="list-inline">
          <li class="list-inline-item avatar-sm fw-bold me-2">
            <a href="javascript: void(0);" class="avatar-title rounded-circle bg-soft-light text-white fs-16">
              <i class="bx bx-microphone-off"></i>
            </a>
          </li>
          <li class="list-inline-item avatar fw-bold me-2">
            <a href="javascript: void(0);" class="avatar-title rounded-circle bg-danger text-white fs-18">
              <i class="bx bx-video-off"/>
            </a>
          </li>
          <li class="list-inline-item avatar-sm fw-bold">
            <a href="javascript: void(0);" class="avatar-title rounded-circle bg-soft-light text-white fs-16">
              <i class="bx bx-volume-full"></i>
            </a>
          </li>
        </ul>
      </div>
    </b-modal>
  </VerticalLayout>
</template>

<script setup lang="ts">
import VerticalLayout from "@/layouts/VerticalLayout.vue";
import {ref, watch, reactive} from 'vue'
import simplebar from 'simplebar-vue'
import DropDown from '@/components/DropDown.vue'

import {chatMsg, dropdownItem} from '@/views/apps/chat/components/data'

import ContactOffcanvas from '@/views/apps/chat/components/ContactOffcanvas.vue'
import ProfileOffcanvas from '@/views/apps/chat/components/ProfileOffcanvas.vue'

import avatar4 from '@/assets/images/users/avatar-4.jpg'

import {object, string} from 'yup'

const chatMessages = ref(chatMsg)

const contactOffcanvas = ref(false)
const profileOffcanvas = ref(false)

const videoModal = ref(false)
const voiceModal = ref(false)

const toggleProfileOffcanvas = () => {
  profileOffcanvas.value = !profileOffcanvas.value
}

const videoToggleModal = () => {
  videoModal.value = !videoModal.value
}

const voiceToggleModal = () => {
  voiceModal.value = !voiceModal.value
}

const error = ref('')

const messageSchema = object({
  message: string().required('Message is Required')
})

const messageState = reactive({
  message: ''
})
const handleYupSubmit = async (event: Event) => {
  await messageSchema
      .validate(messageState)
      .then((res) => {
        error.value = ''
        chatMessages.value.push({
          id: Math.floor(Math.random() * 100 + 20) - 20,
          msg: [{text: res.message}],
          timeStamp: '8:20 am',
          isSender: true,
          isRead: true
        })
        messageState.message = ''
      })
      .catch((e) => {
        return (error.value = e.message)
      })
}

watch(
    chatMessages.value,
    () => {
      setTimeout(() => {
        chatMessages.value.push({
          id: Math.floor(Math.random() * 100 + 20) - 20,
          msg: [{text: 'Server is not connected 😔'}],
          timeStamp: '8:20 am',
          isSender: false
        })
      }, 1000)
    },
    {once: true}
)
</script>
