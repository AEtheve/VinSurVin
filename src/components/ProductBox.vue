<script setup lang="ts">
import { defineProps } from 'vue';

defineProps<{
  product: {
    name: string;
    price: number;
    promo: number;
    image: string;
  };
}>();
</script>
<template>
  <div>
    <div id="product-box">
      <div class="product_card" :style="{ backgroundImage: `url(${product.image})` }"></div>
      <div style="display: inline-flex; flex-direction: column; text-align: center;">
        <!-- <span style="font-weight: 600; font-size: 1.2rem;">Vins exquis de la région</span> -->
        <span style="font-weight: 600; font-size: 1.2rem;">{{ product.name }}</span>
        <div v-if="product.promo > 0" class="product-price">
          <span class="promo">{{ product.price.toFixed(2).replace('.', ',') }}€</span>
          <span class="promo-pourcent">-{{ product.promo }}%</span>
          <div class="promo-price">{{ (product.price * (1 - product.promo / 100)).toFixed(2).replace('.', ',') }}€</div>
          <div><button>Ajouter au panier</button></div>
        </div>
        <div v-else class="product-price">{{ product.price.toFixed(2).replace('.', ',') }}€
          <!-- AJOUTE un espace de la taille de la promo -->
          <div style="height: 20px;"></div>
          <div><button>Ajouter au panier</button></div>
        </div>
      </div>


    </div>
  </div>
</template>
<style scoped>
.product_card {
  background-size: cover;
  background-position: center;
  height: 360px;
  width: 240px;
  margin: 0px;
}


button {
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
  border: 1px solid black;
}


#product-box {
  display: inline-flex;
  flex-direction: column;
}

.product-price {
  padding: 3px;
  font-weight: 600;
}

.promo {
  text-decoration: line-through;
  font-weight: 400;
}
</style>