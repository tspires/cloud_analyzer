<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="3" md="6">
          <b-card no-body class="mb-3 mb-xl-0">
            <img class="card-img-top img-fluid" :src="smallImg1" alt="img-1"/>
            <b-card-body>
              <b-card-title tag="h5" class="mb-2">Card title</b-card-title>
              <p class="card-text text-muted">Some quick example text to build on the card title and make up the bulk of
                the card's content. With supporting text below as a natural lead-in to additional content.</p>
              <a href="javascript:void(0);" class="btn btn-primary">Button</a>
            </b-card-body>
          </b-card>
        </b-col>
        <b-col xl="3" md="6">
          <b-card no-body class="mb-3">
            <img class="card-img-top img-fluid" :src="smallImg2" alt="img-2"/>
            <b-card-body>
              <b-card-title tag="h5" class="mb-2">Card title</b-card-title>
              <p class="card-text text-muted">Some quick example text to build on the card title.</p>
            </b-card-body>
            <ul class="list-group list-group-flush text-muted">
              <li class="list-group-item text-muted">Dapibus ac facilisis in</li>
            </ul>
            <b-card-body>
              <a href="javascript:void(0);" class="card-link text-primary">Card link</a>
              <a href="javascript:void(0);" class="card-link text-primary">Another link</a>
            </b-card-body>
          </b-card>
        </b-col>
        <b-col xl="3" md="6">
          <b-card no-body class="mb-3 mb-xl-0">
            <img class="card-img-top img-fluid" :src="smallImg4" alt="img-4"/>
            <b-card-body>
              <p class="card-text text-muted">Some quick example text to build on the card title and make up the bulk of the card's content. With supporting text below as a natural lead-in to additional content.</p>
              <a href="javascript:void(0);" class="btn btn-primary">Button</a>
            </b-card-body>
          </b-card>
        </b-col>
        <b-col xl="3" md="6">
          <b-card no-body class="mb-3 mb-xl-0">
            <b-card-body>
              <b-card-title tag="h5" class="mb-0">Card title</b-card-title>
            </b-card-body>
            <img class="img-fluid" :src="smallImg5" alt="img-5"/>
            <b-card-body>
              <p class="card-text text-muted">Some quick example text to build on the card title.</p>
              <a href="javascript:void(0);" class="card-link text-primary">Card link</a>
              <a href="javascript:void(0);" class="card-link text-primary">Another link</a>
            </b-card-body>
          </b-card>
        </b-col>
      </b-row>

      <b-row>
        <b-col sm="6">
          <b-card no-body class="card-body">
            <b-card-title tag="h5" class="mb-1"> Special title treatment</b-card-title>
            <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
            <a href="javascript: void(0);" class="btn btn-primary">Go somewhere</a>
          </b-card>
        </b-col>
        <b-col sm="6">
          <b-card no-body class="card-body">
            <b-card-title tag="h5" class="mb-1"> Special title treatment</b-card-title>
            <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
            <a href="javascript: void(0);" class="btn btn-primary">Go somewhere</a>
          </b-card>
        </b-col>
      </b-row>

      <b-row>
        <b-col md="4">
          <b-card no-body>
            <b-card-header>Featured</b-card-header>
            <b-card-body>
              <b-card-title tag="h5" class="mb-1"> Special title treatment</b-card-title>
              <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
              <a href="javascript: void(0);" class="btn btn-primary">Go somewhere</a>
            </b-card-body>
          </b-card>
        </b-col>
        <b-col md="4">
          <b-card no-body>
            <b-card-header>Quote</b-card-header>
            <b-card-body>
              <blockquote>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer posuere erat a ante.</p>
                <footer>
                  Someone famous in <cite>Source Title</cite>
                </footer>
              </blockquote>
            </b-card-body>
          </b-card>
        </b-col>
        <b-col md="4">
          <b-card no-body>
            <b-card-header>Featured</b-card-header>
            <b-card-body>
              <a href="javascript: void(0);" class="btn btn-primary">Go somewhere</a>
            </b-card-body>
            <b-card-footer class="text-muted">2 days ago</b-card-footer>
          </b-card>
        </b-col>
      </b-row>

      <b-row>
        <b-col cols="12">
          <b-card-title tag="h5" class="mb-3">Card Colored</b-card-title>
        </b-col>
      </b-row>

      <b-row>
        <b-col md="4">
          <b-card no-body class="text-bg-primary">
            <b-card-body>
              <b-card-title tag="h5" class="text-white mb-2">Special title treatment</b-card-title>
              <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
              <a href="javascript: void(0);" class="btn btn-light btn-sm">Button</a>
            </b-card-body>
          </b-card>
        </b-col>

        <b-col md="4">
          <b-card no-body class="bg-secondary text-white">
            <b-card-body>
              <blockquote>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer posuere erat a ante.</p>
                <footer> Someone famous in <cite title="Source Title">Source Title</cite>
                </footer>
              </blockquote>
            </b-card-body>
          </b-card>
        </b-col>

        <b-col md="4">
          <b-card no-body class="text-bg-success">
            <b-card-body>
              <blockquote>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer posuere erat a ante.</p>
                <footer> Someone famous in <cite title="Source Title">Source Title</cite>
                </footer>
              </blockquote>
            </b-card-body>
          </b-card>
        </b-col>

        <b-col md="4">
          <b-card no-body class="text-bg-info">
            <b-card-body>
              <blockquote>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer posuere erat a ante.</p>
                <footer> Someone famous in <cite title="Source Title">Source Title</cite>
                </footer>
              </blockquote>
            </b-card-body>
          </b-card>
        </b-col>

        <b-col md="4">
          <b-card no-body class="text-bg-warning">
            <b-card-body>
              <blockquote>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer posuere erat a ante.</p>
                <footer> Someone famous in <cite title="Source Title">Source Title</cite>
                </footer>
              </blockquote>
            </b-card-body>
          </b-card>
        </b-col>

        <b-col md="4">
          <b-card no-body class="text-bg-danger">
            <b-card-body>
              <blockquote>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer posuere erat a ante.</p>
                <footer> Someone famous in <cite title="Source Title">Source Title</cite>
                </footer>
              </blockquote>
            </b-card-body>
          </b-card>
        </b-col>
      </b-row>

      <b-row>
        <b-col cols="12">
          <b-card-title tag="h5" class="mb-3">Card Bordered</b-card-title>
        </b-col>
      </b-row>

      <b-row>
        <b-col md="4">
          <b-card no-body class="border-primary border">
            <b-card-body>
              <b-card-title tag="h5" class="text-primary mb-2"> Special title treatment</b-card-title>
              <p class="card-text">With supporting text below as a natural lead-in to additional content.</p>
              <a href="javascript: void(0);" class="btn btn-primary btn-sm">Button</a>
            </b-card-body>
          </b-card>
        </b-col>

        <b-col md="4">
          <b-card no-body class="border-secondary border">
            <b-card-body>
              <b-card-title tag="h5" class="mb-2"> Special title treatment</b-card-title>
              <p class="card-text">With supporting text below as a natural lead-in to additional content.</p>
              <a href="javascript: void(0);" class="btn btn-secondary btn-sm">Button</a>
            </b-card-body>
          </b-card>
        </b-col>

        <b-col md="4">
          <b-card no-body class="border-success border">
            <b-card-body>
              <b-card-title tag="h5" class="mb-2 text-success"> Special title treatment</b-card-title>
              <p class="card-text">With supporting text below as a natural lead-in to additional content.</p>
              <a href="javascript: void(0);" class="btn btn-success btn-sm">Button</a>
            </b-card-body>
          </b-card>
        </b-col>
      </b-row>

      <b-row>
        <b-col cols="12">
          <b-card-title tag="h5" class="mb-3">Horizontal Card</b-card-title>
        </b-col>
      </b-row>

      <b-row>
        <b-col lg="6">
          <b-card no-body>
            <b-row class="g-0">
              <b-col md="4">
                <img :src="smallImg1" class="img-fluid rounded-start h-100" alt="img-1"/>
              </b-col>
              <b-col md="8">
                <b-card-body>
                  <b-card-title tag="h5" class="mb-2"> Card title</b-card-title>
                  <p class="card-text">This is a wider card with supporting text below as a natural lead-in to
                    additional content. This content is a little bit longer.</p>
                  <p class="card-text">
                    <small class="text-muted">Last updated 3 mins ago</small>
                  </p>
                </b-card-body>
              </b-col>
            </b-row>
          </b-card>
        </b-col>
        <b-col lg="6">
          <b-card no-body>
            <b-row class="g-0">
              <b-col md="8">
                <b-card-body>
                  <b-card-title tag="h5" class="mb-2"> Card title</b-card-title>
                  <p class="card-text">This is a wider card with supporting text below as a natural lead-in to
                    additional content. This content is a little bit longer.</p>
                  <p class="card-text">
                    <small class="text-muted">Last updated 3 mins ago</small>
                  </p>
                </b-card-body>
              </b-col>
              <b-col md="4">
                <img :src="smallImg2" class="img-fluid rounded-end h-100" alt="img-2"/>
              </b-col>
            </b-row>
          </b-card>
        </b-col>
      </b-row>

      <b-row>
        <b-col cols="12">
          <b-card-title tag="h5" class="mb-3">Stretched link</b-card-title>
        </b-col>
      </b-row>

      <b-row>
        <b-col md="6" lg="3">
          <b-card no-body>
            <img :src="smallImg1" class="card-img-top" alt="img-1"/>
            <b-card-body>
              <b-card-title tag="h5" class="mb-2"> Card with stretched link</b-card-title>
              <a href="javascript:void(0);" class="btn btn-primary mt-2 stretched-link">Go somewhere</a>
            </b-card-body>
          </b-card>
        </b-col>
        <b-col md="6" lg="3">
          <b-card no-body>
            <img :src="smallImg2" class="card-img-top" alt="img-2"/>
            <b-card-body>
              <b-card-title tag="h5" class="mb-2">
                <a href="javascript:void(0);" class="text-primary stretched-link">Card with stretched link</a>
              </b-card-title>
              <p class="card-text">Some quick example text to build on the card up the bulk of the card's content.</p>
            </b-card-body>
          </b-card>
        </b-col>
        <b-col md="6" lg="3">
          <b-card no-body>
            <img :src="smallImg3" class="card-img-top" alt="img-3"/>
            <b-card-body>
              <b-card-title tag="h5" class="mb-2"> Card with stretched link</b-card-title>
              <a href="javascript:void(0);" class="btn btn-primary mt-2 stretched-link">Go somewhere</a>
            </b-card-body>
          </b-card>
        </b-col>
        <b-col md="6" lg="3">
          <b-card no-body>
            <img :src="smallImg4" class="card-img-top" alt="img-4"/>
            <b-card-body>
              <b-card-title tag="h5" class="mb-2">
                <a href="javascript:void(0);" class="stretched-link">Card with stretched link</a>
              </b-card-title>
              <p class="card-text">Some quick example text to build on the card up the bulk of the card's content.</p>
            </b-card-body>
          </b-card>
        </b-col>
      </b-row>

      <b-row>
        <b-col cols="12">
          <b-card-title tag="h5" class="mb-3">Card Group</b-card-title>
        </b-col>
      </b-row>

      <b-row>
        <b-col cols="12">
          <div class="card-group mb-3">
            <b-card no-body class="d-block">
              <img class="card-img-top" :src="smallImg1" alt="img-1"/>
              <b-card-body>
                <b-card-title tag="h5" class="mb-2"> Card title</b-card-title>
                <p class="card-text">This is a wider card with supporting text below as a natural lead-in to additional
                  content. This content is a little bit longer.</p>
                <p class="card-text">
                  <small class="text-muted">Last updated 3 mins ago</small>
                </p>
              </b-card-body>
            </b-card>
            <b-card no-body class="d-block">
              <img class="card-img-top" :src="smallImg2" alt="img-2"/>
              <b-card-body>
                <b-card-title tag="h5" class="mb-2"> Card title</b-card-title>
                <p class="card-text">This card has supporting text below as a natural lead-in to additional content.</p>
                <p class="card-text">
                  <small class="text-muted">Last updated 3 mins ago</small>
                </p>
              </b-card-body>
            </b-card>
            <b-card no-body class="d-block">
              <img class="card-img-top" :src="smallImg3" alt="img-3"/>
              <b-card-body>
                <b-card-title tag="h5" class="mb-2"> Card title</b-card-title>
                <p class="card-text">This is a wider card with supporting text below as a natural lead-in to additional
                  content. This card has even longer content than the first to show that equal height action.</p>
                <p class="card-text">
                  <small class="text-muted">Last updated 3 mins ago</small>
                </p>
              </b-card-body>
            </b-card>
          </div>
        </b-col>
      </b-row>

      <b-row>
        <b-col cols="12">
          <b-card-title tag="h5" class="mb-3">Card Decks</b-card-title>
        </b-col>
      </b-row>

      <b-row>
        <b-col cols="12">
          <b-row class="row-cols-1 row-cols-md-3 g-3">
            <b-col>
              <b-card no-body>
                <img :src="smallImg4" class="card-img-top" alt="img-4"/>
                <b-card-body>
                  <b-card-title tag="h5" class="mb-2"> Card title</b-card-title>
                  <p class="card-text">This is a longer card with supporting text below as a natural lead-in to
                    additional content. This content is a little bit longer.</p>
                  <p class="card-text">
                    <small class="text-muted">Last updated 3 mins ago</small>
                  </p>
                </b-card-body>
              </b-card>
            </b-col>
            <b-col>
              <b-card no-body>
                <img :src="smallImg3" class="card-img-top" alt="img-3"/>
                <b-card-body>
                  <b-card-title tag="h5" class="mb-2"> Card title</b-card-title>
                  <p class="card-text">This is a longer card with supporting text below as a natural lead-in to
                    additional content. This content is a little bit longer.</p>
                  <p class="card-text">
                    <small class="text-muted">Last updated 3 mins ago</small>
                  </p>
                </b-card-body>
              </b-card>
            </b-col>
            <b-col>
              <b-card no-body>
                <img :src="smallImg2" class="card-img-top" alt="img-2"/>
                <b-card-body>
                  <b-card-title tag="h5" class="mb-2"> Card title</b-card-title>
                  <p class="card-text">This is a longer card with supporting text below as a natural lead-in to
                    additional content. This content is a little bit longer.</p>
                  <p class="card-text">
                    <small class="text-muted">Last updated 3 mins ago</small>
                  </p>
                </b-card-body>
              </b-card>
            </b-col>
          </b-row>
        </b-col>
      </b-row>
  </VerticalLayout>
</template>

<script setup lang="ts">
import VerticalLayout from "@/layouts/VerticalLayout.vue";


import smallImg1 from '@/assets/images/small/img-1.jpg'
import smallImg2 from '@/assets/images/small/img-2.jpg'
import smallImg3 from '@/assets/images/small/img-3.jpg'
import smallImg4 from '@/assets/images/small/img-4.jpg'
import smallImg5 from '@/assets/images/small/img-5.jpg'
</script>
