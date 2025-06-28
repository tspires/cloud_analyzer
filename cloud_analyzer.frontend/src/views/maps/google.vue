<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="9">
          <UIComponentCard title="Basic Example" id="basic">
            <div class="mt-3">
              <GoogleMap :api-key="api" :center="center" :zoom="5" class="gmaps"></GoogleMap>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Markers Google Map" id="google_map">
            <div class="mt-3">
              <GoogleMap :api-key="api" :center="center" :zoom="3" class="gmaps">
                <Marker v-for="(m, index) in markers" :key="index" :options="m.markerOptions" :clickable="true"
                        :draggable="true"></Marker>
              </GoogleMap>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Polygon Editing" id="polygon_editing">
            <div class="mt-3">
              <GoogleMap :api-key="api" :center="{ lat: 24.886, lng: -70.268 }" :zoom="4" class="gmaps">
                <Polygon :options="polygonOption" :editable="true"></Polygon>
              </GoogleMap>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Info Window" id="info_window">
            <div class="mt-3">
              <GoogleMap :api-key="api" :center="center" :zoom="10" class="gmaps">
                <InfoWindow :options="{ position: center, content: 'Hello viewer!' }"/>
              </GoogleMap>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Heatmap Layer" id="heatmap_layer">
            <div class="mt-3">
              <GoogleMap :api-key="api" :libraries="['visualization']" style="height: 300px"
                         :center="{ lat: 37.774546, lng: -122.433523 }" :zoom="13">
                <HeatmapLayer :options="heatmapData"/>
              </GoogleMap>
            </div>
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
import UIComponentCard from "@/components/UIComponentCard.vue";
import AnchorNavigation from '@/components/AnchorNavigation.vue'
import {ref} from 'vue'

import 'https://maps.googleapis.com/maps/api/js'
import {GoogleMap, Marker, Polygon, HeatmapLayer, InfoWindow} from 'vue3-google-map'

const api = ref('')
const center = ref({lat: -12.043333, lng: -77.028333})
const markers = ref([{markerOptions: {position: {lat: -12.04, lng: -77.0}, label: 'Hi', title: 'Hello from marker'}}])

const polygonOption = {
  paths: [
    {lat: 25.774, lng: -80.19},
    {lat: 18.466, lng: -66.118},
    {lat: 32.321, lng: -64.757},
    {lat: 25.774, lng: -80.19}
  ],
  strokeColor: '#FF0000',
  strokeOpacity: 0.8,
  strokeWeight: 2,
  fillColor: '#FF0000',
  fillOpacity: 0.35
}
const heatmapData = {
  data: [
    {location: {lat: 37.782, lng: -122.447}, weight: 0.5},
    {lat: 37.782, lng: -122.445},
    {location: {lat: 37.782, lng: -122.443}, weight: 2},
    {location: {lat: 37.782, lng: -122.441}, weight: 3},
    {location: {lat: 37.782, lng: -122.439}, weight: 2},
    {lat: 37.782, lng: -122.437},
    {location: {lat: 37.782, lng: -122.435}, weight: 0.5},

    {location: {lat: 37.785, lng: -122.447}, weight: 3},
    {location: {lat: 37.785, lng: -122.445}, weight: 2},
    {lat: 37.785, lng: -122.443},
    {location: {lat: 37.785, lng: -122.441}, weight: 0.5},
    {lat: 37.785, lng: -122.439},
    {location: {lat: 37.785, lng: -122.437}, weight: 2},
    {location: {lat: 37.785, lng: -122.435}, weight: 3}
  ]
}

const anchorNavigation = [
  {
    id: 'basic',
    title: 'Basic'
  },
  {
    id: 'google_map',
    title: 'Markers Google Map'
  },
  {
    id: 'polygon_editing',
    title: 'Polygon Editing'
  },
  {
    id: 'info_window',
    title: 'Info Window'
  },
  {
    id: 'heatmap_layer',
    title: 'Heatmap Layer'
  }
]
</script>
