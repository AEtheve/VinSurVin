<script setup lang="ts">
import ProductBox from './ProductBox.vue'

const products = [
  {
    id: 1,
    name: 'Vins Rouge',
    price: 20,
    promo: 10,
    description: 'Vin rouge de qualité, La cuvée La Germine du domaine Duclaux utilise les deux cépages de l\'appellation. Tout d\'abord la Syrah à 97%. Ce raisin aux petites baies d\'un noir légèrement bleuté est inscrit dans le patrimoine des Côtes du Rhône tellement il se plait dans la région. La Syrah permet la production de vins fruités et tanniques qui ravissent les papilles des amateurs de vins rouges. Le viognier vient compléter la Syrah pour attendrir ses tanins et confère au vin la finesse légendaire des vins de l\'AOC Côtes Rôties.',
    image: '/images/Rouge.jpg',
    cepage: 'Syrah, Viognier',
    region: 'Rhône',
    millesime: 2018,
    appellation: 'Côtes Rôties',
    type: 'Rouge'
  },
  {
    id: 2,
    name: 'Vins Blanc',
    price: 20,
    promo: -1,
    description: 'Vin blanc de qualité, produit à partir de raisins de Chardonnay soigneusement sélectionnés.',
    image: '/images/Blanc.jpg',
    cepage: 'Chardonnay',
    region: 'Bourgogne',
    millesime: 2020,
    appellation: 'Chablis',
    type: 'Blanc'
  },
  {
    id: 3,
    name: 'Vins Rosé',
    price: 30,
    promo: -1,
    description: 'Vin rosé de qualité, caractérisé par des arômes fruités et une fraîcheur exceptionnelle.',
    image: '/images/Rosé.jpg',
    cepage: 'Grenache, Cinsault',
    region: 'Provence',
    millesime: 2021,
    appellation: 'Côtes de Provence',
    type: 'Rosé'
  },
  {
    id: 4,
    name: 'Champagne',
    price: 40,
    promo: -1,
    description: 'Champagne de qualité, élaboré selon la méthode traditionnelle champenoise.',
    image: '/images/Champagne.jpg',
    cepage: 'Pinot Noir, Chardonnay, Pinot Meunier',
    region: 'Champagne',
    millesime: 2012,
    appellation: 'Champagne',
    type: 'Effervescent'
  },
];


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
