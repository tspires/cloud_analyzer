<template>
  <VerticalLayout>
    <b-row>
      <b-col xl="9">
        <b-card no-body>
          <b-card-body>
            <b-card-title tag="h5" class="mb-1 anchor" id="basic-example"> Basic Example 
              <a class="anchor-link" href="#basic-example">#</a>
            </b-card-title>

            <b-row class="mt-3">
              <b-col md="3">
                <img :src="avatar2" alt="img" class="img-fluid avatar-xs rounded" />
                <p>
                  <code>.avatar-xs</code>
                </p>
                <img :src="avatar3" alt="img" class="img-fluid avatar-sm rounded mt-2" />
                <p class="mb-2 mb-sm-0">
                  <code>.avatar-sm</code>
                </p>
              </b-col>
              <b-col md="3">
                <img :src="avatar4" alt="img" class="img-fluid avatar-md rounded" />
                <p>
                  <code>.avatar-md</code>
                </p>
              </b-col>

              <b-col md="3">
                <img :src="avatar5" alt="img" class="img-fluid avatar-lg rounded" />
                <p>
                  <code>.avatar-lg</code>
                </p>
              </b-col>

              <b-col md="3">
                <img :src="avatar6" alt="img" class="img-fluid avatar-xl rounded" />
                <p class="mb-0">
                  <code>.avatar-xl</code>
                </p>
              </b-col>
            </b-row>
          </b-card-body>
        </b-card>

        <b-card no-body>
          <b-card-body>
            <b-card-title tag="h5" class="mb-1 anchor" id="rounded-circle"> Rounded Circle 
              <a class="anchor-link" href="#rounded-circle">#</a>
            </b-card-title>

            <b-row class="mt-3">
              <b-col md="4">
                <img :src="avatar7" alt="img" class="img-fluid avatar-md rounded-circle" />
                <p class="mt-1">
                  <code>.avatar-md .rounded-circle</code>
                </p>
              </b-col>

              <b-col md="4">
                <img :src="avatar8" alt="img" class="img-fluid avatar-lg rounded-circle" />
                <p>
                  <code>.avatar-lg .rounded-circle</code>
                </p>
              </b-col>

              <b-col md="4">
                <img :src="avatar9" alt="img" class="img-fluid avatar-xl rounded-circle" />
                <p class="mb-0">
                  <code>.avatar-xl .rounded-circle</code>
                </p>
              </b-col>
            </b-row>
          </b-card-body>
        </b-card>

        <b-card no-body>
          <b-card-body>
            <b-card-title tag="h5" class="mb-1 anchor" id="images-shapes"> Images Shapes
              <a class="anchor-link" href="#">#</a>
            </b-card-title>
            <p class="text-muted font-14 mb-3">Avatars with different sizes and shapes.</p>

            <div class="d-flex flex-wrap gap-3 align-items-end">
              <div>
                <img :src="smallImg2" alt="img" class="img-fluid rounded" width="200" />
                <p class="mb-0">
                  <code>.rounded</code>
                </p>
              </div>

              <div>
                <img :src="avatar5" alt="img" class="img-fluid rounded" width="120" />
                <p class="mb-0">
                  <code>.rounded</code>
                </p>
              </div>

              <div>
                <img :src="avatar7" alt="img" class="img-fluid rounded-circle" width="120" />
                <p class="mb-0">
                  <code>.rounded-circle</code>
                </p>
              </div>

              <div>
                <img :src="smallImg3" alt="img" class="img-fluid img-thumbnail" width="200" />
                <p class="mb-0">
                  <code>.img-thumbnail</code>
                </p>
              </div>

              <div>
                <img :src="avatar8" alt="img" class="img-fluid rounded-circle img-thumbnail" width="120" />
                <p class="mb-0">
                  <code>.rounded-circle .img-thumbnail</code>
                </p>
              </div>
            </div>
          </b-card-body>
        </b-card>
      </b-col>

      <b-col xl="3">
        <AnchorNavigation :elements="anchorNavigation" />
      </b-col>
    </b-row>
  </VerticalLayout>
</template>

<script lang="ts" setup>
import VerticalLayout from "@/layouts/VerticalLayout.vue";

import AnchorNavigation from '@/components/AnchorNavigation.vue';

import avatar2 from '@/assets/images/users/avatar-2.jpg';
import avatar3 from '@/assets/images/users/avatar-3.jpg';
import avatar4 from '@/assets/images/users/avatar-4.jpg';
import avatar5 from '@/assets/images/users/avatar-5.jpg';
import avatar6 from '@/assets/images/users/avatar-6.jpg';
import avatar7 from '@/assets/images/users/avatar-7.jpg';
import avatar8 from '@/assets/images/users/avatar-8.jpg';
import avatar9 from '@/assets/images/users/avatar-9.jpg';

import smallImg2 from '@/assets/images/small/img-2.jpg';
import smallImg3 from '@/assets/images/small/img-3.jpg';

const anchorNavigation = [
  {
    id: 'basic-example',
    title: 'Basic Example'
  },
  {
    id: 'rounded-circle',
    title: 'Rounded Circle'
  },
  {
    id: 'images-shapes',
    title: 'Images Shapes'
  }
];
</script>
