<script setup lang="ts">
import { ref, inject, provide } from 'vue';
import { onMounted } from 'vue';
import Payment from './Payment.vue';
import LowerPage from './LowerPage.vue';

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
  step.value = 2;
}
const nom = ref('');
const address = ref('');
const city = ref('');
function isFormDeliveryValid() {
  return (
    nom.value &&
    address.value &&
    city.value
  );
}

provide('isFormDeliveryValid', isFormDeliveryValid);
provide('submitDeliveryForm', submitDeliveryForm);
</script>

<template>
  <div style="padding-left: 3%; display: flex; gap: 0px; height: 80vh; justify-content: space-evenly">
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
      <form @submit.prevent="submitDeliveryForm">
        <div class="form-group">
          <label for="name" class="form-label">Nom :</label>
          <input type="text" id="name" v-model="nom" placeholder="Votre nom" required class="form-input" />
        </div>
        <div class="form-group">
          <label for="address" class="form-label">Adresse :</label>
          <input type="text" id="address" v-model="address" placeholder="Votre adresse" required class="form-input" />
        </div>
        <div class="form-group">
          <label for="city" class="form-label">Ville :</label>
          <input type="text" id="city" v-model="city" placeholder="Votre ville" required class="form-input" />
        </div>
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
      <h2>Récapitulatif :</h2>
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

.delivery-form {
  background: #f9f9f9;
  border-radius: 10px;
  padding: 60px;
  padding-top: 1;
  flex: 1;
  width: 35%;
  height: 80%;
  margin: 0 auto;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}


.form-container {
  display: flex;
  justify-content: space-between;
  gap: 84px; 
  margin: 20px 0;
  flex-wrap: nowrap;
}


.delivery-form, .payment-form {
  flex: 1; 
  padding: 60px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
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