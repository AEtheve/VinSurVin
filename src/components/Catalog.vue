<script setup lang="ts">
import { ref } from 'vue'
import ProductBox from './ProductBox.vue'

const products = ref([]);

const fetchProducts = async () => {
  const response = await fetch('http://localhost:8000/products/');
  const data = await response.json();

  data.forEach((product) => {
    console.log(product);
    products.value.push({
      name: product.name,
      price: product.price,
      promo: product.promo,
      image: product.image,
    });
  });
};

fetchProducts();

</script>

<template>
  <div  style="padding-left: 3%;">
    <button class="filter-button"><i class="fa-solid fa-sliders"></i>Trier et filtrer</button>
    <div  style="display: inline-flex; gap: 25px;">
      <ProductBox v-for="product in products" :product="product" />
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
  margin-top: 5px ;
}

#cart_content {
  position: fixed;
  top: 0;
  right: 0;
  background: white;
  padding: 20px;
  height: 100%;
}

#close_cart {
  text-align: right;
}

.filter-button {
  background: #e9e9e9;
  display: flex;
  border:none;
  color:black;
  padding: 15px;
  border-radius: 10px;
  margin-left: 90%;
}
</style>
