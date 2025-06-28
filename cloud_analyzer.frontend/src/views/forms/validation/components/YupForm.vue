<template>
  <b-form class="row g-3" @submit.prevent="handleYupSubmit">
    <div v-if="error.length > 0" class="text-danger">{{ error }}</div>
    <b-col md="4">
      <b-form-group label="First name">
        <b-form-input type="text" v-model="yupState.firstName" />
      </b-form-group>
    </b-col>

    <b-col md="4">
      <b-form-group label="Last name">
        <b-form-input type="text" v-model="yupState.lastName" />
      </b-form-group>
    </b-col>

    <b-col md="4">
      <b-form-group label="Username">
        <b-input-group>
          <b-input-group-text>@</b-input-group-text>
          <b-form-input type="text" v-model="yupState.username" />
        </b-input-group>
      </b-form-group>
    </b-col>

    <b-col md="6">
      <b-form-group label="City">
        <b-form-input type="text" v-model="yupState.city" />
      </b-form-group>
    </b-col>

    <b-col md="3">
      <b-form-group label="State">
        <b-form-select v-model="yupState.state">
          <option selected disabled value="">Choose...</option>
          <option>...</option>
        </b-form-select>
      </b-form-group>
    </b-col>

    <b-col md="3">
      <b-form-group label="Zip">
        <b-form-input v-model="yupState.zip" type="text" />
      </b-form-group>
    </b-col>

    <b-col cols="12">
      <b-form-checkbox v-model="yupState.isAgree">Agree to terms and conditions</b-form-checkbox>
    </b-col>

    <b-col cols="12">
      <b-button variant="primary" type="submit"> Submit form </b-button>
    </b-col>
  </b-form>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { boolean, type InferType, object, string } from 'yup'

const error = ref('')
const yupSchema = object({
  isAgree: boolean().required('Please agree with our terms'),
  zip: string().min(6, 'Must be at least 6 characters').required('Zip code is Required'),
  state: string().required('State is Required'),
  city: string().required('City is Required'),
  username: string().required('Username is Required'),
  lastName: string().required('Last name is Required'),
  firstName: string().required('First name is Required')
})
type Schema = InferType<typeof yupSchema>
const yupState = reactive({
  firstName: undefined,
  lastName: undefined,
  username: undefined,
  city: undefined,
  state: undefined,
  zip: undefined,
  isAgree: undefined
})
const handleYupSubmit = async (event: Event) => {
  await yupSchema
    .validate(yupState)
    .then((res) =>
      // validated data
      console.log(res)
    )
    .catch((e) => {
      return (error.value = e.message)
    })
}
</script>
