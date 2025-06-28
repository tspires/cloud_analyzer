<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="9">

          <UIComponentCard title="World Vector Map" id="world_vector_map">
            <div class="mt-3">
              <JsVectorMap id="world-map-markers" :height="360" :options="worldMapOptions"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Canada Vector Map" id="canada_vector_map">
            <div class="mt-3">
              <JsVectorMap id="canada-vector-map" :height="360" :options="canadaMap"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Russia Vector Map" id="russia_vector_map">
            <div class="mt-3">
              <JsVectorMap id="russia-vector-map" :height="360" :options="russiaMap"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Iraq Vector Map" id="iraq_vector_map">
            <div class="mt-3">
              <JsVectorMap id="iraq-vector-map" :height="360" :options="iraqMap"/>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Spain Vector Map" id="spain_vector_map">
            <div class="mt-3">
              <JsVectorMap id="spain-vector-map" :height="360" :options="spainMap"/>
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
import AnchorNavigation from '@/components/AnchorNavigation.vue'
import JsVectorMap from '@/components/JsVectorMap.vue'
import UIComponentCard from "@/components/UIComponentCard.vue";

const worldMapOptions = {
  map: 'world',
  selector: '#world-map-markers',
  zoomOnScroll: false,
  zoomButtons: true,
  markersSelectable: true,
  markers: [
    {name: 'Greenland', coords: [72, -42]},
    {name: 'Canada', coords: [56.1304, -106.3468]},
    {name: 'Brazil', coords: [-14.235, -51.9253]},
    {name: 'Egypt', coords: [26.8206, 30.8025]},
    {name: 'Russia', coords: [61, 105]},
    {name: 'China', coords: [35.8617, 104.1954]},
    {name: 'United States', coords: [37.0902, -95.7129]},
    {name: 'Norway', coords: [60.472024, 8.468946]},
    {name: 'Ukraine', coords: [48.379433, 31.16558]}
  ],
  markerStyle: {
    initial: {fill: '#5B8DEC'},
    selected: {fill: '#ef5f5f'}
  },
  labels: {
    markers: {
      render: (marker: any) => marker.name
    }
  },
  regionStyle: {
    initial: {
      fill: 'rgba(169,183,197, 0.2)',
      fillOpacity: 1
    }
  }
}

const canadaMap = {
  map: 'canada',
  selector: '#canada-vector-map',
  zoomOnScroll: false,
  regionStyle: {
    initial: {
      fill: '#1e84c4'
    }
  }
}

const russiaMap = {
  map: 'russia',
  selector: '#russia-vector-map',
  zoomOnScroll: false,
  regionStyle: {
    initial: {
      fill: '#1bb394'
    }
  }
}

const iraqMap = {
  map: 'iraq',
  selector: '#iraq-vector-map',
  zoomOnScroll: false,
  regionStyle: {
    initial: {
      fill: '#f8ac59'
    }
  }
}

const spainMap = {
  map: 'spain',
  selector: '#spain-vector-map',
  zoomOnScroll: false,
  regionStyle: {
    initial: {
      fill: '#23c6c8'
    }
  }
}

const anchorNavigation = [
  {
    id: 'world_vector_map',
    title: 'World Vector Map'
  },
  {
    id: 'canada_vector_map',
    title: 'Canada Vector Map'
  },
  {
    id: 'russia_vector_map',
    title: 'Russia Vector Map'
  },
  {
    id: 'iraq_vector_map',
    title: 'Iraq Vector Map'
  },
  {
    id: 'spain_vector_map',
    title: 'Spain Vector Map'
  }
]
</script>
