<template>
  <VerticalLayout>
    <b-row>
      <b-col cols="12">
        <b-card no-body>
          <b-card-body>
            <b-row>
              <b-col xl="3">
                <div class="d-grid">
                  <b-button type="button" variant="primary" id="btn-new-event" @click="toggleModal">
                    <i class="bx bx-plus fs-18 me-2"></i>
                    Add New Schedule
                  </b-button>
                </div>
                <div id="external-events">
                  <br />
                  <p class="text-muted">Drag and drop your event or click in the calendar</p>
                  <template v-for="(event, idx) in externalEvents" :key="idx">
                    <div :class="`external-event bg-soft-${event.className} text-${event.className}`"
                      :data-class="`bg-${event.className}`">
                      <i class="bx bxs-circle me-2 vertical-middle"></i>
                      {{ event.title }}
                    </div>
                  </template>
                </div>
              </b-col>

              <b-col xl="9">
                <div class="mt-4 mt-lg-0">
                  <div id="calendar">
                    <FullCalendar ref="fullCalendar" :bootstrap-font-awesome="false" :options="calendarOptions" />
                  </div>
                </div>
              </b-col>
            </b-row>
          </b-card-body>
        </b-card>

        <b-modal v-model="modal" :title="isEditEvent ? 'Edit Event' : 'Add Event'" header-class="p-3 border-bottom-0"
          body-class="px-3 pb-3 pt-0" hide-footer>
          <b-form @submit.prevent="handleVuelidateSubmit">
            <b-row>
              <b-col cols="12">
                <div class="mb-3">
                  <b-form-group label="Event Name">
                    <b-form-input type="text" v-model="v.eventName.$model" />
                    <div v-if="v.eventName.$error" class="text-danger">Please provide a valid event name</div>
                  </b-form-group>
                </div>
              </b-col>
              <b-col cols="12">
                <div class="mb-3">
                  <b-form-group label="Category">
                    <b-form-select v-model="v.eventCategory.$model">
                      <option :value="option.value" v-for="(option, idx) in options" :key="idx">
                        {{ option.text }}
                      </option>
                    </b-form-select>
                    <div v-if="v.eventCategory.$error" class="text-danger">Please select a valid event category</div>
                  </b-form-group>
                </div>
              </b-col>
            </b-row>
            <b-row>
              <b-col cols="6">
                <b-button type="button" variant="danger" id="btn-delete-event" @click="deleteEvent" v-if="isEditEvent">
                  Delete
                </b-button>
              </b-col>
              <b-col cols="6" class="text-end">
                <b-button type="button" variant="light" class="me-1" @click="toggleModal"> Close</b-button>
                <b-button type="submit" variant="primary" id="btn-save-event"> Save</b-button>
              </b-col>
            </b-row>
          </b-form>
        </b-modal>
      </b-col>
    </b-row>
  </VerticalLayout>
</template>

<script setup lang="ts">
import VerticalLayout from "@/layouts/VerticalLayout.vue";
import { ref, onMounted, reactive, computed } from 'vue';
import FullCalendar from '@fullcalendar/vue3';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin, { Draggable } from '@fullcalendar/interaction';
import bootstrapPlugin from '@fullcalendar/bootstrap';
import listPlugin from '@fullcalendar/list';
import { type CalendarOptions } from '@fullcalendar/core';
import { useVuelidate } from '@vuelidate/core';
import { required } from '@vuelidate/validators';
import { externalEvents, options, initialEvents } from '@/views/apps/calendar/schedule/components/data';

const modal = ref(false);
const eventData = ref();
const isEditEvent = ref(false);
const isDateClick = ref('');

const dateEvent = (e: any) => {
  isDateClick.value = e.date;
  toggleModal();
};

const toggleModal = () => {
  modal.value = !modal.value;
  v.value.$reset();
  isEditEvent.value = false;
  vuelidateState.eventName = undefined;
  vuelidateState.eventCategory = undefined;
};

const deleteEvent = () => {
  eventData.value.remove();
  toggleModal();
};

const editEvent = (info: any) => {
  toggleModal();
  isEditEvent.value = true;
  eventData.value = info.event;
  vuelidateState.eventName = eventData.value.title;
  vuelidateState.eventCategory = eventData.value.classNames[0];
};

const calendarOptions = ref<CalendarOptions>({
  plugins: [dayGridPlugin, timeGridPlugin, listPlugin, bootstrapPlugin, interactionPlugin],
  initialView: 'dayGridMonth',
  slotDuration: '00:30:00',
  slotMinTime: '07:00:00',
  slotMaxTime: '19:00:00',
  themeSystem: 'bootstrap',
  bootstrapFontAwesome: false,
  buttonText: {
    today: 'Today',
    month: 'Month',
    week: 'Week',
    day: 'Day',
    list: 'List',
    prev: 'Prev',
    next: 'Next'
  },
  handleWindowResize: true,
  // height: window.innerHeight - 200,
  headerToolbar: {
    left: 'prev,next today',
    center: 'title',
    right: 'dayGridMonth,timeGridWeek,timeGridDay,listMonth'
  },
  droppable: true,
  editable: true,
  selectable: true,
  events: initialEvents,
  eventClick: editEvent,
  dateClick: dateEvent
});

onMounted(() => {
  const ele = document.getElementById('external-events');

  if (ele) {
    new Draggable(ele, {
      itemSelector: '.external-event',
      eventData: function (eventEl: any) {
        return {
          title: eventEl.innerText,
          start: new Date(),
          className: eventEl.getAttribute('data-class')
        };
      }
    });
  }
});

const vuelidateState = reactive({
  eventName: undefined,
  eventCategory: undefined
});

const vuelidateRules = computed(() => ({
  eventName: { required },
  eventCategory: { required }
}));

const v = useVuelidate(vuelidateRules, vuelidateState);

const fullCalendar = ref();

const handleVuelidateSubmit = async () => {
  const result = await v.value.$validate();
  if (result) {
    if (!isEditEvent.value) {
      const calendarApi = fullCalendar.value?.getApi();
      calendarApi.addEvent({
        id: (Math.floor(Math.random() * 100 + 20) - 20).toString(),
        title: vuelidateState.eventName,
        className: vuelidateState.eventCategory,
        start: isDateClick.value || new Date()
      });
    } else {
      eventData.value.setProp('title', vuelidateState.eventName);
      eventData.value.setProp('classNames', [vuelidateState.eventCategory]);
      isEditEvent.value = false;
    }
    isDateClick.value = '';
    toggleModal();
  }
};
</script>
