<template>
  <VerticalLayout>
    <b-row>
      <b-col lg="12">
        <div class="timeline">
          <template v-for="(item, idx) in timelineData" :key="idx">
            <article class="timeline-time" v-if="item.date">
              <div class="time-show d-flex align-items-center justify-content-center mt-0">
                <h5 class="mb-0 text-uppercase fs-14 fw-semibold">
                  {{ item.date }}
                </h5>
              </div>
            </article>

            <article class="timeline-item" v-for="(event, idx) in item.events" :key="idx"
              :class="event.side === 'left' && 'timeline-item-left'">
              <div class="timeline-desk">
                <div class="timeline-box clearfix">
                  <span class="timeline-icon"></span>
                  <div class="overflow-hidden">
                    <b-card no-body class="d-inline-block">
                      <b-card-body>
                        <h5 class="mt-0 fs-16">
                          {{ event.title }}
                          <b-badge variant="secondary" class="ms-1 align-items-center" v-if="event.badge">{{ event.badge
                            }}</b-badge>
                        </h5>
                        <p class="text-muted mb-0">
                          {{ event.description }}
                        </p>
                      </b-card-body>
                    </b-card>
                  </div>
                </div>
              </div>
            </article>
          </template>
        </div>
      </b-col>
    </b-row>
  </VerticalLayout>
</template>
<script setup lang="ts">
import VerticalLayout from '@/layouts/VerticalLayout.vue';
import { timelineData } from '@/views/pages/components/data';
</script>