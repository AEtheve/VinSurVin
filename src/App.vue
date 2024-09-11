<script setup lang="ts">
import { ref, provide } from 'vue';
const cartOpen = ref(false);
const productsInCard = ref([]);

provide('cartOpen', cartOpen);
provide('productsInCard', productsInCard);

function computeSubtotal() {
  let subtotal = 0;
  productsInCard.value.forEach((product) => {
    subtotal += product.price * product.quantity;
  });
  return subtotal;
}

function removeProductFromCart(id) {
  const index = productsInCard.value.findIndex((product) => product.id === id);
  productsInCard.value.splice(index, 1);
}
</script>

<template>
  <router-view />
  <router-view name="Home" />
  <router-view name="Catalog" />
  <router-view name="Account" />
  <router-view name="Product" />
  <router-view name="CartProcess" />

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
              <div>x1</div>
              <div>{{ product.price.toFixed(2).replace('.', ',') }} €</div>
            </div>
            <div style="font-size: 1.1rem; color: rgb(56 56 184); cursor:pointer;"
              @click="removeProductFromCart(product.id)"
            >Supprimer</div>
          </div>
        </div>
      </div>

      <div>Sous-total : {{ computeSubtotal().toFixed(2).replace('.', ',') }} €</div>
      <router-link to="/cartprocess"><button id="validate-cart" >Valider mon panier</button></router-link>
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
}
</style>
