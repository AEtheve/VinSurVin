<script setup lang="ts">
import LowerPage from './LowerPage.vue';
import { useRouter } from 'vue-router';

const router = useRouter();
</script>

<template>
    <div class="page-container">
        <div class="back-arrow">
            <router-link to="/boutique">
                <span>&larr; Retour à la boutique</span>
            </router-link>
        </div>
        <div class="main-div">
            <h1>Merci pour votre commande</h1>
            <p class="text-center">
                Vous avez reçu un récapitulatif de votre commande sur <br>
                votre adresse personnelle
            </p>
        </div>
        <LowerPage></LowerPage>
    </div>
</template>

<style scoped>
.page-container {
    position: relative;
    min-height: 100vh; 
}

.back-arrow {
    position: absolute;
    top: 20px;
    left: 20px;
    font-size: 1.2rem;
}

.back-arrow span {
    color: #333;
    text-decoration: none;
}

.back-arrow span:hover {
    text-decoration: underline;
}

.main-div {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: calc(100vh - 300px); 
    margin-top: 0;
}

.text-center {
    text-align: center;
}
</style>
