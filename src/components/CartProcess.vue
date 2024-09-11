<script setup lang="ts">
import { inject } from 'vue';
import { onMounted } from 'vue';

onMounted(() => {
  const cartOpen = inject("cartOpen");
  cartOpen.value = false;
});

const productsInCard = inject('productsInCard');

function computeSubtotal() {
  let subtotal = 0;
  productsInCard.value.forEach((product) => {
    subtotal += product.price * product.quantity;
  });
  return subtotal;
}
</script>

<template>
  <div style="padding-left: 3%; display: flex; gap: 20px; height: 80vh;">
    <div style="flex: 0.7 auto; border: 1px solid black; margin: 10px; padding-left: 20px;">
      <h2>Panier</h2>

      <div style="display: inline-flex; flex-direction: column; gap: 20px; overflow-y: auto;">
      <div v-for="product in productsInCard" :key="product.id" style="display: inline-flex; gap: 21px;">
        <div data-v-0ec6eb9a="" class="product_card" style="
        width: 120px;
        height: 180px;" :style="{ backgroundImage: `url(${product.image})` }">
          </div>
          <div style="display: inline-flex; flex-direction: column; padding: 1px; gap: 8px;">
            <div style="font-weight: bold; font-size: 1.2rem;">{{ product.name }}</div>
            <div style="font-size: 1.2rem; display: inline-flex; gap: 60px;">
              <div>Quantité : {{product.quantity}}</div>
              <div>{{ product.price.toFixed(2).replace('.', ',') }} €</div>
            </div>
            <div style="font-size: 1.1rem; color: rgb(56 56 184); cursor:pointer;">Supprimer</div>
          </div>
        </div>
      </div>
    </div>
    <div style="flex: 0.3 auto; border: 1px solid black; margin: 10px; padding-left: 20px;">
      <h2>Récapitulatif</h2>
      <div style="display: flex; flex-direction: column; gap: 30px; margin-bottom: 20px; padding: 0 20px;">
        <div style="display: inline-flex; gap: 21px; justify-content: space-between;">
          <div style="font-size: 1.2rem;">Sous-total</div>
          <div style="font-size: 1.2rem; font-weight: bold;">{{ computeSubtotal().toFixed(2).replace('.', ',') }} €</div>
        </div>
        <div style="display: inline-flex; gap: 21px; justify-content: space-between;">
          <div style="font-size: 1.2rem;">Frais de livraison</div>
          <div style="font-size: 1.2rem; font-weight: bold;">Gratuit</div>
        </div>
        <div style="display: inline-flex; gap: 21px; justify-content: space-between;">
          <div style="font-size: 1.2rem;">Total</div>
          <div style="font-size: 1.2rem; font-weight: bold;">{{ computeSubtotal().toFixed(2).replace('.', ',') }} €</div>
        </div>
        <button id="validate-cart" >Valider mon panier</button>
        </div>
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
  margin-top: 5px;
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
  border: none;
  color: black;
  padding: 15px;
  border-radius: 10px;
  margin-left: 90%;
}

button {
  padding: 15px;
  background: black;
  color: white;
  border-radius: 10px;
  font-size: 1.1rem;
  cursor: pointer;
}
</style>