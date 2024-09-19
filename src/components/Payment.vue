<script setup lang="ts">
import { inject, ref, computed, watch } from 'vue';
import router from '../Router';

const clearCart = inject('clearCart');

const city = inject('city');
const address = inject('address');
const codepostale = inject('codepostale');
const email = inject('email');

const isConnected = inject('isConnected');
const isPaymentFormValid = inject('isPaymentFormValid');
const processPayment = inject('processPayment');

const cardNumber = ref('');
const expiryDate = ref('');
const cvv = ref('');
const name = ref('');

const cardNumberError = ref('');
const expiryDateError = ref('');
const cvvError = ref('');
const nameError = ref('');
const generalErrorMessage = ref('');
const successMessage = ref('');
const showLoading = ref(false);


watch(processPayment, () => {
  createOrder();
});

function getCurrentYear() {
  return new Date().getFullYear() % 100;
}

function validateCardNumber() {
  if (cardNumber.value.replace(/\s+/g, '').length !== 16) {
    cardNumberError.value = 'Le numéro de carte doit comporter 16 chiffres.';
  } else {
    cardNumberError.value = '';
  }
}

function validateExpiryDate() {
  const [month, year] = expiryDate.value.split('/').map(Number);
  const currentYear = getCurrentYear();

  if (!month || month < 1 || month > 12) {
    expiryDateError.value = "Le mois d'expiration doit être entre 01 et 12.";
  } else if (!year || year < currentYear) {
    expiryDateError.value = `L'année d'expiration doit être supérieure ou égale à ${currentYear}.`;
  } else {
    expiryDateError.value = '';
  }
}

function validateCVV() {
  if (!/^\d+$/.test(cvv.value)) {
    cvvError.value = 'Le CVV doit être un nombre à 3 chiffres.';
  } else if (cvv.value.length !== 3) {
    cvvError.value = 'Le CVV doit comporter 3 chiffres.';
  } else {
    cvvError.value = '';
  }
}

function validateName() {
  if (!name.value) {
    nameError.value = 'Le nom sur la carte est obligatoire.';
  } else {
    nameError.value = '';
  }
}

const isFormValid = computed(() => {
  return (
    !cardNumberError.value &&
    !expiryDateError.value &&
    !cvvError.value &&
    !nameError.value &&
    cardNumber.value.replace(/\s+/g, '').length === 16 &&
    /^\d{2}\/\d{2}$/.test(expiryDate.value) &&
    cvv.value.length === 3 &&
    name.value
  );
});

watch(isFormValid, (newValue) => {
  if (newValue) {
    isPaymentFormValid.value = true;
  }
});

function formatCardNumber(event: Event) {
  const input = event.target as HTMLInputElement;
  let value = input.value.replace(/\D/g, '');
  value = value.replace(/(.{4})/g, '$1 ').trim();
  input.value = value;
  cardNumber.value = input.value;
}

function formatCVV(event: Event) {
  const input = event.target as HTMLInputElement;
  input.value = input.value.replace(/\D/g, '');
  cvv.value = input.value;
}

function createOrder() {
  if (isConnected.value == true) {
    fetch(`//${window.location.hostname}:8000/create-order/`, {
      method: 'POST',
      credentials: 'include',
      mode: 'cors',
      body: JSON.stringify({
        street: address.value,
        city: city.value,
        zip_code: codepostale.value,
      }),
    }).then(() => {
      handleSubmit();
    });
  }
  else {
    fetch(`//${window.location.hostname}:8000/create-order/`, {
      method: 'POST',
      credentials: 'include',
      mode: 'cors',
      body: JSON.stringify({
        street: address.value,
        city: city.value,
        zip_code: codepostale.value,
        email: email.value
      }),
    }).then(() => {
      handleSubmit();
    });
  }
  
}

function formatExpiryDate(event: Event) {
  const input = event.target as HTMLInputElement;
  let value = input.value.replace(/[^\d]/g, '');

  if (value.length > 2) {
    value = value.slice(0, 2) + '/' + value.slice(2, 4);
  }

  expiryDate.value = value;
  input.value = value;
}


const handleSubmit = () => {
  // generalErrorMessage.value = '';
  // successMessage.value = '';

  // validateCardNumber();
  // validateExpiryDate();
  // validateCVV();
  // validateName();

  // if (!isFormValid.value) {
  //   generalErrorMessage.value = 'Tous les champs doivent être correctement remplis.';
  //   return;
  // }

  showLoading.value = true;

  setTimeout(() => {
    showLoading.value = false;
    successMessage.value = 'Paiement effectué avec succès !';
    clearCart();

    setTimeout(() => {
      router.push('/confirmation');
    }, 1000); 
  }, 2000); 
};


</script>


<template>
  <div v-if="showLoading" class="loading-overlay">
    <img src="https://vinsurvin-bucket.s3.eu-west-3.amazonaws.com/gif2.gif" alt="Loading..." class="loading-spinner" />
  </div>
  <div class="payment-container">
    <h2 class="form-title">2. Paiement sécurisé</h2>

    <form>
      <div class="form-group">
        <label class="form-label" for="cardNumber">Numéro de carte *:</label>
        <input type="text" id="cardNumber" v-model="cardNumber" placeholder="1234 5678 9012 3456" maxlength="19" required
          @input="formatCardNumber" @blur="validateCardNumber" inputmode="numeric" />
        <div v-if="cardNumberError" class="error-message">{{ cardNumberError }}</div>
      </div>

      <div class="form-group">
        <label class="form-label" for="expiryDate">Date d'expiration *:</label>
        <input type="text" id="expiryDate" v-model="expiryDate" placeholder="MM/AA" maxlength="5" required
          @input="formatExpiryDate" @blur="validateExpiryDate" />
        <div v-if="expiryDateError" class="error-message">{{ expiryDateError }}</div>
      </div>

      <div class="form-group">
        <label class="form-label" for="cvv">CVV *:</label>
        <input type="text" id="cvv" v-model="cvv" placeholder="123" maxlength="3" required @input="formatCVV"
          @blur="validateCVV" inputmode="numeric" />
        <div v-if="cvvError" class="error-message">{{ cvvError }}</div>
      </div>

      <div class="form-group">
        <label class="form-label" for="name">Nom sur la carte *:</label>
        <input type="text" id="name" v-model="name" placeholder="Nom du titulaire" required @blur="validateName" />
        <div v-if="nameError" class="error-message">{{ nameError }}</div>
      </div>
    </form>
  </div>
</template>



<style scoped>
.payment-container {
  width: 100%;
  margin: 0 auto;
  flex: 1;
  padding: 60px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  padding-top: 0;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
}

.form-label {
  font-weight: bold;
  color: #666;
  margin-bottom: 5px;
  display: block;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

button {
  width: 110%;
  padding: 10px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.error-message {
  color: red;
  margin-top: 10px;
}

.success-message {
  color: green;
  margin-top: 10px;
}

.main-div {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-top: 100px;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.loading-spinner {
  width: 100px;
  height: 100px;
}
</style>
