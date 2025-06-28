<template>
  <b-form class="row g-3" @submit.prevent="handleVuelidateSubmit">
    <b-col md="4">
      <b-form-group label="First name">
        <b-form-input type="text" v-model="v.firstName.$model" />
        <div v-if="v.firstName.$error" class="text-danger">First name is required.</div>
      </b-form-group>
    </b-col>

    <b-col md="4">
      <b-form-group label="Last name">
        <b-form-input type="text" v-model="v.lastName.$model" />
        <div v-if="v.lastName.$error" class="text-danger">Last name is required.</div>
      </b-form-group>
    </b-col>

    <b-col md="4">
      <b-form-group label="Username">
        <b-input-group>
          <b-input-group-text>@</b-input-group-text>
          <b-form-input type="text" v-model="v.username.$model" />
        </b-input-group>
        <div v-if="v.username.$error" class="text-danger">Username is required.</div>
      </b-form-group>
    </b-col>

    <b-col md="6">
      <b-form-group label="City">
        <b-form-input type="text" v-model="v.city.$model" />
        <div v-if="v.city.$error" class="text-danger">City is required.</div>
      </b-form-group>
    </b-col>

    <b-col md="3">
      <b-form-group label="State">
        <b-form-select v-model="v.state.$model">
          <option selected disabled value="">Choose...</option>
          <option>...</option>
        </b-form-select>
        <div v-if="v.state.$error" class="text-danger">State is required.</div>
      </b-form-group>
    </b-col>

    <b-col md="3">
      <b-form-group label="Zip">
        <b-form-input v-model="v.zip.$model" type="text" />
        <div v-if="v.zip.$error" class="text-danger">Zip code is required.</div>
      </b-form-group>
    </b-col>

    <b-col cols="12">
      <b-form-checkbox v-model="v.isAgree.$model">Agree to terms and conditions</b-form-checkbox>
      <div v-if="v.isAgree.$error" class="text-danger">Please agree with our terms.</div>
    </b-col>

    <b-col cols="12">
      <b-button variant="primary" type="submit"> Submit form </b-button>
    </b-col>
  </b-form>
</template>

<script setup lang="ts">
import { reactive, computed } from 'vue'
import { required } from '@vuelidate/validators'
import { useVuelidate } from '@vuelidate/core'

const vuelidateState = reactive({
  firstName: undefined,
  lastName: undefined,
  username: undefined,
  city: undefined,
  state: undefined,
  zip: undefined,
  isAgree: undefined
})

const vuelidateRules = computed(() => ({
  firstName: { required },
  lastName: { required },
  username: { required },
  city: { required },
  state: { required },
  zip: { required },
  isAgree: { required }
}))

const v = useVuelidate(vuelidateRules, vuelidateState)

const handleVuelidateSubmit = async () => {
  const result = await v.value.$validate()
}
</script>
