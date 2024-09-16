<script setup lang="ts">
import { inject, ref } from 'vue';
import { useRoute } from 'vue-router';
import LowerPage from './LowerPage.vue';
</script>
<template>
  <div class="top">
    <h1 class="text-center">Conditions Générales de Vente</h1>
    
    <div>
      <h2>1. Préambule</h2>
      <p>Les présentes Conditions Générales de Vente (CGV) régissent les ventes de vins réalisées sur notre site fictif de vin pour l'école.</p>
    </div>

    <div>
      <h2>2. Objet</h2>
      <p>Les présentes conditions régissent les ventes de vins effectuées sur notre site. Elles précisent les droits et obligations des parties, à savoir le vendeur (notre site fictif) et l'acheteur (vous, l'utilisateur).</p>
    </div>

    <div>
      <h2>3. Produits</h2>
      <p>Les produits proposés à la vente sont des bouteilles de vin fictives. Les descriptions des vins sont fournies à titre indicatif et n'ont pas de valeur contractuelle.</p>
    </div>

    <div>
      <h2>4. Prix</h2>
      <p>Les prix indiqués sur le site sont fictifs et ne représentent pas une transaction réelle. Aucune somme ne sera perçue.</p>
    </div>

    <div>
      <h2>5. Commande</h2>
      <p>Les commandes s'effectuent via notre plateforme en ligne. Étant donné le caractère fictif du site, aucune commande réelle ne sera traitée.</p>
    </div>

    <div>
      <h2>6. Livraison</h2>
      <p>Aucune livraison réelle ne sera effectuée étant donné que le site et les produits sont fictifs.</p>
    </div>

    <div>
      <h2>7. Rétractation</h2>
      <p>Conformément à la réglementation fictive en vigueur, vous avez un droit de rétractation de 14 jours après votre commande fictive. Cependant, aucune transaction réelle n'aura lieu.</p>
    </div>

    <div>
      <h2>8. Responsabilité</h2>
      <p>Le site fictif décline toute responsabilité concernant les produits proposés, étant donné que tout est fictif et uniquement dans le cadre d'un projet scolaire.</p>
    </div>

    <div>
      <h2>9. Données personnelles</h2>
      <p>Aucune donnée personnelle réelle n'est collectée.</p>
    </div>

    <div>
      <h2>10. Droit applicable</h2>
      <p>Ces conditions sont soumises à un droit fictif adapté à un cadre scolaire. Elles ne sont pas juridiquement contraignantes.</p>
    </div>
  </div>
  <LowerPage></LowerPage>
</template>


<style scoped>

.top {
    margin: 0 auto;
    width: 80%;
    padding: 20px;
    font-size: 1.2rem;
    line-height: 1.5;
    text-align: justify;
}
.text-center {
    text-align: center;
}
</style>