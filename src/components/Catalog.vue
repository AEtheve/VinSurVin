<script setup lang="ts">
import ProductBox from './ProductBox.vue'

const products = [
  {
    name: 'Vins Rouge',
    price: 20,
    promo: 10,
    image: 'https://media.discordapp.net/attachments/1281590451169787925/1281595657291042878/Leonardo_Phoenix_A_sleek_blacklabeled_red_wine_bottle_with_a_s_3.jpg?ex=66df9637&is=66de44b7&hm=e3ff18603a88c1a5cf34f31af2f989022fa6bd5e1ed19848af8eddfbfd7ee142&=&format=webp&width=1026&height=1026'
  },
  {
    name: 'Vins Blanc',
    price: 20,
    promo: -1,
    image: 'https://media.discordapp.net/attachments/1281590451169787925/1281596055175172116/Leonardo_Phoenix_A_refined_solitary_white_wine_bottle_stands_e_1.jpg?ex=66df9696&is=66de4516&hm=e8b9705fb61dbda012770c7f2fc9cd9168e2aa3f267c5520f9dd699e4592b4fb&=&format=webp&width=1026&height=1026'
  },
  {
    name: 'Vins Rosé',
    price: 30,
    promo: -1,
    image: 'https://media.discordapp.net/attachments/1281590451169787925/1281596638787538997/Leonardo_Phoenix_updatedpromptA_sleek_elongated_rose_wine_bott_1.jpg?ex=66df9721&is=66de45a1&hm=8ebaa62ac26aeaeff681cdae705614e823d044e50917d27a5d0adf4b9f9673b3&=&format=webp&width=1026&height=1026'
  },
  {
    name: 'Chanpagne',
    price: 40,
    promo: -1,
    image: 'https://media.discordapp.net/attachments/1281590451169787925/1281597398921248879/Leonardo_Phoenix_A_solitary_elegant_champagne_bottle_with_a_sl_0.jpg?ex=66df97d6&is=66de4656&hm=9cab54679935906e14b545a0781d0c2647b31d672c2c95b25f74bd4661a88867&=&format=webp&width=1026&height=1026'
  },
];

</script>

<template>
  <div  style="padding-left: 3%;">
    <button class="filter-button"><i class="fa-solid fa-sliders"></i>Trier et filtrer</button>
    <div  style="display: inline-flex; gap: 25px;">
      <!-- <div>
        <div id="product-box">
          <div class="product_card"></div>
          <div style="display: inline-flex; flex-direction: column; text-align: center;">
            <span style="font-weight: 600; font-size: 1.2rem;">Vins exquis de la région</span>
            <div class="product-price"><span class="promo">20,00€</span> <span class="promo-pourcent">-5%</span></div>
            <div class="promo-price">19,00€</div>
            <div><button>Ajouter au panier</button></div>

          </div>
        </div>
      </div> -->
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
