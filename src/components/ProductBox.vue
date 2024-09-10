<script setup lang="ts">
import { ref } from 'vue';
import { defineProps } from 'vue';

defineProps<{
  product: {
    name: string;
    price: number;
    promo: number;
    image: string;
  };
}>();

const quantity = ref(1);

function increment() {
  quantity.value++;
}

function decrement() {
  if (quantity.value > 1) {
    quantity.value--;
  }
}
</script>

<template>
  <div>
    <div id="product-box">
      <div class="product_card" :style="{ backgroundImage: `url(${product.image})` }"></div>
      <div class="price-box">
        <span style="font-weight: 600; font-size: 1.2rem;">{{ product.name }}</span>
        <div v-if="product.promo > 0" class="product-price">
          <span class="promo">{{ product.price.toFixed(2).replace('.', ',') }}€</span>
          <span class="promo-pourcent">-{{ product.promo }}%</span>
          <div class="promo-price">{{ (product.price * (1 - product.promo / 100)).toFixed(2).replace('.', ',') }}€</div>
          <div class="quantity-product-button">
            <button class="quantity_button" @click="decrement">-</button>
            <input class="quantity_input" :value="quantity" readonly />
            <button class="quantity_button" @click="increment">+</button>
          </div>
            <button class="cart_button">Ajouter au panier</button>
        </div>
        <div v-else class="product-price">{{ product.price.toFixed(2).replace('.', ',') }}€
          <div class="quantity-product-button">
            <button class="quantity_button" @click="decrement">-</button>
            <input class="quantity_input" :value="quantity" readonly />
            <button class="quantity_button" @click="increment">+</button>
          </div>
          <button class="cart_button">Ajouter au panier</button>
        </div>
      </div>
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
}

.product_card {
  background-size: cover;
  background-position: center;
  height: 360px;
  width: 240px;
  margin: 0px;
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
}

.product-price {
  padding: 3px;
  font-weight: 600;
  display: contents;
}

.promo {
  text-decoration: line-through;
  font-weight: 400;
}

.price-box {
  display: inline-flex;
  flex-direction: column;
  text-align: center;
  height: 131px;
  margin-top: 5px;
  justify-content: space-around;
}
</style>
