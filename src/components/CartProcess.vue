<script setup lang="ts">
import { ref, inject, provide } from 'vue';
import Payment from './Payment.vue';
import LowerPage from './LowerPage.vue';

const errorMessage = ref('');

const isConnected = document.cookie.includes("csrftoken");
provide('isConnected', isConnected);

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

const productsInCard = inject('productsInCard');

function computeSubtotal() {
  let subtotal = 0;
  productsInCard.value.forEach((product) => {
    subtotal += (product.price * (1 - product.promo / 100)) * product.quantity;
  });
  return subtotal;
}
provide('computeSubtotal', computeSubtotal);

const step = ref(0);

function validateCart() {
  step.value = 1;
}

function submitDeliveryForm() {
  if (isFormDeliveryValid()) {
    errorMessage.value = ''; // Si le formulaire est valide, on vide le message d'erreur
    step.value = 2;
  } else {
    errorMessage.value = 'Veuillez remplir tous les champs de livraison.';
  }
}


const nom = ref('');
const address = ref('');
const city = ref('');
const codepostale = ref('');
const email = ref('');

function formatCodePostale(event: Event) {
  const input = event.target as HTMLInputElement;
  let value = input.value.replace(/\D/g, '');
  if (value.length > 5) {
    value = value.slice(0, 5);
  }
  input.value = value;
  codepostale.value = value;
}


provide('address', address);
provide('city', city);
provide('codepostale', codepostale);
provide('email', email);

function isFormDeliveryValid() {
  return nom.value.trim() !== '' && address.value.trim() !== '' && city.value.trim() !== '';
}

provide('isFormDeliveryValid', isFormDeliveryValid);
provide('submitDeliveryForm', submitDeliveryForm);
</script>

<template>
  <div style="padding-left: 3%; display: flex; gap: 0px; height: 80vh; justify-content: space-evenly">
    <!-- Step 0: Résumé de la commande -->
    <div v-if="step === 0" style="flex: 0.7 auto; border: 1px solid black; margin: 10px; padding-left: 20px;">
      <h2 class="form-title">Panier</h2>
      <div style="display: inline-flex; flex-direction: column; gap: 20px; overflow-y: auto; max-height: 60vh; padding-right: 10px; width: 98%;">
        <div v-for="product in productsInCard" :key="product.id" style="display: inline-flex; gap: 21px;">
          <div data-v-0ec6eb9a="" class="product_card" style="width: 120px; height: 180px;" :style="{ backgroundImage: `url(${product.image})` }">
          </div>
          <div style="display: inline-flex; flex-direction: column; padding: 1px; gap: 8px;">
            <div style="font-weight: bold; font-size: 1.2rem;">{{ product.name }}</div>
            <div style="font-size: 1.2rem; display: inline-flex; gap: 60px;">
              <div>Quantité : {{product.quantity}}</div>
              <div>{{ (product.price * (1 - product.promo / 100)).toFixed(2).replace('.', ',') }} €</div>
            </div>
            <div style="font-size: 1.1rem; color: rgb(56 56 184); cursor:pointer;" @click="removeProductFromCart(product.pk, product.quantity)">Supprimer</div>
          </div>
        </div>
      </div>
    </div>

 <!-- Step 1: commande validé, formulaire de livraison et formulaire de paiement côte à côte -->
 <div v-if="step === 1" class="form-container">
    <div class="delivery-form">
      <h2 class="form-title">Formulaire de Livraison</h2>
      <p v-if="errorMessage" style="color: red;">{{ errorMessage }}</p>

      <form @submit.prevent="submitDeliveryForm">
        <div class="form-group">
          <label for="name" class="form-label">Nom *:</label>
          <input type="text" id="name" v-model="nom" placeholder="Votre nom" required class="form-input" />
        </div>
        <div class="form-group">
          <label for="address" class="form-label">Adresse *:</label>
          <input type="text" id="address" v-model="address" placeholder="Votre adresse" required class="form-input" />
        </div>
        <div class="form-group">
          <label for="city" class="form-label">Ville *:</label>
          <input type="text" id="city" v-model="city" placeholder="Votre ville" required class="form-input" />
        </div>
        <div class="form-group">
          <label for="codepostale" class="form-label">Code Postal *:</label>
          <input 
            type="text" 
            id="codepostale" 
            v-model="codepostale" 
            placeholder="Votre Code postal" 
            required 
            class="form-input" 
            @input="formatCodePostale" 
          />
        </div>
        <div v-if="!isConnected" class="form-group">
          <label for="email" class="form-label">Email *:</label>
          <input type="email" id="email" v-model="email" placeholder="Votre email" required class="form-input" @input="formatCodePostale" />
        </div>
        <div style="font-size: 0.8rem; color: #666; margin-top: 10px;">*Champ obligatoire</div>
      </form>
    </div>
      <Payment></Payment>
  </div>

     <!-- Step 2: récap de la commande validé  -->
     <div v-if="step === 2" style="flex: 0.7 auto; border: 1px solid black; margin: 10px; padding-left: 20px;">
      <h2>Récapitulatif de la Commande</h2>
      <p>Votre commande a été reçue. Merci pour votre achat!</p>
    </div>


    <div style="flex: 0.3 1 auto; border: 1px solid black; margin: 10px; padding-left: 20px;">
      <h2 class="form-title">Récapitulatif :</h2>
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
  <LowerPage></LowerPage>
</template>


<style scoped>


.form-container {
  display: flex;
  justify-content: space-between;
  gap: 84px; 
  margin: 20px 0;
  flex-wrap: nowrap;
}


.delivery-form, .payment-form {
  flex: 1; 
  padding: 0 50px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
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