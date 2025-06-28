import {createApp} from 'vue'
import {createPinia} from 'pinia'

import App from './App.vue'
import router from './router'

import {createBootstrap} from 'bootstrap-vue-next'
import VueApexCharts from 'vue3-apexcharts'

import moment from 'moment'

window.moment = moment

import 'simplebar'
import 'swiper/css'
import 'swiper/css/scrollbar'
import 'swiper/css/navigation'
import 'swiper/css/pagination'
import 'swiper/css/effect-fade'
import 'swiper/css/effect-flip'
import 'swiper/css/effect-creative'
import 'dropzone/src/dropzone.scss'
import 'flatpickr/dist/flatpickr.css'
import 'apexcharts/dist/apexcharts.css'
import 'nouislider/dist/nouislider.css'
import 'gridjs/dist/theme/mermaid.min.css'
import 'choices.js/src/styles/choices.scss'
import '@vueup/vue-quill/dist/vue-quill.snow.css'
import '@vueup/vue-quill/dist/vue-quill.bubble.css'

import 'bootstrap-vue-next/dist/bootstrap-vue-next.css'
import '@/assets/scss/app.scss'
import '@/assets/scss/icons.scss'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(createBootstrap())
app.use(VueApexCharts)

app.mount('#app')
