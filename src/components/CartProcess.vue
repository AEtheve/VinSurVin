<script setup lang="ts">
import { ref, inject } from 'vue';
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
const step = ref(0);

function formatCardNumber(event: Event) {
  const input = event.target as HTMLInputElement;
  input.value = input.value.replace(/[^\d ]/g, ''); 
}



function validateCart() {
  step.value = 1;
}

function submitDeliveryForm() {
  step.value = 2;
}
</script>

<template>
  <div style="padding-left: 3%; display: flex; gap: 20px; height: 80vh;">
    <!-- Step 0: Résumé de la commande -->
    <div v-if="step === 0" style="flex: 0.7 auto; border: 1px solid black; margin: 10px; padding-left: 20px;">
      <h2>Panier</h2>
      <div style="display: inline-flex; flex-direction: column; gap: 20px; overflow-y: auto; max-height: 60vh; padding-right: 10px; width: 98%;">
        <div v-for="product in productsInCard" :key="product.id" style="display: inline-flex; gap: 21px;">
          <div data-v-0ec6eb9a="" class="product_card" style="width: 120px; height: 180px;" :style="{ backgroundImage: `url(${product.image})` }">
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

<!-- Step 1: commande validé, formulaire de livraison-->
<div v-if="step === 1" class="delivery-form">
  <h2 class="form-title">Formulaire de Livraison</h2>
  <form @submit.prevent="submitDeliveryForm">
    <div class="form-group">
      <label for="name" class="form-label">Nom :</label>
      <input type="text" id="name" placeholder="Votre nom" required class="form-input" />
    </div>
    <div class="form-group">
      <label for="address" class="form-label">Adresse :</label>
      <input type="text" id="address" placeholder="Votre adresse" required class="form-input" />
    </div>
    <div class="form-group">
      <label for="city" class="form-label">Ville :</label>
      <input type="text" id="city" placeholder="Votre ville" required class="form-input" />
    </div>
    <div class="form-group">
  <label for="credit-card" class="form-label">Carte Bancaire :</label>
  <input 
    type="text" 
    id="credit-card" 
    placeholder="0000 0000 0000 0000" 
    maxlength="19" 
    required 
    class="form-input" 
    inputmode="numeric"
    @input="formatCardNumber"
  />
</div>
    <button type="submit" class="submit-button">Soumettre</button>
  </form>
</div>

     <!-- Step 2: récap de la commande validé  -->
     <div v-if="step === 2" style="flex: 0.7 auto; border: 1px solid black; margin: 10px; padding-left: 20px;">
      <h2>Récapitulatif de la Commande</h2>
      <p>Votre commande a été reçue. Merci pour votre achat!</p>
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
        <button v-if="step === 0" @click="validateCart">Valider mon panier</button>

      </div>
    </div>
  </div>
</template>


<style scoped>

.delivery-form {
  background: #f9f9f9;
  border-radius: 10px;
  padding: 30px;
  width: 35%;
  height: 80%;
  margin: 0 auto;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}

.form-title {
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
  text-align: center;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  font-weight: bold;
  color: #666;
  margin-bottom: 5px;
  display: block;
}

.form-input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
  color: #333;
}


.submit-button {
  padding: 15px;
  margin: 20px;
  background: black;
  color: white;
  border-radius: 10px;
  font-size: 1.1rem;
  cursor: pointer;
}

.submit-button:hover {
  background: white;
  color: black;
  border: 2px solid black;
}


#cart_content {
  position: fixed;
  top: 0;
  right: 0;
  background: white;
  padding: 20px;
  height: 100%;
  width: 98%;

  overflow-y: auto;
  max-height: 100vh;
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