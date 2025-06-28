<template>
  <VerticalLayout>
    <b-row>
      <b-col cols="12">
        <UIComponentCard id="basic-wizard" title="Simple">
          <form-wizard color="#1e84c4" back-button-text="Back To Previous" next-button-text="Next Step"
            finish-button-text="Finish">
            <tab-content title="Account">
              <h4 class="fs-16 fw-semibold mb-1">Account Information</h4>
              <p class="text-muted">Setup your account information</p>

              <b-row>
                <b-col lg="6">
                  <b-form-group class="mb-3" label="User Name" label-for="basicUser">
                    <b-form-input id="basicUser" type="text" placeholder="Enter your name" />
                  </b-form-group>
                </b-col>

                <b-col lg="6">
                  <b-form-group class="mb-3" label="Email" label-for="basicEmail">
                    <b-form-input id="basicEmail" type="email" placeholder="Enter your email" />
                  </b-form-group>
                </b-col>

                <b-col lg="6">
                  <b-form-group class="mb-3" label="Password" label-for="basicPassworda">
                    <b-form-input id="basicPassworda" type="password" placeholder="Enter Password" />
                  </b-form-group>
                </b-col>

                <b-col lg="6">
                  <b-form-group class="mb-3" label="Confirm Password" label-for="basicConfirmPassword">
                    <b-form-input id="basicConfirmPassword" type="password" placeholder="Confirm a Password" />
                  </b-form-group>
                </b-col>
              </b-row>
            </tab-content>

            <tab-content title="Profile">
              <h4 class="fs-16 fw-semibold mb-1">Profile Information</h4>
              <p class="text-muted">Setup your profile information</p>

              <b-row>
                <b-col cols="12">
                  <div class="avatar-lg mb-3">
                    <div
                      class="avatar-title bg-body rounded-circle border border-3 border-dashed-light position-relative">
                      <label for="imageInput" class="position-absolute end-0 bottom-0">
                        <div class="avatar-xs cursor-pointer">
                          <span class="avatar-title bg-light text-dark rounded-circle"><i
                              class="bx bx-camera"></i></span>
                        </div>
                      </label>
                      <input class="hidden" type="file" id="imageInput" accept="image/*" />

                      <img id="preview" :src="dummyAvatar" alt="Preview Img" class="rounded-circle img-fluid" />
                    </div>
                  </div>

                  <b-row>
                    <b-col md="6">
                      <b-form-group class="mb-3" label-for="basicFname" label="First Name">
                        <b-form-input type="text" id="basicFname" placeholder="Chris" />
                      </b-form-group>
                    </b-col>

                    <b-col md="6">
                      <b-form-group class="mb-3" label-for="basicLname" label="Last Name">
                        <b-form-input type="text" id="basicLname" placeholder="Keller" />
                      </b-form-group>
                    </b-col>

                    <b-col md="6">
                      <b-form-group class="mb-3" label-for="basicMnumber" label="Number">
                        <b-form-input type="tel" id="basicMnumber" placeholder="Mobile Number" />
                      </b-form-group>
                    </b-col>

                    <b-col md="6">
                      <b-form-group class="mb-3" label-for="basicCountry" label="Country">
                        <b-form-select id="basicCountry" v-model="selectedCountry" :options="countryOptions" />
                      </b-form-group>
                    </b-col>
                  </b-row>
                </b-col>
              </b-row>
            </tab-content>

            <tab-content title="Social Link">
              <h4 class="fs-16 fw-semibold mb-1">Social Media Links</h4>
              <p class="text-muted">Fill your social media links</p>

              <b-row>
                <b-col lg="6">
                  <b-form-group class="mb-3" label-for="basicGitLink" label="GitHub">
                    <b-form-input id="basicGitLink" type="text" placeholder="GitHub Link" />
                  </b-form-group>
                </b-col>

                <b-col lg="6">
                  <b-form-group class="mb-3" label-for="basicGoogleLink" label="GitHub">
                    <b-form-input id="basicGoogleLink" type="text" placeholder="Google Link" />
                  </b-form-group>
                </b-col>

                <b-col lg="6">
                  <b-form-group class="mb-3" label-for="basicInstagramLink" label="GitHub">
                    <b-form-input id="basicInstagramLink" type="text" placeholder="Instagram Link" />
                  </b-form-group>
                </b-col>

                <b-col lg="6">
                  <b-form-group class="mb-3" label-for="basicSkypeLink" label="GitHub">
                    <b-form-input id="basicSkypeLink" type="text" placeholder="Skype Link" />
                  </b-form-group>
                </b-col>
              </b-row>
            </tab-content>

            <tab-content title="Finish">
              <b-row>
                <b-col cols="12">
                  <div class="text-center">
                    <div class="avatar-md mx-auto mb-3">
                      <div class="avatar-title bg-primary bg-opacity-10 text-primary rounded-circle">
                        <Icon icon="iconamoon:like-duotone" class="fs-36"></Icon>
                      </div>
                    </div>
                    <h3 class="mt-0">Finished !</h3>

                    <p class="w-75 mb-2 mx-auto">Filled Data Successfully.</p>

                    <div class="mb-3">
                      <div class="form-check d-inline-block">
                        <b-form-checkbox>I agree with the Terms and Conditions</b-form-checkbox>
                      </div>
                    </div>
                  </div>
                </b-col>
              </b-row>
            </tab-content>
          </form-wizard>
        </UIComponentCard>

        <UIComponentCard id="custom-wizard" title="Custom Title">
          <form-wizard shape="tab" color="#1e84c4" back-button-text="Back To Previous" next-button-text="Next Step"
            finish-button-text="Finish">
            <tab-content custom-icon='<a class="nav-link fs-5"> Account </a>'>
              <h4 class="fs-16 fw-semibold mb-1">Account Information</h4>
              <p class="text-muted">Setup your account information</p>

              <b-row>
                <b-col lg="6">
                  <b-form-group class="mb-3" label="User Name" label-for="basicUser">
                    <b-form-input id="basicUser" type="text" placeholder="Enter your name" />
                  </b-form-group>
                </b-col>

                <b-col lg="6">
                  <b-form-group class="mb-3" label="Email" label-for="basicEmail">
                    <b-form-input id="basicEmail" type="email" placeholder="Enter your email" />
                  </b-form-group>
                </b-col>

                <b-col lg="6">
                  <b-form-group class="mb-3" label="Password" label-for="basicPassworda">
                    <b-form-input id="basicPassworda" type="password" placeholder="Enter Password" />
                  </b-form-group>
                </b-col>

                <b-col lg="6">
                  <b-form-group class="mb-3" label="Confirm Password" label-for="basicConfirmPassword">
                    <b-form-input id="basicConfirmPassword" type="password" placeholder="Confirm a Password" />
                  </b-form-group>
                </b-col>
              </b-row>
            </tab-content>

            <tab-content custom-icon='<a class="nav-link fs-5"> Profile </a>'>
              <h4 class="fs-16 fw-semibold mb-1">Profile Information</h4>
              <p class="text-muted">Setup your profile information</p>

              <b-row>
                <b-col cols="12">
                  <div class="avatar-lg mb-3">
                    <div
                      class="avatar-title bg-body rounded-circle border border-3 border-dashed-light position-relative">
                      <label for="imageInput" class="position-absolute end-0 bottom-0">
                        <div class="avatar-xs cursor-pointer">
                          <span class="avatar-title bg-light text-dark rounded-circle">
                            <i class="bx bx-camera"></i>
                          </span>
                        </div>
                      </label>
                      <input class="hidden" type="file" id="imageInput" accept="image/*" />

                      <img id="preview" :src="dummyAvatar" alt="Preview Img" class="rounded-circle img-fluid" />
                    </div>
                  </div>

                  <b-row>
                    <b-col md="6">
                      <b-form-group class="mb-3" label-for="basicFname" label="First Name">
                        <b-form-input type="text" id="basicFname" placeholder="Chris" />
                      </b-form-group>
                    </b-col>

                    <b-col md="6">
                      <b-form-group class="mb-3" label-for="basicLname" label="Last Name">
                        <b-form-input type="text" id="basicLname" placeholder="Keller" />
                      </b-form-group>
                    </b-col>

                    <b-col md="6">
                      <b-form-group class="mb-3" label-for="basicMnumber" label="Number">
                        <b-form-input type="tel" id="basicMnumber" placeholder="Mobile Number" />
                      </b-form-group>
                    </b-col>

                    <b-col md="6">
                      <b-form-group class="mb-3" label-for="basicCountry" label="Country">
                        <b-form-select id="basicCountry" v-model="selectedCountry" :options="countryOptions" />
                      </b-form-group>
                    </b-col>
                  </b-row>
                </b-col>
              </b-row>
            </tab-content>

            <tab-content custom-icon='<a class="nav-link fs-5"> Social Link </a>'>
              <h4 class="fs-16 fw-semibold mb-1">Social Media Links</h4>
              <p class="text-muted">Fill your social media links</p>

              <b-row>
                <b-col lg="6">
                  <b-form-group class="mb-3" label-for="basicGitLink" label="GitHub">
                    <b-form-input id="basicGitLink" type="text" placeholder="GitHub Link" />
                  </b-form-group>
                </b-col>

                <b-col lg="6">
                  <b-form-group class="mb-3" label-for="basicGoogleLink" label="GitHub">
                    <b-form-input id="basicGoogleLink" type="text" placeholder="Google Link" />
                  </b-form-group>
                </b-col>

                <b-col lg="6">
                  <b-form-group class="mb-3" label-for="basicInstagramLink" label="GitHub">
                    <b-form-input id="basicInstagramLink" type="text" placeholder="Instagram Link" />
                  </b-form-group>
                </b-col>

                <b-col lg="6">
                  <b-form-group class="mb-3" label-for="basicSkypeLink" label="GitHub">
                    <b-form-input id="basicSkypeLink" type="text" placeholder="Skype Link" />
                  </b-form-group>
                </b-col>
              </b-row>
            </tab-content>

            <tab-content custom-icon='<a class="nav-link fs-5"> Finish </a>'>
              <b-row>
                <b-col cols="12">
                  <div class="text-center">
                    <div class="avatar-md mx-auto mb-3">
                      <div class="avatar-title bg-primary bg-opacity-10 text-primary rounded-circle">
                        <Icon icon="iconamoon:like-duotone" class="fs-36"></Icon>
                      </div>
                    </div>
                    <h3 class="mt-0">Finished !</h3>

                    <p class="w-75 mb-2 mx-auto">Filled Data Successfully.</p>

                    <div class="mb-3">
                      <div class="form-check d-inline-block">
                        <b-form-checkbox>I agree with the Terms and Conditions</b-form-checkbox>
                      </div>
                    </div>
                  </div>
                </b-col>
              </b-row>
            </tab-content>
          </form-wizard>
        </UIComponentCard>
      </b-col>
    </b-row>
  </VerticalLayout>
</template>

<script setup lang="ts">
import VerticalLayout from "@/layouts/VerticalLayout.vue";
import UIComponentCard from "@/components/UIComponentCard.vue";

import { ref } from 'vue';

import { FormWizard, TabContent } from 'vue3-form-wizard';
import 'vue3-form-wizard/dist/style.css';

import dummyAvatar from '@/assets/images/users/dummy-avatar.jpg';
import { Icon } from "@iconify/vue";

const selectedCountry = ref('United States');

const countryOptions = [
  { value: 'United States', text: 'United States' },
  { value: 'Canada', text: 'Canada' },
  { value: 'Australia', text: 'Australia' },
  { value: 'Germany', text: 'Germany' },
  { value: 'Bangladesh', text: 'Bangladesh' },
  { value: 'China', text: 'China' },
  { value: 'Argentina', text: 'Argentina' },
  { value: 'Bharat', text: 'Bharat' },
  { value: 'Afghanistan', text: 'Afghanistan' },
  { value: 'France', text: 'France' },
  { value: 'Brazil', text: 'Brazil' },
  { value: 'Belgium', text: 'Belgium' },
  { value: 'Colombia', text: 'Colombia' },
  { value: 'Albania', text: 'Albania' }
];
</script>
