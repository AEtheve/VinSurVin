<script setup lang="ts">
import { provide } from 'vue';
import { defineProps, ref,inject, onMounted } from 'vue';


const showPopup = ref(false);
const popupMessage = ref('');

function showPopupNotification(message: string) {
  popupMessage.value = message;
  showPopup.value = true;

  setTimeout(() => {
    showPopup.value = false;
  }, 3000); 
}

const props = defineProps<{
  product: {
    name: string;
    price: number;
    promo: number;
    image: string;
    description: string;

    pk: number;  
    grape_variety?: string;
    region?: string;
    millesime?: number;
    appellation?: string;
    type?: string;
  };
}>();



const productsInCard = inject('productsInCard');

const quantity = ref(1);

function increment() {
  quantity.value++;
}

function decrement() {
  if (quantity.value > 1) {
    quantity.value--;
  }
}

function addToCart() {
  fetch('http://localhost:8000/add-to-cart/', {
    method: 'POST',
    credentials: "include",
    mode: 'cors',
    body: JSON.stringify({
      product: props.product.pk,
      quantity: quantity.value
    })
  }).then(response => response.json())
  .then(data => {
    
  productsInCard.value.push({
    pk: props.product.pk,
    name: props.product.name,
    price: props.product.price,
    promo: props.product.promo,
    image: props.product.image,
    description: props.product.description,
    quantity: quantity.value
  });
  localStorage.setItem('cart', JSON.stringify(productsInCard.value));
  showPopupNotification('Produit ajouté au panier !');
  });

}

provide('addToCart', addToCart);
</script>


<template>
  <div>
    <div id="product-box">
      <a :href="'/product/' + product.pk">
        <div class="product_card" :style="{ backgroundImage: 'url(' + product.image + ')' }">
          <div class="overlay">
            <div class="description">
              <p v-if="product.type"><strong>Type:</strong> {{ product.type }}</p>
              <p><strong>Appellation:</strong> {{ product.appellation ? product.appellation : 'Non spécifiée' }}</p>
              <p><strong>Région:</strong> {{ product.region ? product.region : 'Non spécifiée' }}</p>
              <p v-if="product.millesime"><strong>Millésime:</strong> {{ product.millesime }}</p>
              <p><strong>Cépage:</strong> {{ product.grape_variety ? product.grape_variety : 'Non spécifié' }}</p>
            </div>
          </div>
        </div>
      </a>
      <div class="price-box">
        <span style="font-weight: 600; font-size: 1.2rem;">{{ product.name }}</span>   
        <div class="product-price">
          <div class="promo-details">
            <div v-if="product.promo > 0">
              <span class="promo">{{ product.price.toFixed(2).replace('.', ',') }}€</span>
              <span class="promo-pourcent">-{{ product.promo }}%</span>
              <div class="promo-price">{{ (product.price * (1 - product.promo / 100)).toFixed(2).replace('.', ',') }}€</div>
            </div>
            <div v-else>
              <span>{{ product.price.toFixed(2).replace('.', ',') }}€</span>
            </div>
          </div>
          <div class="quantity-product-button">
            <button class="quantity_button" @click="decrement">-</button>
            <input class="quantity_input" :value="quantity" readonly />
            <button class="quantity_button" @click="increment">+</button>
          </div>
          <button class="cart_button" @click="addToCart">Ajouter au panier</button>
        </div>
      </div>
    </div>
  </div>
  <transition name="fade">
    <div v-if="showPopup" class="popup-notification">
      {{ popupMessage }}
    </div>
  </transition>
</template>


<style scoped>

.popup-notification {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  z-index: 1001;
  transition: opacity 0.3s ease;
}

.popup-notification.fade-enter-active, .popup-notification.fade-leave-active {
  transition: opacity 0.3s ease;
}

.popup-notification.fade-enter, .popup-notification.fade-leave-to {
  opacity: 0;
}


.quantity_input {
  border: 1px solid black;
  padding: 10px;
  border-radius: 10px;
  height: 20px;
  text-align: center;
}

.product_card {
  position: relative;
  background-size: cover;
  background-position: center;
  height: 360px;
  width: 240px;
  margin: 0px;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.product_card:hover {
  transform: scale(1.05);
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.3);
}

.promo-details {
    min-height: 50px; 
    margin-bottom: 10px;
}
.overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.8);
  opacity: 0;
  transition: opacity 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.product_card:hover .overlay {
  opacity: 1;
}

.description {
  font-size: 0.9rem;
  text-align: left;
  color: black;
  padding: 20px;
  justify-content: center;
}

.quantity-product-button {
  display: inline-flex;
  gap: 10px;
  display: inline-flex;
  width: auto;
  align-items: center;
  justify-content: center;
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

.cart_button {
  padding: 10px;
  margin: 10px;
  background: black;
  color: white;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

button:hover {
  background: white;
  color: black;
  border: 2px solid black;
}

#product-box {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  z-index: 1;
}

.product-price {
  padding: 3px;
  font-weight: 600;
  display: contents;
}

.promo {
  text-decoration: line-through;
  font-weight: 400;
  color: #d32f2f;
  margin: 5px;
}

.price-box {
  display: inline-flex;
  flex-direction: column;
  text-align: center;
  height: 131px;
  margin-top: 15px;
  justify-content: space-around;
}
</style>
