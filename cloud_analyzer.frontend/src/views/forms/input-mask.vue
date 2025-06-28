<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="12">
          <UIComponentCard id="default" title="Input Masks">
            <div>
              <b-row>
                <b-col md="6">
                  <b-form action="#">
                    <div class="mb-3">
                      <label class="form-label">Date</label>
                      <InputMask id="dates" mask="99/99/9999"/>
                      <span class="fs-13 text-muted">e.g "DD/MM/YYYY"</span>
                    </div>
                    <div class="mb-3">
                      <label class="form-label">Hour</label>
                      <InputMask id="time" mask="99:99:99"/>
                      <span class="fs-13 text-muted">e.g "HH:MM:SS"</span>
                    </div>
                    <div class="mb-3">
                      <label class="form-label">Date & Hour</label>
                      <InputMask id="date-and-time" mask="99/99/9999 99:99:99"/>
                      <span class="fs-13 text-muted">e.g "DD/MM/YYYY HH:MM:SS"</span>
                    </div>
                    <div class="mb-3">
                      <label class="form-label">ZIP Code</label>
                      <InputMask id="zip" mask="99999-999"/>
                      <span class="fs-13 text-muted">e.g "xxxxx-xxx"</span>
                    </div>
                    <div class="mb-3">
                      <label class="form-label">Crazy Zip Code</label>
                      <InputMask id="crazy-zip" mask="9-99-99-99"/>
                      <span class="fs-13 text-muted">e.g "x-xx-xx-xx"</span>
                    </div>
                    <div class="mb-3">
                      <label class="form-label">Money</label>
                      <InputMask id="money" mask="999.999.999.999.999,99"/>
                      <span class="fs-13 text-muted">e.g "Your money"</span>
                    </div>
                    <div class="mb-3">
                      <label class="form-label">Money 2</label>
                      <InputMask id="money-2" mask="#.##9,99"/>
                      <span class="fs-13 text-muted">e.g "#.##0,00"</span>
                    </div>
                  </b-form>
                </b-col>

                <b-col md="6">
                  <b-form>
                    <div class="mb-3">
                      <label class="form-label">Telephone</label>
                      <InputMask id="telephone" mask="9999-9999"/>
                      <span class="fs-13 text-muted">e.g "xxxx-xxxx"</span>
                    </div>
                    <div class="mb-3">
                      <label class="form-label">Telephone with Code Area</label>
                      <InputMask id="code-telephone" mask="(99) 9999-9999"/>
                      <span class="fs-13 text-muted">e.g "(xx) xxxx-xxxx"</span>
                    </div>
                    <div class="mb-3">
                      <label class="form-label">US Telephone</label>
                      <InputMask id="us-telephone" mask="(999) 999-9999"/>
                      <span class="fs-13 text-muted">e.g "(xxx) xxx-xxxx"</span>
                    </div>
                    <div class="mb-3">
                      <label class="form-label">São Paulo Cellphones</label>
                      <InputMask id="sao-paulo-telephone" mask="(99) 99999-9999"/>
                      <span class="fs-13 text-muted">e.g "(xx) xxxxx-xxxx"</span>
                    </div>
                    <div class="mb-3">
                      <label class="form-label">CPF</label>
                      <InputMask id="cpf" mask="999.999.999-99"/>
                      <span class="fs-13 text-muted">e.g "xxx.xxx.xxxx-xx"</span>
                    </div>
                    <div class="mb-3">
                      <label class="form-label">CNPJ</label>
                      <InputMask id="cnpj" mask="99.999.999/9999-99"/>
                      <span class="fs-13 text-muted">e.g "xx.xxx.xxx/xxxx-xx"</span>
                    </div>
                    <div class="mb-3">
                      <label class="form-label">IP Address</label>
                      <InputMask id="ip" mask="999.999.999.999"/>
                      <span class="fs-13 text-muted">e.g "xxx.xxx.xxx.xxx"</span>
                    </div>
                  </b-form>
                </b-col>
              </b-row>
            </div>
          </UIComponentCard>
        </b-col>
      </b-row>
  </VerticalLayout>
</template>

<script setup lang="ts">
import VerticalLayout from "@/layouts/VerticalLayout.vue";
import UIComponentCard from "@/components/UIComponentCard.vue";
import InputMask from '@/components/InputMask.vue'
</script>
