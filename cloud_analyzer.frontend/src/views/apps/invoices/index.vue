<template>
     <VerticalLayout>
          <b-row>
               <b-col>
                    <b-card no-body>
                         <b-card-body>
                              <div class="d-flex flex-wrap justify-content-between gap-3">
                                   <div class="search-bar">
                                        <span><i class="bx bx-search-alt"></i></span>
                                        <input type="search" class="form-control" id="search" placeholder="Search invoice...">
                                   </div>
                                   <div>
                                        <a href="#!" class="btn btn-success"> <i class="bx bx-plus me-1"></i>Create Invoice </a>
                                   </div>
                              </div>
                         </b-card-body>
                         <div>
                              <b-table-simple responsive class="table-centered text-nowrap mb-0">
                                   <b-thead class="bg-light bg-opacity-50">
                                        <b-tr>
                                             <b-th class="border-0 py-2">Invoice ID</b-th>
                                             <b-th class="border-0 py-2">Customer</b-th>
                                             <b-th class="border-0 py-2">Created Date</b-th>
                                             <b-th class="border-0 py-2">Due Date</b-th>
                                             <b-th class="border-0 py-2">Amount</b-th>
                                             <b-th class="border-0 py-2">Payment Status</b-th>
                                             <b-th class="border-0 py-2">Via</b-th>
                                             <b-th class="border-0 py-2">Action</b-th>
                                        </b-tr>
                                   </b-thead>
                                   <b-tbody>
                                        <b-tr v-for="(item, idx) in invoiceList" :key="idx">
                                             <b-td>
                                                  <router-link :to="`/apps/invoice/${item.id}`" class="fw-medium">#{{ item.id }}</router-link>
                                             </b-td>
                                             <b-td>
                                                  <div class="d-flex align-items-center">
                                                       <img :src="item.customer.img" alt=""
                                                            class="avatar-xs rounded-circle me-2">
                                                       <div>
                                                            <h5 class="fs-14 m-0 fw-normal">{{ item.customer.name }}</h5>
                                                       </div>
                                                  </div>
                                             </b-td>
                                             <b-td>{{ item.createdDate }}</b-td>
                                             <b-td>{{ item.dueDate }}</b-td>
                                             <b-td>{{ currency }}{{ item.amount }}</b-td>
                                             <b-td>
                                                  <b-badge :variant="null" :class="item.paymentStatus === 'paid' ? 'badge-soft-success' : item.paymentStatus === 'send' ? 'badge-soft-primary' : 'badge-soft-warning'">
                                                       {{ toSentenceCase(item.paymentStatus) }}
                                                  </b-badge>
                                             </b-td>
                                             <b-td>{{ item.via }}</b-td>
                                             <b-td>
                                                  <button type="button" class="btn btn-sm btn-soft-secondary me-1"><i class="bx bx-edit fs-16"></i></button>
                                                  <button type="button" class="btn btn-sm btn-soft-danger"><i class="bx bx-trash fs-16"></i></button>
                                             </b-td>
                                        </b-tr>
                                   </b-tbody>
                              </b-table-simple>
                              <div class="align-items-center justify-content-between row g-0 text-center text-sm-start p-3 border-top">
                                   <div class="col-sm">
                                        <div class="text-muted">
                                             Showing <span class="fw-semibold">10</span> of <span
                                                  class="fw-semibold">52</span> invoices
                                        </div>
                                   </div>
                                   <div class="col-sm-auto mt-3 mt-sm-0">
                                        <ul class="pagination pagination-rounded m-0">
                                             <li class="page-item">
                                                  <a href="#" class="page-link"><i class='bx bx-left-arrow-alt'></i></a>
                                             </li>
                                             <li class="page-item active">
                                                  <a href="#" class="page-link">1</a>
                                             </li>
                                             <li class="page-item">
                                                  <a href="#" class="page-link">2</a>
                                             </li>
                                             <li class="page-item">
                                                  <a href="#" class="page-link">3</a>
                                             </li>
                                             <li class="page-item">
                                                  <a href="#" class="page-link"><i class='bx bx-right-arrow-alt'></i></a>
                                             </li>
                                        </ul>
                                   </div>
                              </div>
                         </div>
                    </b-card>
               </b-col>
          </b-row>
     </VerticalLayout>
</template>
<script setup lang="ts">
import VerticalLayout from "@/layouts/VerticalLayout.vue";
import { currency } from '@/helpers/constants';
import { toSentenceCase } from '@/helpers/change-casing';
import { invoiceList } from '@/views/apps/invoices/components/data';
</script>