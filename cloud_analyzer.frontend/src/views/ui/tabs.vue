<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="9">
          <UIComponentCard title="Nav Tabs" id="default">
            <b-tabs content-class="text-muted" class="mt-3">
              <b-tab id="home">
                <template #title>
                  <span class="d-block d-sm-none"><i class="bx bx-home"></i></span>
                  <span class="d-none d-sm-block">Home</span>
                </template>
                <p class="mb-0">
                  Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium,
                  totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta
                  sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                  consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui
                  dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non
                  numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem?
                </p>
              </b-tab>
              <b-tab id="profile" active>
                <template #title>
                  <span class="d-block d-sm-none"><i class="bx bx-user"></i></span>
                  <span class="d-none d-sm-block">Profile</span>
                </template>
                <p class="mb-0">
                  Li Europan lingues es membres del sam familie. Lor separat existentie es un myth. Por scientie,
                  musica, sport etc, litot Europa usa li sam vocabular. Li lingues differe solmen in li grammatica, li
                  pronunciation e li plu commun vocabules. Omnicos directe al desirabilite de un nov lingua franca: On
                  refusa continuar payar custosi traductores. At solmen va esser necessi far uniform grammatica,
                  pronunciation e plu sommun paroles. Ma quande lingues coalesce, li grammatica del resultant
                  lingue es plu simplic e regulari quam ti del coalescent lingues. Li nov lingua franca va esser plu
                  simplic e regulari quam li existent Europan lingues.
                </p>
              </b-tab>
              <b-tab id="settings">
                <template #title>
                  <span class="d-block d-sm-none"><i class="bx bx-envelope"></i></span>
                  <span class="d-none d-sm-block">Messages</span>
                </template>
                <p class="mb-0">
                  Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium,
                  totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta
                  sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                  consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui
                  dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non
                  numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem?
                </p>
              </b-tab>
            </b-tabs>
          </UIComponentCard>

          <UIComponentCard title="Tabs Justified" id="static-backdrop">
            <b-tabs content-class="pt-2 text-muted" class="mt-3" justified>
              <b-tab id="home" active>
                <template #title>
                  <span class="d-block d-sm-none"><i class="bx bx-home"></i></span>
                  <span class="d-none d-sm-block">Home</span>
                </template>
                <p class="mb-0">
                  Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium,
                  totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta
                  sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                  consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui
                  dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non
                  numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem?
                </p>
              </b-tab>
              <b-tab id="profile">
                <template #title>
                  <span class="d-block d-sm-none"><i class="bx bx-user"></i></span>
                  <span class="d-none d-sm-block">Profile</span>
                </template>
                <p class="mb-0">
                  Li Europan lingues es membres del sam familie. Lor separat existentie es un myth. Por scientie,
                  musica, sport etc, litot Europa usa li sam vocabular. Li lingues differe solmen in li grammatica, li
                  pronunciation e li plu commun vocabules. Omnicos directe al desirabilite de un nov lingua franca: On
                  refusa continuar payar custosi traductores. At solmen va esser necessi far uniform grammatica,
                  pronunciation e plu sommun paroles. Ma quande lingues coalesce, li grammatica del resultant
                  lingue es plu simplic e regulari quam ti del coalescent lingues. Li nov lingua franca va esser plu
                  simplic e regulari quam li existent Europan lingues.
                </p>
              </b-tab>
              <b-tab id="settings">
                <template #title>
                  <span class="d-block d-sm-none"><i class="bx bx-envelope"></i></span>
                  <span class="d-none d-sm-block">Messages</span>
                </template>
                <p class="mb-0">
                  Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium,
                  totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta
                  sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                  consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui
                  dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non
                  numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem?
                </p>
              </b-tab>
            </b-tabs>
          </UIComponentCard>

          <UIComponentCard title="Nav Pills" id="scrolling-long-content">
            <b-tabs content-class="pt-2 text-muted" class="mt-3" pills>
              <b-tab id="home">
                <template #title>
                  <span class="d-block d-sm-none"><i class="bx bx-home"></i></span>
                  <span class="d-none d-sm-block">Home</span>
                </template>
                <p class="mb-0">
                  Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium,
                  totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta
                  sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                  consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui
                  dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non
                  numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem?
                </p>
              </b-tab>
              <b-tab id="profile" active>
                <template #title>
                  <span class="d-block d-sm-none"><i class="bx bx-user"></i></span>
                  <span class="d-none d-sm-block">Profile</span>
                </template>
                <p class="mb-0">
                  Li Europan lingues es membres del sam familie. Lor separat existentie es un myth. Por scientie,
                  musica, sport etc, litot Europa usa li sam vocabular. Li lingues differe solmen in li grammatica, li
                  pronunciation e li plu commun vocabules. Omnicos directe al desirabilite de un nov lingua franca: On
                  refusa continuar payar custosi traductores. At solmen va esser necessi far uniform grammatica,
                  pronunciation e plu sommun paroles. Ma quande lingues coalesce, li grammatica del resultant
                  lingue es plu simplic e regulari quam ti del coalescent lingues. Li nov lingua franca va esser plu
                  simplic e regulari quam li existent Europan lingues.
                </p>
              </b-tab>
              <b-tab id="settings">
                <template #title>
                  <span class="d-block d-sm-none"><i class="bx bx-envelope"></i></span>
                  <span class="d-none d-sm-block">Messages</span>
                </template>
                <p class="mb-0">
                  Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium,
                  totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta
                  sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                  consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui
                  dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non
                  numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem?
                </p>
              </b-tab>
            </b-tabs>
          </UIComponentCard>

          <UIComponentCard title="Pills Justified" id="modal-position">
            <b-tabs class="mt-3" content-class="pt-2 text-muted" nav-class="p-1"
                    nav-wrapper-class="d-flex flex-wrap gap-2" justified pills>
              <b-tab id="home">
                <template #title>
                  <span class="d-block d-sm-none"><i class="bx bx-home"></i></span>
                  <span class="d-none d-sm-block">Home</span>
                </template>
                <p class="mb-0">
                  Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium,
                  totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta
                  sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                  consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui
                  dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non
                  numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem?
                </p>
              </b-tab>
              <b-tab id="profile" active>
                <template #title>
                  <span class="d-block d-sm-none"><i class="bx bx-user"></i></span>
                  <span class="d-none d-sm-block">Profile</span>
                </template>
                <p class="mb-0">
                  Li Europan lingues es membres del sam familie. Lor separat existentie es un myth. Por scientie,
                  musica, sport etc, litot Europa usa li sam vocabular. Li lingues differe solmen in li grammatica, li
                  pronunciation e li plu commun vocabules. Omnicos directe al desirabilite de un nov lingua franca: On
                  refusa continuar payar custosi traductores. At solmen va esser necessi far uniform grammatica,
                  pronunciation e plu sommun paroles. Ma quande lingues coalesce, li grammatica del resultant
                  lingue es plu simplic e regulari quam ti del coalescent lingues. Li nov lingua franca va esser plu
                  simplic e regulari quam li existent Europan lingues.
                </p>
              </b-tab>
              <b-tab id="settings">
                <template #title>
                  <span class="d-block d-sm-none"><i class="bx bx-envelope"></i></span>
                  <span class="d-none d-sm-block">Messages</span>
                </template>
                <p class="mb-0">
                  Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium,
                  totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta
                  sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                  consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui
                  dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non
                  numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem?
                </p>
              </b-tab>
            </b-tabs>
          </UIComponentCard>

          <UIComponentCard title="Tabs Vertical Left" id="toggle-between-modals">
            <b-row class="mt-3">
              <b-tabs content-class="pt-0" nav-class="flex-column" nav-wrapper-class="col-sm-3 mb-2 mb-sm-0" pills
                      vertical justified>
                <b-tab title="Home" id="home" active>
                  <p class="mb-0">
                    Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium,
                    totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae
                    dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit,
                    sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam
                    est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non
                    numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem?
                  </p>
                </b-tab>
                <b-tab title="Profile" id="profile">
                  <p class="mb-0">
                    Li Europan lingues es membres del sam familie. Lor separat existentie es un myth. Por scientie,
                    musica, sport etc, litot Europa usa li sam vocabular. Li lingues differe solmen in li grammatica, li
                    pronunciation e li plu commun vocabules. Omnicos directe al desirabilite de un nov lingua franca: On
                    refusa continuar payar custosi traductores. At solmen va esser necessi far uniform grammatica,
                    pronunciation e plu sommun paroles. Ma quande lingues coalesce, li grammatica del
                    resultant lingue es plu simplic e regulari quam ti del coalescent lingues. Li nov lingua franca va
                    esser plu simplic e regulari quam li existent Europan lingues.
                  </p>
                </b-tab>
                <b-tab title="Settings" id="settings">
                  <p class="mb-0">
                    Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium,
                    totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae
                    dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit,
                    sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam
                    est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non
                    numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem?
                  </p>
                </b-tab>
              </b-tabs>
            </b-row>
          </UIComponentCard>

          <UIComponentCard title="Tabs Vertical Right" id="varying-modal-content">
            <b-row class="mt-3">
              <b-tabs content-class="pt-0" nav-class="flex-column" nav-wrapper-class="col-sm-3 ms-2" pills vertical
                      justified :end="true">
                <b-tab title="Home" id="home" active>
                  <p class="mb-0">
                    Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium,
                    totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae
                    dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit,
                    sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam
                    est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non
                    numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem?
                  </p>
                </b-tab>
                <b-tab title="Profile" id="profile">
                  <p class="mb-0">
                    Li Europan lingues es membres del sam familie. Lor separat existentie es un myth. Por scientie,
                    musica, sport etc, litot Europa usa li sam vocabular. Li lingues differe solmen in li grammatica, li
                    pronunciation e li plu commun vocabules. Omnicos directe al desirabilite de un nov lingua franca: On
                    refusa continuar payar custosi traductores. At solmen va esser necessi far uniform grammatica,
                    pronunciation e plu sommun paroles. Ma quande lingues coalesce, li grammatica del
                    resultant lingue es plu simplic e regulari quam ti del coalescent lingues. Li nov lingua franca va
                    esser plu simplic e regulari quam li existent Europan lingues.
                  </p>
                </b-tab>
                <b-tab title="Settings" id="settings">
                  <p class="mb-0">
                    Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium,
                    totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae
                    dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit,
                    sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam
                    est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non
                    numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem?
                  </p>
                </b-tab>
              </b-tabs>
            </b-row>
          </UIComponentCard>
        </b-col>

        <b-col xl="3">
          <AnchorNavigation :elements="anchorNavigation"/>
        </b-col>
      </b-row>
  </VerticalLayout>
</template>

<script lang="ts" setup>
import VerticalLayout from "@/layouts/VerticalLayout.vue";

import AnchorNavigation from '@/components/AnchorNavigation.vue'
import UIComponentCard from '@/components/UIComponentCard.vue'

const anchorNavigation = [
  {
    id: 'default',
    title: 'Nav Tabs'
  },
  {
    id: 'static-backdrop',
    title: 'Static Backdrop'
  },
  {
    id: 'scrolling-long-content',
    title: 'Scrolling Long Content'
  },
  {
    id: 'toggle-between-modals',
    title: 'Toggle Between Modals'
  },
  {
    id: 'varying-modal-content',
    title: 'Varying Modal Content'
  }
]
</script>
