<script setup lang="ts">
import { provide, Ref } from 'vue';
import { defineProps, ref, inject } from 'vue';


const showPopup = ref(false);
const popupMessage = ref('');
const isError = ref(false);

function showPopupNotification(message: string) {
  popupMessage.value = message;
  showPopup.value = true;

  setTimeout(() => {
    showPopup.value = false;
  }, 3000);
}

function showPopupError(message: string) {
  popupMessage.value = message;
  showPopup.value = true;
  isError.value = true;

  setTimeout(() => {
    showPopup.value = false;
  }, 5000);
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
    stock: number;
  };
}>();

type Product = {
  pk: number;
  name: string;
  price: number;
  promo: number;
  image: string;
  description: string;
  quantity: number;
  stock: number;
};
const productsInCard = inject('productsInCard') as Ref<Product[]>;

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
  fetch(`//${window.location.hostname}:8000/add-to-cart/`, {
    method: 'POST',
    credentials: "include",
    mode: 'cors',
    body: JSON.stringify({
      product: props.product.pk,
      quantity: quantity.value
    })
  }).then(response => response.json())
    .then(_ => {
      if (_.error === 'Insufficient stock') {
        showPopupError('Stock insuffisant !');
        return;
      }

      const existingProductIndex = productsInCard.value.findIndex((product) => product.pk === props.product.pk);

      if (existingProductIndex !== -1) {
        productsInCard.value[existingProductIndex].quantity += quantity.value;
      } else {
        productsInCard.value.push({
          pk: props.product.pk,
          name: props.product.name,
          price: props.product.price,
          promo: props.product.promo,
          image: props.product.image,
          description: props.product.description,
          quantity: quantity.value
        });
      }
      

      localStorage.setItem('cart', JSON.stringify(productsInCard.value));
      showPopupNotification('Produit ajouté au panier !');
      quantity.value = 1;
      // window.location.reload(); 
    });
}

provide('addToCart', addToCart);
</script>

<template>
  <div>
    <div id="product-box">
      <a :href="'/product/' + props.product.pk">
        <div class="product_card" :style="{ backgroundImage: 'url(' + props.product.image + ')' }">
          <div class="overlay">
            <div class="description">
              <p v-if="props.product.type"><strong>Type:</strong> {{ props.product.type }}</p>
              <p><strong>Appellation:</strong> {{ props.product.appellation ? props.product.appellation : 'Non spécifiée'
              }}</p>
              <p><strong>Région:</strong> {{ props.product.region ? props.product.region : 'Non spécifiée' }}</p>
              <p v-if="props.product.millesime"><strong>Millésime:</strong> {{ props.product.millesime }}</p>
              <p><strong>Cépage:</strong> {{ props.product.grape_variety ? props.product.grape_variety : 'Non spécifié' }}                 
              </p>
              <p><strong>Stock:</strong> {{ props.product.Stock ? props.product.Stock : 'Stock épuisé' }}</p>
            </div>
          </div>
        </div>
      </a>
      <div class="price-box">
        <span style="font-weight: 600; font-size: 1.2rem;">{{ props.product.name }}</span>
        <div class="product-price">
          <div class="promo-details">
            <div v-if="props.product.promo > 0">
              <span class="promo">{{ props.product.price.toFixed(2).replace('.', ',') }}€</span>
              <span class="promo-pourcent">-{{ props.product.promo }}%</span>
              <div class="promo-price">{{ (props.product.price * (1 - props.product.promo / 100)).toFixed(2).replace('.',
                ',') }}€</div>
            </div>
            <div v-else>
              <span>{{ props.product.price.toFixed(2).replace('.', ',') }}€</span>
            </div>
          </div>
          <div class="quantity-product-button">
            <button class="quantity_button" @click="decrement">-</button>
            <input class="quantity_input" :value="quantity" readonly />
            <button class="quantity_button" @click="increment">+</button>
          </div>
          <button class="cart_button" @click="addToCart" :disabled="quantity > props.product.Stock"
            :class="{ 'disabled-button': quantity > props.product.Stock }">
            {{ quantity > props.product.Stock ? 'Quantité insuffisante' : 'Ajouter au panier' }}
          </button>
        </div>
      </div>
    </div>
  </div>
  <transition name="fade">
    <div v-if="showPopup" class="popup-notification" :class="{ 'error-popup': isError }">
      <p>{{ popupMessage }}</p>
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
  transition: opacity 0.3s ease, background-color 0.3s ease;
}

.error-popup {
  background: red;
  color: white;
}

.popup-notification.fade-enter-active,
.popup-notification.fade-leave-active {
  transition: opacity 0.3s ease;
}

.popup-notification.fade-enter,
.popup-notification.fade-leave-to {
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
  height: 300px;
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

.cart_button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
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
  margin-top: 15px;
  justify-content: space-around;
}
</style>
