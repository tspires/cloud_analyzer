<template>
  <AuthLayout>
    <b-row class="justify-content-center">
      <b-col xl="5">
        <b-card no-body class="auth-card">
          <b-card-body class="px-3 py-5">
            <LogoBox customClass="mx-auto mb-4 text-center auth-logo" :smLogoHeight="30" :logoHeight="24" smLogoClass="me-1" />
            <h2 class="fw-bold text-center fs-18">Sign In</h2>
            <p class="text-muted text-center mt-1 mb-4">Enter your email address and password to access admin panel.</p>

            <div class="px-4">
              <b-form @submit.prevent="handleSignIn" class="authentication-form">
                <div v-if="error.length > 0" class="mb-2 text-danger">{{ error }}</div>
                <b-form-group label="Email" class="mb-3">
                  <b-form-input type="email" id="example-email" name="example-email" placeholder="Enter your Email"
                    v-model="v.email.$model" />
                  <div v-if="v.email.$error" class="text-danger">
                    <span v-for="(err, idx) in v.email.$errors" :key="idx">
                      {{ err.$message }}
                    </span>
                  </div>
                </b-form-group>
                <div class="mb-3">
                  <router-link :to="{ name: 'auth.reset-password' }"
                    class="float-end text-muted text-unline-dashed ms-1">Reset password</router-link>
                  <label class="form-label" for="example-password">Password</label>
                  <input type="password" id="example-password" class="form-control" placeholder="Enter your password"
                    v-model="v.password.$model">
                  <div v-if="v.password.$errors" class="text-danger">
                    <span v-for="(err, idx) in v.password.$errors" :key="idx">
                      {{ err.$message }}
                    </span>
                  </div>
                </div>
                <div class="mb-3">
                  <b-form-checkbox id="checkbox-signin">
                    Remember me
                  </b-form-checkbox>
                </div>

                <div class="mb-1 text-center d-grid">
                  <b-button variant="primary" type="submit">Sign In</b-button>
                </div>
              </b-form>

              <p class="mt-3 fw-semibold no-span">OR sign with</p>

              <div class="text-center">
                <a href="javascript:void(0);" class="btn btn-light shadow-none"><i
                    class='bx bxl-google fs-20'></i></a>{{ ' ' }}
                <a href="javascript:void(0);" class="btn btn-light shadow-none"><i
                    class='bx bxl-facebook fs-20'></i></a>{{ ' ' }}
                <a href="javascript:void(0);" class="btn btn-light shadow-none"><i class='bx bxl-github fs-20'></i></a>
              </div>
            </div>
          </b-card-body>
        </b-card>
        <p class="mb-0 text-center">New here? <router-link :to="{ name: 'auth.sign-up' }"
            class="text-reset fw-bold ms-1">Sign Up</router-link></p>
      </b-col>
    </b-row>
  </AuthLayout>
</template>

<script setup lang="ts">
import AuthLayout from '@/layouts/AuthLayout.vue';

import { required, email } from '@vuelidate/validators';
import { useVuelidate } from '@vuelidate/core';

import { ref, reactive, computed } from 'vue';
import { useRoute } from 'vue-router';

import HttpClient from '@/helpers/http-client';
import { useAuthStore } from '@/stores/auth';

import type { AxiosResponse } from 'axios';
import type { User } from '@/types/auth';
import router from '@/router';

const credentials = reactive({
  email: 'user@email.com',
  password: 'password'
});

const vuelidateRules = computed(() => ({
  email: { required, email },
  password: { required }
}));

const v = useVuelidate(vuelidateRules, credentials);

const useAuth = useAuthStore();
const route = useRoute();
const query = route.query;

const error = ref('');
const checked = ref(false);

const handleSignIn = async () => {
  const result = await v.value.$validate();

  if (result) {
    try {
      const res: AxiosResponse<User> = await HttpClient.post('/sign-in', credentials);
      console.log("res", res);

      if (res.data.token) {
        useAuth.saveSession({
          ...res.data,
          token: res.data.token
        });
        redirectUser();
      }
    } catch (e: any) {
      if (e.response?.data?.error) {
        if (error.value.length == 0) error.value = e.response?.data?.error;
      }
    }
  }
};

const redirectUser = () => {
  if (query.redirectedFrom) {
    return router.push(`${query.redirectedFrom}`);
  }
  return router.push('/');
};
</script>
