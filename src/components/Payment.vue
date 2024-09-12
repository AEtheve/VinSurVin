<script setup lang="ts">
import { inject, ref } from 'vue';

// Injecter la fonction `computeSubtotal` correctement
const total = inject('computeSubtotal');

if (!total) {
  console.error("La fonction 'computeSubtotal' n'a pas été injectée correctement.");
}

// Variables pour stocker les données du formulaire
const cardNumber = ref('');
const expiryDate = ref('');
const cvv = ref('');
const name = ref('');
const billingAddress = ref('');

// Variables pour les messages d'erreur et succès
const errorMessage = ref('');
const successMessage = ref('');

const handleSubmit = () => {
    errorMessage.value = '';
    successMessage.value = '';

    if (!cardNumber.value || !expiryDate.value || !cvv.value || !name.value || !billingAddress.value) {
        errorMessage.value = 'Tous les champs sont obligatoires.';
        return;
    }

    if (cardNumber.value.replace(/\s+/g, '').length !== 16) {
        errorMessage.value = 'Le numéro de carte doit comporter 16 chiffres.';
        return;
    }

    if (!/^\d{2}\/\d{2}$/.test(expiryDate.value)) {
        errorMessage.value = 'Le format de la date d\'expiration est invalide.';
        return;
    }

    if (cvv.value.length !== 3) {
        errorMessage.value = 'Le CVV doit comporter 3 chiffres.';
        return;
    }

    setTimeout(() => {
        successMessage.value = 'Le paiement a été effectué avec succès.';
    }, 1000);
};
</script>

<template>
    <div class="payment-container">
        <h2>Paiement sécurisé</h2>

        <form @submit.prevent="handleSubmit">
            <div class="form-group">
                <label for="cardNumber">Numéro de carte</label>
                <input type="text" id="cardNumber" v-model="cardNumber" placeholder="1234 5678 9012 3456" maxlength="19" required />
            </div>

            <div class="form-group">
                <label for="expiryDate">Date d'expiration</label>
                <input type="text" id="expiryDate" v-model="expiryDate" placeholder="MM/AA" maxlength="5" required />
            </div>

            <div class="form-group">
                <label for="cvv">CVV</label>
                <input type="text" id="cvv" v-model="cvv" placeholder="123" maxlength="3" required />
            </div>

            <div class="form-group">
                <label for="name">Nom sur la carte</label>
                <input type="text" id="name" v-model="name" placeholder="Nom du titulaire" required />
            </div>

            <div class="form-group">
                <label for="billingAddress">Adresse de facturation</label>
                <input type="text" id="billingAddress" v-model="billingAddress" placeholder="123 Rue Principale" required />
            </div>

            <!-- Bouton de paiement affichant le total -->
            <button type="submit">Payer {{ total ? total().toFixed(2).replace('.', ',') : '0,00' }} €</button>

            <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
            <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
        </form>
    </div>
</template>


<style scoped>
.payment-container {
    max-width: 400px;
    margin: 0 auto;
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

.form-group {
    margin-bottom: 15px;
}

label {
    display: block;
    font-weight: bold;
    margin-bottom: 5px;
}

input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
}

button {
    width: 100%;
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

.error-message {
    color: red;
    margin-top: 10px;
}

.success-message {
    color: green;
    margin-top: 10px;
}
</style>