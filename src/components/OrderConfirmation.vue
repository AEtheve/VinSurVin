<script setup lang="ts">
import LowerPage from './LowerPage.vue';
</script>

<template>
    <div class="main-div">
        <h1> Merci pour votre commande</h1>
        <p class="text-center">Vous avez reçu un récapitulatif de votre commande sur <br>
        votre adresse personnelle</p>
    </div>
    <LowerPage></LowerPage>
</template>


<style scoped>
.text-center {
    text-align: center;
}
.main-div {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin-top: 100px;
}

</style>