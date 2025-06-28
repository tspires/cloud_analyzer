<template>
  <AuthLayout>
    <b-row class="justify-content-center">
      <b-col xl="5">
        <b-card no-body class="auth-card">
          <b-card-body class="px-3 py-5">
            <LogoBox customClass="mx-auto mb-4 text-center auth-logo" :smLogoHeight="30" :logoHeight="24" smLogoClass="me-1" />
            <h2 class="fw-bold text-center fs-18">Sign Up</h2>
            <p class="text-muted text-center mt-1 mb-4">New to our platform? Sign up now! It only takes a minute.</p>
            <div class="px-4">
              <b-form action="/" class="authentication-form">
                <b-form-group label="Name" class="mb-3">
                  <b-form-input type="text" id="example-name" placeholder="Enter your name" />
                </b-form-group>

                <b-form-group label="Email" class="mb-3">
                  <b-form-input type="email" id="example-email" placeholder="Enter your email" />
                </b-form-group>

                <b-form-group label="Password" class="mb-3">
                  <b-form-input type="password" id="example-password" name="password"
                    placeholder="Enter your password" />
                </b-form-group>
                <div class="mb-3">
                  <b-form-checkbox>I accept Terms and Condition</b-form-checkbox>
                </div>

                <div class="mb-1 text-center d-grid">
                  <b-button variant="primary" type="submit">Sign Up</b-button>
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

        <p class="mb-0 text-center">I already have an account
          <router-link :to="{ name: 'auth.sign-in' }" class="text-reset fw-bold ms-1">Sign In</router-link>
        </p>
      </b-col>
    </b-row>
  </AuthLayout>
</template>

<script setup lang="ts">
import AuthLayout from '@/layouts/AuthLayout.vue';
</script>
