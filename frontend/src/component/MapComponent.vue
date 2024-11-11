<template>
    <div id="map" class="map"></div>
</template>

<script setup>
    import { onMounted, ref } from 'vue';
    import L from 'leaflet';
    import 'leaflet/dist/leaflet.css';
    import markerIcon from '@/assets/marker.svg';

    const marker = ref(null)
    const map = ref(null)

    onMounted(() => {
        map.value = L.map('map').setView([13.84800, 100.56762], 16);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 25,
            attribution: '© OpenStreetMap'
        }).addTo(map.value);

        const customIcon = L.icon({
        iconUrl: markerIcon,
        iconSize: [30, 30],
        iconAnchor: [15, 30],
        popupAnchor: [0, -30]
        });

        map.value.on('click', function(e) {
            if (marker.value) {
                map.value.removeLayer(marker.value);
            }
            marker.value = L.marker(e.latlng, {icon: customIcon}).addTo(map.value);
            marker.value.bindPopup(`You clicked at ${e.latlng.toString()}`).openPopup();
        })

    })
</script>