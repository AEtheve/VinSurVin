<script setup lang="ts">
import { inject } from 'vue';
import LowerPage from './LowerPage.vue';
import Catalog from './Catalog.vue';
</script>

<template>
  <div>
    <div style="background: rgb(55, 67, 50); height: 560px;
    mask-image: linear-gradient(rgb(0 0 0 / 90%), rgb(0 0 0));
    ">
      <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;">
        <video src="../assets/wine_video.mp4" autoplay loop muted style="width: 100%; height: 100%; object-fit: cover; opacity: 0.7; background-color: black;"></video>
        
        <div style="position: absolute; top: 70%; left: 35%; transform: translate(-90%, -50%); color: white; font-size: 1.8rem;">
          <h1>Découvrez nos vins</h1>
          <p style="font-size: 1.2rem; text-align: left; width: 380px;">
            Naviguez facilement parmi nos catégories et trouvez le vin parfait pour chaque occasion.
          </p>
          <router-link to="/boutique">
            <button style="background: #5A5A5A; color: white; padding: 20px 20px; border: none; border-radius: 28px; cursor: pointer; font-size: 1.1rem; width: 200px; margin-top: 20px;">
              Explorer
            </button>
          </router-link>
        </div>
      </div>
    </div>

    <LowerPage></LowerPage>
  </div>
</template>

<style scoped>
#cart_box {
  font-size: 1.4rem;
  color: black;
  position: fixed;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  left: 0;
}

#cart_content {
  position: fixed;
  top: 0;
  right: 0;
  background: white;
  padding: 20px;
  height: 100%;
}

#close_cart {
  text-align: right;
}
</style>
