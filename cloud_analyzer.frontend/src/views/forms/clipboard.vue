<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="9">
          <UIComponentCard id="copy-from-element" title="Copy text from another element">
            <b-row>
              <b-col lg="6">
                <div>
                  <div class="input-group">
                    <b-form-input id="clipboard_example" type="text" placeholder="name@example.com"
                                  v-model="inputEle"/>
                    <b-button variant="primary" class="btn-copy-clipboard" @click="(e:any) => doCopy(inputEle, e)"> Copy
                    </b-button>
                  </div>
                </div>
              </b-col>
            </b-row>
          </UIComponentCard>

          <UIComponentCard id="copy-from-textarea" title="Copy text from another element">
            <b-row>
              <b-col lg="6">
                <div class="d-flex gap-2 align-items-start">
                  <b-form-textarea v-model="textareaEle" cols="62" rows="6"/>
                  <b-button variant="primary" @click="(e:any) => doCopy(textareaEle, e)"> Copy</b-button>
                </div>
              </b-col>
            </b-row>
          </UIComponentCard>

          <UIComponentCard id="copy-from-attribute" title="Copy text from attribute">
            <b-row>
              <b-col lg="6">
                <div>
                  <b-button variant="primary"
                            @click="(e:any) => doCopy(`Just because you can doesn't mean you should — clipboard.js`, e)">
                    Copy to clipboard
                  </b-button>
                </div>
              </b-col>
            </b-row>
          </UIComponentCard>
        </b-col>

        <b-col xl="3">
          <AnchorNavigation :elements="anchorNavigation"/>
        </b-col>
      </b-row>
  </VerticalLayout>
</template>

<script setup lang="ts">
import VerticalLayout from "@/layouts/VerticalLayout.vue";
import AnchorNavigation from '@/components/AnchorNavigation.vue'
import {copyText} from 'vue3-clipboard'
import {ref} from 'vue'
import UIComponentCard from "@/components/UIComponentCard.vue";

const inputEle = ref('name@example.com')
const textareaEle = ref('Mussum ipsum cacilds, vidis litro abertis. Consetis adipiscings elitis. Pra lá , depois divoltis porris, paradis. Paisis, filhis, espiritis santis. Mé faiz elementum girarzis, nisi eros vermeio, in elementis mé pra quem é amistosis quis leo. Manduma pindureta quium dia nois paga.')

const doCopy = (text: string, e: any) => {
  copyText(text, undefined, (error: string) => {
    if (error) {
      console.log(error)
      return
    } else {
      const text = e.srcElement.innerText
      e.srcElement.innerText = 'Copied!'
      setTimeout(() => {
        e.srcElement.innerText = text
      }, 3000)
    }
  })
}

const anchorNavigation = [
  {
    id: 'copy-from-element',
    title: 'Copy text from another element'
  },
  {
    id: 'copy-from-textarea',
    title: 'Copy text from textarea'
  },
  {
    id: 'copy-from-attribute',
    title: 'Copy text from attribute'
  }
]
</script>
