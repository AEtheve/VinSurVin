<script setup lang="ts">
import { ref, provide, computed } from 'vue';
const cartOpen = ref(false);
const productsInCard = ref(JSON.parse(localStorage.getItem('cart')) || []);
const isCartEmpty = computed(() => productsInCard.value.length === 0);
const dialogMenuMobile = ref(false);
const productlist = ref([]);
const currentPage = ref(1);
const totalPages = ref(1);

const showAgeCheckDialog = ref(localStorage.getItem('adultCheck') !== 'true');

function confirmAdult() {
  localStorage.setItem('adultCheck', 'true');
  showAgeCheckDialog.value = false;
}

function refuseAdult() {
  localStorage.setItem('adultCheck', 'false');
  alert('Vous devez être majeur pour accéder à ce site.');
}


provide('isCartEmpty', isCartEmpty);
provide('cartOpen', cartOpen);
provide('productsInCard', productsInCard);
provide('dialogMenuMobile', dialogMenuMobile);
provide('productlist', productlist);
provide('currentPage', currentPage);
provide('totalPages', totalPages);


function computeSubtotal() {
  let subtotal = 0;
  productsInCard.value.forEach((product) => {
    subtotal += (product.price * (1 - product.promo / 100)) * product.quantity;
  });
  return subtotal;
}

function clearCart() {
  productsInCard.value = [];
  localStorage.setItem('cart', JSON.stringify(productsInCard.value));
  console.log('Cart cleared', productsInCard.value);
  console.log('Is Cart Empty:', isCartEmpty.value);
  fetch(`//${window.location.hostname}:8000/delete-cart/`, {
    method: 'POST',
    credentials: 'include',
    mode: 'cors',
  });
}

function removeProductFromCart(id, quantity) {
  const index = productsInCard.value.findIndex((product) => product.pk === id);

  fetch(`//${window.location.hostname}:8000/remove-from-cart/`, {
    method: 'POST',
    credentials: 'include',
    mode: 'cors',
    body: JSON.stringify({
      product: id,
      quantity: quantity,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.message) {
        productsInCard.value.splice(index, 1);
        localStorage.setItem('cart', JSON.stringify(productsInCard.value));
      }
    });
}
provide('removeProductFromCart', removeProductFromCart);
</script>

<template>

<div v-if="showAgeCheckDialog" class="age-check-dialog">
    <div class="age-check-content">
      <h2>Êtes-vous majeur ?</h2>
      <p>Vous devez avoir 18 ans ou plus pour accéder à ce site.</p>
      <div class="age-check-actions">
        <button @click="confirmAdult">Oui, je suis majeur</button>
        <button @click="refuseAdult">Non</button>
      </div>
    </div>
  </div>

  <router-view />
  <router-view name="Home" />
  <router-view name="Catalog" />
  <router-view name="Account" />
  <router-view name="Product" />
  <router-view name="CartProcess" />
  <router-view name="LegalMentions" />
  <router-view name="SalesConditions" />

  <div id="cart_box" v-if="cartOpen">
    <div id="cart_content">
      <div id="close_cart" @click="cartOpen = false"><svg data-v-2f9813ef="" width="16" height="16" viewBox="0 0 16 16"
          fill="none" xmlns="http://www.w3.org/2000/svg">
          <path data-v-2f9813ef="" d="M12 4L4 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"
            stroke-linejoin="round"></path>
          <path data-v-2f9813ef="" d="M4 4L12 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"
            stroke-linejoin="round"></path>
        </svg></div>
      <div style="display: flex; flex-direction: column; gap: 30px; margin-bottom: 20px;">
        <div v-for="product in productsInCard" :key="product.id" style="display: inline-flex; gap: 21px;">
          <div data-v-0ec6eb9a="" class="product_card" style="
          width: 60px;
          height: 90px;" :style="{ backgroundImage: `url(${product.image})` }">
          </div>
          <div style="display: inline-flex; flex-direction: column; padding: 1px; gap: 8px;">
            <div style="font-weight: bold; font-size: 1.2rem;">{{ product.name }}</div>
            <div style="font-size: 1.2rem; display: inline-flex; gap: 60px;">
              <div>x{{ product.quantity }}</div>
              <div>{{ (product.price * (1 - product.promo / 100)).toFixed(2).replace('.', ',') }} €</div>
            </div>
            <div style="font-size: 1.1rem; color: rgb(56 56 184); cursor:pointer;"
              @click="removeProductFromCart(product.pk, product.quantity)">Supprimer</div>
          </div>
        </div>
      </div>

      <div>Sous-total : {{ computeSubtotal().toFixed(2).replace('.', ',') }} €</div>
      <router-link to="/cartprocess"><button id="validate-cart">Valider mon panier</button></router-link>
      <button @click="clearCart" :disabled="isCartEmpty" class="clear-cart-button">
        Vider le panier
      </button>
    </div>
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
  z-index: 1001;
  top: 0%;
}

#cart_content {
  position: fixed;
  top: 0;
  right: 0;
  background: white;
  padding: 20px;
  height: 100%;
  width: 20vw;
  text-align: center;

  overflow-y: auto;
  max-height: 100vh;
}


#close_cart {
  text-align: right;
}

#promo-border {
  height: 40px;
  width: 100%;
  background: #2c2c2c;
  position: absolute;
  top: 0;
  color: white;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  text-transform: uppercase;
}

button {
  padding: 15px;
  margin: 20px;
  background: black;
  color: white;
  border-radius: 10px;
  font-size: 1.1rem;
  cursor: pointer;
  border: 1px solid white;

}

button:hover {
  background: white;
  color: black;
  border: 1px solid black;
}

.clear-cart-button {
  padding: 10px 20px;
  background-color: rgb(252, 107, 107);
  color: white;
  border: 1px solid black;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease, transform 0.3s ease;
}

.clear-cart-button:hover {
  background-color: rgb(233, 76, 76);
}

.clear-cart-button:disabled {
  background-color: #ccc;
  color: #666;
  cursor: not-allowed;
  transform: none;
}


.age-check-dialog {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.age-check-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
}

.age-check-actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
  justify-content: center;
}

</style>
