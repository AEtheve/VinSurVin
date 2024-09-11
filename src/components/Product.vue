<script setup lang="ts">
import { ref } from 'vue';


// raw data
const product = ref({
  id: 1,
  name: "Vin Rouge",
  price: 25.99,
  promo: 10,
  image: "/images/Rouge.jpg",
  description: "Un vin rouge délicieux avec des notes de fruits rouges et d'épices.",
  cepage: "Merlot",
  region: "Bordeaux",
  millesime: 2020,
  appellation: "AOC Bordeaux",
  type: "Rouge",
});

const quantity = ref(1);
const showModal = ref(false);



function increment() {
  quantity.value++;
}

function decrement() {
  if (quantity.value > 1) {
    quantity.value--;
  }
}

function openModal() {
  showModal.value = true;
}

function closeModal() {
  showModal.value = false;
}
</script>

<template>
  <div class="product-page">
    <div class="back-arrow">
      <router-link to="/boutique">
        <span>&larr; Retour à la boutique</span>
      </router-link>
    </div>

    <div class="product-content">
      <div class="product-image">
        <img :src="product.image" :alt="product.name" @click="openModal" />
      </div>
      <div class="product-details">
        <h1 class="product-name">{{ product.name }}</h1>
        <p class="product-description">{{ product.description }}</p>
        <p class="product-cepage"><strong>Cépage:</strong> {{ product.cepage || 'Non spécifié' }}</p>
        <p class="product-region"><strong>Région:</strong> {{ product.region || 'Non spécifiée' }}</p>
        <p class="product-millesime"><strong>Millésime:</strong> {{ product.millesime || 'Non spécifié' }}</p>
        <p class="product-appellation"><strong>Appellation:</strong> {{ product.appellation || 'Non spécifiée' }}</p>
        <p class="product-type"><strong>Type:</strong> {{ product.type || 'Non spécifié' }}</p>
        <div class="quantity-product-button">
          <button class="quantity_button" @click="decrement">-</button>
          <input class="quantity_input" :value="quantity" readonly />
          <button class="quantity_button" @click="increment">+</button>
        </div>
        <div class="add-to-cart-container">
          <button class="cart_button">Ajouter au panier</button>
        </div>
      </div>
    </div>
    <div v-if="showModal" class="modal" @click="closeModal">
      <img class="modal-image" :src="product.image" :alt="product.name" />
    </div>
  </div>
</template>

<style scoped>
.quantity_input {
  border: 1px solid black;
  padding: 10px;
  border-radius: 10px;
  height: 20px;
  text-align: center;
  width: 25px;
}

.quantity-product-button {
  display: inline-flex;
  gap: 10px;
  display: inline-flex;
  width: auto;
  align-items: center;
  justify-content: center;
  margin-top: 1rem;
}

.add-to-cart-container {
  margin-top: 1rem; 
}

.quantity_button {
  background: black;
  color: white;
  margin: 10px;
  padding: 10px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.product-page {
  padding: 3%;
}

.back-arrow {
  margin-bottom: 1rem;
  font-size: 1.2rem;
  cursor: pointer;
}

.back-arrow span {
  color: #333;
  text-decoration: none;
}

.back-arrow span:hover {
  text-decoration: underline;
}

.product-content {
  display: flex;
  gap: 2rem;
}

.product-image img {
  cursor: zoom-in;
  height: 65vh;
  object-fit: contain;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.product-image img:hover {
  transform: scale(1.05);
}

.product-details {
  max-width: 600px;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-image {
  max-width: 90%;
  max-height: 90%;
  border-radius: 10px;
}

.modal-image:hover {
  cursor: zoom-out;
}

.product-name {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.product-description {
  margin-bottom: 1rem;
  line-height: 1.6;
}

.product-cepage,
.product-region,
.product-millesime,
.product-appellation,
.product-type {
  margin-bottom: 0.5rem;
}

.product-price {
  margin-top: 1.5rem;
  font-size: 1.5rem;
  color: #333;
}

.price-before {
  text-decoration: line-through;
  color: #888;
  margin-right: 0.5rem;
}

.price-promo {
  font-weight: bold;
  color: #d32f2f;
}

.promo-percent {
  font-size: 0.9rem;
  color: #d32f2f;
  margin-left: 0.5rem;
}

.cart_button {
  padding: 10px;
  margin: 10px;
  background: black;
  color: white;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  width: 60%;
}


button:hover {
  background: white;
  color: black;
  border: 2px solid black;
}
</style>
