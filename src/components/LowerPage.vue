<script setup>
import { ref } from 'vue'

const count = ref(0)
</script>

<template>
<div style="text-align: center; margin-top: 50px; z-index: 0;">
    <img src="https://vinsurvin-bucket.s3.eu-west-3.amazonaws.com/bandeau_boissons_alcooliques.jpg" alt="wine_bottom" style="width: 100%; height: 150px; object-fit: scale-down;">
    @Vin/20 Corporation -
    <a href="/legalmentions" class="button">Legal mentions</a>
    <a href="/salesconditions" class="button">CGV</a>
</div>
</template>
    
<style>
.center {
    text-align: center;
    padding: 20px;
}

.button {
    padding-right: 20px;
    margin-bottom: 10px;
}

.button:hover {
    background-color: #f1f1f1;
    color: black;
}
</style>