<script setup lang="ts">
import { inject } from 'vue';
import LowerPage from './LowerPage.vue';
import Catalog from './Catalog.vue';
</script>

<template>
  <div>
    <div style="background: rgb(55, 67, 50); height: 100vh;
    mask-image: linear-gradient(rgb(0 0 0 / 90%), rgb(0 0 0));
    ">
      <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;">
        <video src="https://vinsurvin-bucket.s3.eu-west-3.amazonaws.com/wine_video.mp4" autoplay loop muted playsinline
          style="width: 100%; height: 100%; object-fit: cover; opacity: 0.7; background-color: black;"></video>

        <div id="video-content">
          <h1>Découvrez nos vins</h1>
          <p style="font-size: 1.2rem; text-align: left; width: 380px;">
            Naviguez facilement parmi nos catégories et trouvez le vin parfait pour chaque occasion.
          </p>
          <router-link to="/boutique">
            <button id="explorer_button" class="explore-button">
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
#cart_content {
  position: fixed;
  top: 0;
  right: 0;
  background: white;
  padding: 20px;
  height: 100%;
}

.explore-button {
  background: #5A5A5A;
  color: white;
  padding: 20px 20px;
  border: none;
  border-radius: 28px;
  cursor: pointer;
  font-size: 1.1rem;
  width: 200px;
  margin-top: 20px;
  transition: background 0.3s, transform 0.3s;
}

.explore-button:hover {
  background: #434343;
  transform: scale(1.05);
}

#video-content {
  position: absolute;
  top: 70%;
  left: 35%;
  transform: translate(-90%, -50%);
  color: white;
  font-size: 1.8rem;
}

@media (max-width: 1091px) {
  .explore-button {
    width: 150px;
    font-size: 1rem;
  }

  #video-content {
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 1.5rem;
  }
}

@media (max-width: 1400px) {
  #video-content {
    left: 40%;
  }

  h1 {
    font-size: 2.5rem;
  }
}
</style>
