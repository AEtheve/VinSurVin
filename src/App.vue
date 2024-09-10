<script setup lang="ts">
import { ref, provide } from 'vue';
const cartOpen = ref(false);
provide('cartOpen', cartOpen);

</script>

<template>
  <router-view />
  <router-view name="Home" />
  <router-view name="Catalog" />
  <router-view name="Account" />
  <router-view name="Product" />


  <div id="cart_box" v-if="cartOpen">
      <div id="cart_content">
        <div id="close_cart" @click="cartOpen = false"><svg data-v-2f9813ef="" width="16" height="16" viewBox="0 0 16 16"
            fill="none" xmlns="http://www.w3.org/2000/svg">
            <path data-v-2f9813ef="" d="M12 4L4 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"
              stroke-linejoin="round"></path>
            <path data-v-2f9813ef="" d="M4 4L12 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"
              stroke-linejoin="round"></path>
          </svg></div>
        Votre panier vide
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
</style>
