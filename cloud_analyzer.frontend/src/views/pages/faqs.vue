<template>
  <VerticalLayout>
    <b-row>
      <b-col>
        <b-card no-body>
          <b-card-body class="p-4">
            <b-row class="g-xl-4">
              <b-col xl="6">
                <h4 class="mb-3 fw-semibold fs-16">General</h4>
                <b-accordion free>
                  <template v-for="(item, idx) in generalFAQs" :key="idx">
                    <b-accordion-item :title="item.question" button-class="fw-medium" :visible="!idx">
                      {{ item.answer }}
                    </b-accordion-item>
                  </template>
                </b-accordion>
                <h4 class="mb-3 mt-4 fw-semibold fs-16">Refunds</h4>
                <b-accordion free>
                  <template v-for="(item, idx) in refundsFAQs" :key="idx">
                    <b-accordion-item :title="item.question" button-class="fw-medium" :visible="!idx">
                      {{ item.answer }}
                    </b-accordion-item>
                  </template>
                </b-accordion>
              </b-col>
              <b-col xl="6">
                <h4 class="mb-3 fw-semibold fs-16">Payments</h4>
                <b-accordion free>
                  <template v-for="(item, idx) in paymentsFAQs" :key="idx">
                    <b-accordion-item :title="item.question" button-class="fw-medium" :visible="!idx">
                      {{ item.answer }}
                    </b-accordion-item>
                  </template>
                </b-accordion>
                <h4 class="mb-3 mt-4 fw-semibold fs-16">Support</h4>
                <b-accordion free>
                  <template v-for="(item, idx) in supportFAQs" :key="idx">
                    <b-accordion-item :title="item.question" button-class="fw-medium" :visible="!idx">
                      {{ item.answer }}
                    </b-accordion-item>
                  </template>
                </b-accordion>
              </b-col>
            </b-row>
            <b-row class="my-5">
              <b-col cols="12" class="text-center">
                <h4>Can't find a questions?</h4>
                <b-button type="button" variant="success" class="mt-2"><i class="bx bx-envelope me-1"></i> Email us your question</b-button>
                <b-button type="button" variant="info" class="mt-2 ms-1"><i class="bx bxl-twitter me-1"></i> Send us a tweet</b-button>
              </b-col>
            </b-row>
          </b-card-body>
        </b-card>
      </b-col>
    </b-row>
  </VerticalLayout>
</template>
<script setup lang="ts">
import VerticalLayout from '@/layouts/VerticalLayout.vue';
import { generalFAQs, refundsFAQs, paymentsFAQs, supportFAQs } from '@/views/pages/components/data';
</script>