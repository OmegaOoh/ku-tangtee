<template>
    <div id="map" class="map"></div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-geosearch/dist/geosearch.css';
import markerIcon from '@/assets/marker.svg';
import { OpenStreetMapProvider, SearchControl } from 'leaflet-geosearch';

const marker = ref(null)
const map = ref(null)

const customIcon = L.icon({
    iconUrl: markerIcon,
    iconSize: [30, 30],
    iconAnchor: [15, 30],
    popupAnchor: [0, -30]
    });

const createMarker = (event) => {
    if (!map.value) return; // Map does not initialized.
    if (marker.value) {
        map.value.removeLayer(marker.value);
    }
    marker.value = L.marker(event.latlng, {icon: customIcon}).addTo(map.value);
    marker.value.bindPopup(`You clicked at ${event.latlng.toString()}`).openPopup();
} 

    onMounted(() => {
        map.value = L.map('map').setView([13.84800, 100.56762], 16);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 25,
            attribution: '© OpenStreetMap'
        }).addTo(map.value);

        // Onclick Action
        map.value.on('click', createMarker)

        //Search
        const searchControl = new SearchControl({
            provider: new OpenStreetMapProvider(),
            style: 'bar',
            autoComplete: true,
            autoCompleteDelay: 250,
            keepResult: false,
            showMarker: false,
            
            onResult: (result) => {
                map.value.setView(result.location, 18);
            },
        });

        map.value.addControl(searchControl);
        searchControl.addTo(map.value)

        })
</script>