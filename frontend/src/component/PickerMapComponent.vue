<template>
    <div id="map" class="map"></div>
</template>

<script setup>
import { onMounted, ref, defineEmits, defineProps, watch, nextTick } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-geosearch/dist/geosearch.css';
import markerIcon from '@/assets/marker.svg';
import { OpenStreetMapProvider, SearchControl } from 'leaflet-geosearch';


const props = defineProps({
    latitude: {
        type: Number,
        Required: false,
    },
    longitude: {
        type: Number,
        Required: false,
    }
})

const provider = new OpenStreetMapProvider()

const emit = defineEmits(['markerPlaced']);

const marker = ref(null)
const map = ref(null)

const customIcon = L.icon({
    iconUrl: markerIcon,
    iconSize: [30, 30],
    iconAnchor: [15, 30],
    popupAnchor: [0, -30]
    });

const onClick = (event) => {
    /**
     * Call create marker with latLng object
     */
    createMarker(event.latlng)
}

const createMarker = (coords) => {
    if (!map.value) return; // Map does not initialized.
    if (marker.value) {
        map.value.removeLayer(marker.value);
    }
    marker.value = L.marker(coords, {icon: customIcon}).addTo(map.value);
    emit('markerPlaced', { lat: coords.lat, lon: coords.lng });
} 

watch(() => [props.latitude, props.longitude], ([newLat, newLon]) => {
    if (!props.latitude || !props.longitude) return;
    nextTick(()=> {
        if (map.value) {
            const loc = L.latLng(newLat, newLon)
            console.log(loc)
            createMarker(loc);
        }
    })
},);

onMounted(() => {
    let loc = L.latLng(13.84800, 100.56762)
    if (props.latitude && props.longitude) {
        loc.lat = props.latitude;
        loc.lng = props.longitude; 
    }
    map.value = L.map('map').setView(loc,16);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '© OpenStreetMap'
    }).addTo(map.value);

    if (props.latitude && props.longitude) {
        map.value.setView(loc, 18)
        createMarker(loc);
    }

    // Onclick Action
    map.value.on('click', onClick)

    //Search
    const searchControl = new SearchControl({
        provider: provider,
        style: 'bar',
        keepResult: false,
        showMarker: false,
        onResult: (result) => {
            map.value.setView(result.location, 18);
            createMarker(result.latlng)
        },
    });

    map.value.addControl(searchControl);
    searchControl.addTo(map.value)
})
</script>