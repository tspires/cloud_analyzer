<template>
  <VerticalLayout>
    <b-row>
      <b-col xl="12">
        <UIComponentCard id="quill-snow-editor" title="Snow Editor">
          <div class="mt-3">
            <QuillEditor theme="snow" :toolbar="toolbar1" style="height: 300px" :content="taskDetail" content-type="html" />
          </div>
        </UIComponentCard>
        <UIComponentCard id="quill-bubble-editor" title="Bubble Editor">
          <div class="mt-3">
            <QuillEditor theme="bubble" style="height: 300px" :toolbar="toolbar2" :content="taskDetail" content-type="html" />
          </div>
        </UIComponentCard>
      </b-col>
    </b-row>
  </VerticalLayout>
</template>

<script setup lang="ts">
import VerticalLayout from "@/layouts/VerticalLayout.vue";
import { QuillEditor } from '@vueup/vue-quill';
import { ref } from 'vue';
import UIComponentCard from "@/components/UIComponentCard.vue";

const content = ref('');

const toolbar1 = [[{ font: [] }, { size: [] }], ['bold', 'italic', 'underline', 'strike'], [{ color: [] }, { background: [] }], [{ script: 'super' }, { script: 'sub' }], [{ header: [false, 1, 2, 3, 4, 5, 6] }, 'blockquote', 'code-block'], [{ list: 'ordered' }, { list: 'bullet' }, { indent: '-1' }, { indent: '+1' }], ['direction', { align: [] }], ['link', 'image', 'video'], ['clean']];
const toolbar2 = [
  ['bold', 'italic', 'link'],
  [{ header: '1' }, { header: '2' }, 'blockquote']
];

const taskDetail = `<h3><span class="ql-size-large">Hello World!</span></h3>
      <h3>This is a simple editable area.</h3>
      - Select a text to reveal the toolbar.
      - Edit rich document on-the-fly, so elastic!
      <span ><b>End of simple area</b></span>`;
</script>
