<template>
  <VerticalLayout>
    <b-row>
      <b-col xl="9">
        <UIComponentCard id="basic" title="Basic">
          <div>
            <b-button variant="primary" id="sweetalert-basic">Click me</b-button>
          </div>
        </UIComponentCard>

        <UIComponentCard id="title" title="A Title with a Text Under">
          <div>
            <b-button class="btn btn-primary" id="sweetalert-title">Click me</b-button>
          </div>
        </UIComponentCard>

        <UIComponentCard id="message" title="Message">
          <div class="hstack gap-2">
            <b-button variant="success" id="sweetalert-success">Success</b-button>
            <b-button variant="warning" id="sweetalert-warning">Warning</b-button>
            <b-button variant="info" id="sweetalert-info">Info</b-button>
            <b-button variant="danger" id="sweetalert-error">Error</b-button>
          </div>
        </UIComponentCard>

        <UIComponentCard id="longcontent" title="Long content Images Message">
          <div>
            <b-button variant="primary" id="sweetalert-longcontent">Click me</b-button>
          </div>
        </UIComponentCard>

        <UIComponentCard id="parameter" title="Parameter">
          <div>
            <b-button variant="primary" id="sweetalert-params">Click me</b-button>
          </div>
        </UIComponentCard>

      </b-col>

      <b-col xl="3">
        <AnchorNavigation :elements="anchorNavigation" />
      </b-col>
    </b-row>
  </VerticalLayout>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import VerticalLayout from "@/layouts/VerticalLayout.vue";
import AnchorNavigation from '@/components/AnchorNavigation.vue';

import Swal from 'sweetalert2/dist/sweetalert2.js';
import 'sweetalert2/dist/sweetalert2.css';
import UIComponentCard from "@/components/UIComponentCard.vue";

type TVueSwalInstance = typeof Swal & typeof Swal.fire;

const anchorNavigation = [
  {
    id: 'basic',
    title: 'Basic Example'
  },
  {
    id: 'title',
    title: 'A Title with a Text Under'
  },
  {
    id: 'message',
    title: 'Message'
  },
  {
    id: 'longcontent',
    title: 'Long content Images Message'
  },
  {
    id: 'parameter',
    title: 'Parameter'
  }
];

onMounted(() => {
  //Basic
  const basic = document.getElementById('sweetalert-basic');
  if (basic) {
    basic.addEventListener('click', function () {
      ; (Swal as TVueSwalInstance).fire({
        title: 'Any fool can use a computer',
        confirmButtonClass: 'btn btn-primary w-xs mt-2',
        // buttonsStyling: false,
        confirmButtonColor: '#ff6c2f',
        showCloseButton: false
      });
    });
  }

  //A title with a text under
  const sweetalertTitle = document.getElementById('sweetalert-title');
  if (sweetalertTitle) {
    sweetalertTitle.addEventListener('click', function () {
      ; (Swal as TVueSwalInstance).fire({
        title: 'The Internet?',
        text: 'That thing is still around?',
        icon: 'question',
        confirmButtonClass: 'btn btn-primary w-xs mt-2',
        confirmButtonColor: '#ff6c2f',
        // buttonsStyling: false,
        showCloseButton: false
      });
    });
  }

  //Success Message
  const success = document.getElementById('sweetalert-success');
  if (success) {
    success.addEventListener('click', function () {
      ; (Swal as TVueSwalInstance).fire({
        title: 'Good job!',
        text: 'You clicked the button!',
        icon: 'success',
        showCancelButton: true,
        confirmButtonClass: 'btn btn-primary w-xs me-2 mt-2',
        cancelButtonClass: 'btn btn-danger w-xs mt-2',
        confirmButtonColor: '#ff6c2f',
        cancelButtonColor: '#ef5f5f',
        // buttonsStyling: false,
        showCloseButton: false
      });
    });
  }

  //error Message
  const error = document.getElementById('sweetalert-error');
  if (error) {
    error.addEventListener('click', function () {
      ; (Swal as TVueSwalInstance).fire({
        title: 'Oops...',
        text: 'Something went wrong!',
        icon: 'error',
        confirmButtonClass: 'btn btn-primary w-xs mt-2',
        confirmButtonColor: '#ff6c2f',
        // buttonsStyling: false,
        footer: '<a href="">Why do I have this issue?</a>',
        showCloseButton: false
      });
    });
  }

  //info Message
  const info = document.getElementById('sweetalert-info');
  if (info) {
    info.addEventListener('click', function () {
      ; (Swal as TVueSwalInstance).fire({
        title: 'Oops...',
        text: 'Something went wrong!',
        icon: 'info',
        confirmButtonClass: 'btn btn-primary w-xs mt-2',
        confirmButtonColor: '#ff6c2f',
        // buttonsStyling: false,
        footer: '<a href="">Why do I have this issue?</a>',
        showCloseButton: false
      });
    });
  }

  //Warning Message
  const warning = document.getElementById('sweetalert-warning');
  if (warning) {
    warning.addEventListener('click', function () {
      ; (Swal as TVueSwalInstance).fire({
        title: 'Oops...',
        text: 'Something went wrong!',
        icon: 'warning',
        confirmButtonClass: 'btn btn-primary w-xs mt-2',
        confirmButtonColor: '#ff6c2f',
        // buttonsStyling: false,
        footer: '<a href="">Why do I have this issue?</a>',
        showCloseButton: false
      });
    });
  }

  // long content
  const longContent = document.getElementById('sweetalert-longcontent');
  if (longContent) {
    longContent.addEventListener('click', function () {
      ; (Swal as TVueSwalInstance).fire({
        imageUrl: 'https://placeholder.pics/svg/300x1500',
        imageHeight: 1500,
        imageAlt: 'A tall image',
        confirmButtonClass: 'btn btn-primary w-xs mt-2',
        confirmButtonColor: '#ff6c2f',
        // buttonsStyling: false,
        showCloseButton: false
      });
    });
  }

  //Parameter
  const params = document.getElementById('sweetalert-params');
  if (params) {
    params.addEventListener('click', function () {
      ; (Swal as TVueSwalInstance)
        .fire({
          title: 'Are you sure?',
          text: "You won't be able to revert this!",
          icon: 'warning',
          showCancelButton: true,
          confirmButtonText: 'Yes, delete it!',
          cancelButtonText: 'No, cancel!',
          confirmButtonClass: 'btn btn-primary w-xs me-2 mt-2',
          cancelButtonClass: 'btn btn-danger w-xs mt-2',
          confirmButtonColor: '#ff6c2f',
          cancelButtonColor: '#ef5f5f',
          // buttonsStyling: false,
          showCloseButton: false
        })
        .then(function (result: any) {
          if (result.value) {
            ; (Swal as TVueSwalInstance).fire({
              title: 'Deleted!',
              text: 'Your file has been deleted.',
              icon: 'success',
              confirmButtonClass: 'btn btn-primary w-xs mt-2',
              confirmButtonColor: '#ff6c2f'
              // buttonsStyling: false
            });
          } else if (
            // Read more about handling dismissals
            result.dismiss === (Swal as TVueSwalInstance).DismissReason.cancel
          ) {
            ; (Swal as TVueSwalInstance).fire({
              title: 'Cancelled',
              text: 'Your imaginary file is safe :)',
              icon: 'error',
              confirmButtonClass: 'btn btn-primary mt-2',
              confirmButtonColor: '#ff6c2f'
              // buttonsStyling: false
            });
          }
        });
    });
  }
});
</script>
