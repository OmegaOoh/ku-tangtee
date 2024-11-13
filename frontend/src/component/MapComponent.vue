<template>
    <div id="map" class="map"></div>
</template>

<script setup>
import { onMounted, ref, defineProps } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-geosearch/dist/geosearch.css';
import markerIcon from '@/assets/marker.svg';

const marker = ref(null)
const map = ref(null)

const props = defineProps({
    latitude: {
        type: Number,
        Required: true,
    },
    longitude: {
        type: Number,
        Required: true,
    }
})


const customIcon = L.icon({
    iconUrl: markerIcon,
    iconSize: [30, 30],
    iconAnchor: [15, 30],
    popupAnchor: [0, -30]
    });

    onMounted(() => {
        map.value = L.map('map').setView([props.latitude, props.longitude], 18);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 18,
            attribution: '© OpenStreetMap'
        }).addTo(map.value);
        marker.value = L.marker(L.latLng(props.latitude, props.longitude), {icon: customIcon}).addTo(map.value);
    })

    
</script>