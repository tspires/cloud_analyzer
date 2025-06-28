<template>
  <VerticalLayout>
      <b-row>
        <b-col>
          <b-card no-body>
            <b-card-body>
              <div class="d-flex flex-wrap justify-content-between gap-3">
                <div class="search-bar">
                  <span><i class="bx bx-search-alt"></i></span>
                  <b-form-input type="search" id="search" placeholder="Search task..." />
                </div>
                <div>
                  <a href="#!" class="btn btn-primary d-inline-flex align-items-center">
                    <i class="bx bx-plus me-1"></i>Create Task
                  </a>
                </div>
              </div>
            </b-card-body>
            <div>
              <b-table-simple responsive class="text-nowrap table-centered mb-0">
                <b-thead class="bg-light bg-opacity-50">
                  <b-tr>
                    <b-th class="border-0 py-2">Task Name</b-th>
                    <b-th class="border-0 py-2">Created Date</b-th>
                    <b-th class="border-0 py-2">Due Date</b-th>
                    <b-th class="border-0 py-2">Assigned</b-th>
                    <b-th class="border-0 py-2">Status</b-th>
                    <b-th class="border-0 py-2">Priority</b-th>
                    <b-th class="border-0 py-2">Action</b-th>
                  </b-tr>
                </b-thead>
                <b-tbody>
                  <b-tr v-for="(todo, idx) in todosData" :key="idx">
                    <b-td>
                      <div class="d-flex align-items-center gap-2">
                        <div class="form-check form-todo ps-4">
                          <input type="checkbox" class="form-check-input rounded-circle mt-0 fs-18"
                            :id="`customCheck${todo.id}`" :checked="todo.checked" />
                          <label class="form-check-label" :for="`customCheck${todo.id}`">
                            {{ todo.taskName }}
                          </label>
                        </div>
                      </div>
                    </b-td>
                    <b-td>
                      {{ todo.createDate }}
                      <small>{{ todo.time }}</small>
                    </b-td>
                    <b-td>{{ todo.dueDate }}</b-td>
                    <b-td>
                      <div class="d-flex align-items-center">
                        <img :src="todo.assigned.avatar" alt="" class="avatar-xs rounded-circle me-2" />
                        <div>
                          <h5 class="fs-14 mt-1 fw-normal">
                            {{ todo.assigned.name }}
                          </h5>
                        </div>
                      </div>
                    </b-td>
                    <b-td>
                      <b-badge :variant="null"
                        :class="todo.status === 'completed' ? 'badge-soft-success' : todo.status === 'new' ? 'badge-soft-info' : todo.status === 'pending' ? 'badge-soft-primary' : 'badge-soft-warning'">
                        {{ kebabToTitleCase(todo.status) }}
                      </b-badge>
                    </b-td>
                    <b-td
                      :class="todo.priority === 'high' ? 'text-danger' : todo.priority === 'medium' ? 'text-warning' : 'text-success'">
                      <i class="bx bxs-circle me-1"></i>{{ toSentenceCase(todo.priority) }}
                    </b-td>
                    <b-td>
                      <b-button type="button" size="sm" :variant="null" class="btn-soft-secondary me-2">
                        <i class="bx bx-edit fs-16"></i>
                      </b-button>
                      <b-button type="button" size="sm" :variant="null" class="btn-soft-danger">
                        <i class="bx bx-trash fs-16"></i>
                      </b-button>
                    </b-td>
                  </b-tr>
                </b-tbody>
              </b-table-simple>
              <div class="align-items-center justify-content-between row g-0 text-center text-sm-start p-3 border-top">
                <div class="col-sm">
                  <div class="text-muted">
                    Showing
                    <span class="fw-semibold">10</span>
                    of
                    <span class="fw-semibold">52</span>
                    tasks
                  </div>
                </div>
                <div class="col-sm-auto mt-3 mt-sm-0">
                  <b-pagination class="m-0" pills v-model="currentPage" :per-page="perPageItem"
                    :total-rows="todosData.length" />
                </div>
              </div>
            </div>
          </b-card>
        </b-col>
      </b-row>
  </VerticalLayout>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import VerticalLayout from "@/layouts/VerticalLayout.vue";
import { kebabToTitleCase, toSentenceCase } from '@/helpers/change-casing';
import { todosData } from '@/views/apps/todo/components/data';

const perPageItem = ref(5);
const currentPage = ref(1);
</script>
