<template>
  <VerticalLayout>
      <b-row class="g-1 mb-3">
        <b-col xxl="2">
          <div class="offcanvas-xxl offcanvas-start h-100" tabindex="-1" id="EmailSidebaroffcanvas" aria-labelledby="EmailSidebaroffcanvasLabel">
            <EmailSidebar :filterMails="filterMails" :showTab="showTab"/>
          </div>

          <div class="d-block d-xl-none">
            <b-offcanvas v-model="showEmailSidebar" class="offcanvas-xxl" placement="start" no-header body-class="p-0 m-0">
              <EmailSidebar :filterMails="filterMails" :showTab="showTab"/>
            </b-offcanvas>
          </div>
        </b-col>

        <b-col xxl="10">
          <b-card no-body class="position-relative overflow-hidden h-100">
            <div class="p-3">
              <div class="d-flex flex-wrap gap-1">
                <b-button variant="light" class="d-xxl-none d-flex align-items-center px-2 me-2" type="button"
                          @click="showEmailSidebar = !showEmailSidebar">
                  <i class="bx bx-menu fs-18"/>
                </b-button>

                <!-- archive, spam & delete -->
                <b-button-group class="me-1">
                  <b-button type="button" variant="light" v-b-tooltip.hover.top="'Archive'">
                    <i class="bx bx-archive fs-18"></i>
                  </b-button>
                  <b-button type="button" variant="light" v-b-tooltip.hover.top="'Mark as spam'">
                    <i class="bx bx-info-square fs-18"></i>
                  </b-button>
                  <b-button type="button" variant="light" v-b-tooltip.hover.top="'Delete'">
                    <i class="bx bx-trash fs-18"></i>
                  </b-button>
                </b-button-group>

                <!-- move to -->
                <b-dropdown toggle-class="btn-light" class="me-1">
                  <template #button-content>
                    <i class="bx bx-folder fs-18 me-1"/>
                  </template>
                  <span class="dropdown-header">Move to</span>
                  <b-dropdown-item>Social</b-dropdown-item>
                  <b-dropdown-item>Promotions</b-dropdown-item>
                  <b-dropdown-item>Updates</b-dropdown-item>
                  <b-dropdown-item>Forums</b-dropdown-item>
                </b-dropdown>

                <!-- labels -->
                <b-dropdown toggle-class="btn-light" class="me-1">
                  <template #button-content>
                    <i class="bx bx-bookmarks fs-18 me-1"/>
                  </template>
                  <span class="dropdown-header">Label as :</span>
                  <b-dropdown-item>Updates</b-dropdown-item>
                  <b-dropdown-item>Social</b-dropdown-item>
                  <b-dropdown-item>Promotions</b-dropdown-item>
                  <b-dropdown-item>Forums</b-dropdown-item>
                </b-dropdown>

                <!-- more option -->
                <b-dropdown toggle-class="btn-light" text="More">
                  <span class="dropdown-header">More Option :</span>
                  <b-dropdown-item>Mark as Unread</b-dropdown-item>
                  <b-dropdown-item>Add to Tasks</b-dropdown-item>
                  <b-dropdown-item>Add Star</b-dropdown-item>
                  <b-dropdown-item>Mute</b-dropdown-item>
                </b-dropdown>
              </div>
            </div>

            <div class="tab-content pt-0" id="email-tabContent">
              <div class="tab-pane fade" id="email-inbox"
                   :class="['primaryMail', 'socialMail', 'PromotionsMail', 'updatesMail', 'forumsMail', 'email-inbox'].includes(showTab) && 'show active'">
                <div>
                  <ul class="nav nav-tabs nav-justified">
                    <li class="nav-item">
                      <a href="#" class="nav-link d-flex align-items-center"
                         :class="['primaryMail', 'email-inbox'].includes(showTab) && 'active'"
                         @click="filterMails('', 'primaryMail')">
                        <span class="me-2"><i class="bx bxs-inbox fs-18"></i></span>
                        <span class="d-none d-md-block">Primary</span>
                      </a>
                    </li>
                    <li class="nav-item">
                      <a href="#" class="nav-link d-flex align-items-center"
                         :class="showTab === 'socialMail' && 'active'"
                         @click="filterMails('social', 'socialMail')">
                        <span class="me-2"><i class="bx bxs-group fs-18"></i></span>
                        <span class="d-none d-md-block">Social</span>
                      </a>
                    </li>
                    <li class="nav-item">
                      <a href="#" class="nav-link d-flex align-items-center"
                         :class="showTab === 'PromotionsMail' && 'active'"
                         @click="filterMails('promotions', 'PromotionsMail')">
                        <span class="me-2"><i class="bx bxs-purchase-tag fs-18"></i></span>
                        <span class="d-none d-md-block">Promotions</span>
                      </a>
                    </li>
                    <li class="nav-item">
                      <a href="#" class="nav-link d-flex align-items-center"
                         :class="showTab === 'updatesMail' && 'active'" @click="filterMails('updates', 'updatesMail')">
                        <span class="me-2"><i class="bx bxs-info-circle fs-18"></i></span>
                        <span class="d-none d-md-block">Updates</span>
                      </a>
                    </li>
                    <li class="nav-item">
                      <a href="#" class="nav-link d-flex align-items-center"
                         :class="showTab === 'forumsMail' && 'active'"
                         @click="filterMails('forums', 'forumsMail')">
                        <span class="me-2"><i class="bx bxs-chat fs-18"></i></span>
                        <span class="d-none d-md-block">Forums</span>
                      </a>
                    </li>
                  </ul>

                  <div class="tab-content text-muted pt-0">
                    <div class="tab-pane" id="primaryMail"
                         :class="['primaryMail', 'email-inbox'].includes(showTab) && 'show active'">
                      <ul class="message-list mb-0">
                        <template v-for="(mail, idx) in filteredMails" :key="idx">
                          <MailCard :mail="mail" :toggleReadOffcanvas="toggleReadOffcanvas"/>
                        </template>
                      </ul>
                    </div>
                    <div class="tab-pane" id="socialMail" :class="showTab === 'socialMail' && 'show active'">
                      <ul class="message-list mb-0">
                        <template v-for="(mail, idx) in filteredMails" :key="idx">
                          <MailCard :mail="mail" :toggleReadOffcanvas="toggleReadOffcanvas"/>
                        </template>
                      </ul>
                    </div>
                    <div class="tab-pane" id="PromotionsMail" :class="showTab === 'PromotionsMail' && 'show active'">
                      <ul class="message-list mb-0">
                        <template v-for="(mail, idx) in filteredMails" :key="idx">
                          <MailCard :mail="mail" :toggleReadOffcanvas="toggleReadOffcanvas"/>
                        </template>
                      </ul>
                    </div>
                    <div class="tab-pane" id="updatesMail" :class="showTab === 'updatesMail' && 'show active'">
                      <ul class="message-list mb-0">
                        <template v-for="(mail, idx) in filteredMails" :key="idx">
                          <MailCard :mail="mail" :toggleReadOffcanvas="toggleReadOffcanvas"/>
                        </template>
                      </ul>
                    </div>
                    <div class="tab-pane" id="forumsMail" :class="showTab === 'forumsMail' && 'show active'">
                      <ul class="message-list mb-0">
                        <template v-for="(mail, idx) in filteredMails" :key="idx">
                          <MailCard :mail="mail" :toggleReadOffcanvas="toggleReadOffcanvas"/>
                        </template>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>

              <template v-for="(tab, idx) in emailTabs" :key="idx">
                <TabPane :tab="tab" :filteredMails="filteredMails" :showTab="showTab"
                         :toggleReadOffcanvas="toggleReadOffcanvas"/>
              </template>
            </div>

            <div class="px-3 py-2 mt-auto">
              <div class="d-flex align-items-center justify-content-between">
                <div class="">Showing 1 - 20 of 289</div>
                <b-button-group>
                  <b-button type="button" variant="light" size="sm">
                    <i class="bx bx-chevron-left"></i>
                  </b-button>
                  <b-button type="button" variant="primary" size="sm">
                    <i class="bx bx-chevron-right"></i>
                  </b-button>
                </b-button-group>
              </div>
            </div>

            <b-offcanvas v-model="showEmail" class="email-offcanvas position-absolute shadow" placement="end" body-class="p-0 h-100" :body-scrolling="true" id="email-read">
              <template #header>
                <div class="d-flex gap-2 align-items-center w-50">
                  <a href="#" role="button" @click="toggleReadOffcanvas">
                    <i class="bx bx-arrow-back fs-18 align-middle"></i>
                  </a>
                  <h5 class="offcanvas-title text-truncate w-50" id="email-readLabel">Medium</h5>
                </div>

                <div class="ms-auto">
                  <!-- archive, spam & delete -->
                  <b-button-group>
                    <b-button type="button" variant="light">
                      <i class="bx bx-archive fs-18"></i>
                    </b-button>
                    <b-button type="button" variant="light">
                      <i class="bx bx-info-square fs-18"></i>
                    </b-button>
                    <b-button type="button" variant="light">
                      <i class="bx bx-trash fs-18"></i>
                    </b-button>
                  </b-button-group>
                </div>
              </template>
              <EmailRead/>
            </b-offcanvas>
          </b-card>
        </b-col>
      </b-row>
  </VerticalLayout>
</template>

<script setup lang="ts">
import {ref, computed} from 'vue'
import VerticalLayout from "@/layouts/VerticalLayout.vue";
import MailCard from '@/views/apps/email/components/MailCard.vue'
import TabPane from '@/views/apps/email/components/TabPane.vue'
import EmailSidebar from '@/views/apps/email/components/EmailSidebar.vue'
import EmailRead from '@/views/apps/email/components/EmailRead.vue'
import {emailData, emailTabs} from '@/views/apps/email/components/data'

const showEmailSidebar = ref(false)

const showTab = ref('primaryMail')
const category = ref<any>('')
const categoryType = ref('')

const showEmail = ref(false)
const toggleReadOffcanvas = () => {
  showEmail.value = !showEmail.value
}

const filterMails = (ele: any, tab: string) => {
  let keyCheck = ''
  keyCheck = isKeyInArray(emailData, ele)

  if (keyCheck) {
    categoryType.value = 'key'
  } else {
    categoryType.value = 'type'
  }

  category.value = ele
  showTab.value = tab
}

const isKeyInArray = (array: any, key: any) => {
  return array.some((obj: any) => obj.hasOwnProperty(key))
}

const filteredMails = computed(() => {
  return filterEmails(categoryType.value, category.value)
})

const filterEmails = (categoryType: string, category: any) => {
  if (category) {
    if (categoryType === 'type') {
      return emailData.filter((item) => item.type === category)
    } else {
      // @ts-ignore
      return emailData.filter((item) => item[category] === true)
    }
  } else {
    return emailData
  }
}
</script>
