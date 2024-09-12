<script setup lang="ts">
import { ref } from 'vue'
import ProductBox from './ProductBox.vue'
import LowerPage from './LowerPage.vue'

const products = ref([]);

const fetchProducts = async () => {
  const response = await fetch('http://localhost:8000/products/');
  const data = await response.json();

  data.forEach((productData) => {
    const product = productData.fields;
    products.value.push({
      name: product.name,
      price: product.price,
      promo: product.promo,
      image: product.image,
      grape_variety: product.grape_variety,
      region: product.region,
      millesime: product.millesime,
      appelation: product.appelation,
      type: product.type,
    });
  });
};

fetchProducts();


</script>

<template>
  <div style="padding-left: 3%;">
    <button class="filter-button"><i class="fa-solid fa-sliders"></i>Trier et filtrer</button>
    <div style="display: inline-flex; gap: 25px; flex-wrap: wrap; row-gap: 100px;">
      <ProductBox v-for="product in products" :product="product" />
    </div>
    <LowerPage />
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


.filter-button {
  background: #e9e9e9;
  display: flex;
  border: none;
  color: black;
  padding: 15px;
  border-radius: 10px;
  margin-left: 90%;
}
</style>
