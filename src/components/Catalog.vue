<script setup lang="ts">
</script>

<template>
  <div  style="padding-left: 3%;">
    <button class="filter-button"><i class="fa-solid fa-sliders"></i>Trier et filtrer</button>
    <div  style="display: inline-flex; gap: 25px;">
      <div>
        <div id="product-box">
          <div class="product_card"></div>
          <div style="display: inline-flex; flex-direction: column; text-align: center;">
            <span style="font-weight: 600; font-size: 1.2rem;">Vins exquis de la région</span>
            <div class="product-price">20,00€
              <div><button>Ajouter au panier</button></div>
            </div>
          </div>
        </div>
      </div>
      <div>
        <div id="product-box">
          <div class="product_card"></div>
          <div style="display: inline-flex; flex-direction: column; text-align: center;">
            <span style="font-weight: 600; font-size: 1.2rem;">Vins exquis de la région</span>
            <div class="product-price"><span class="promo">20,00€</span> <span class="promo-pourcent">-5%</span></div>
            <div class="promo-price">19,00€</div>
            <div><button>Ajouter au panier</button></div>

          </div>
        </div>
      </div>
      <div>
        <div id="product-box">
          <div class="product_card"></div>
          <div style="display: inline-flex; flex-direction: column; text-align: center;">
            <span style="font-weight: 600; font-size: 1.2rem;">Vins exquis de la région</span>
            <div class="product-price">20,00€
              <div><button>Ajouter au panier</button></div>
            </div>
          </div>
        </div>
      </div>
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

.product_card {
  background-image: url('https://images.unsplash.com/photo-1464036388609-747537735eab?ixid=M3wzOTE5Mjl8MHwxfHNlYXJjaHw3fHx3aW5lJTIwY2F0ZWdvcmllc3xlbnwwfHx8fDE3MjU1NDYxNzF8MA&ixlib=rb-4.0.3&auto=format&fit=crop&w=576&h=720&q=100');
  background-size: cover;
  background-position: center;
  height: 360px;
  width: 240px;
  margin: 0px;
}

#product-box {
  display: inline-flex;
  flex-direction: column;
}

button {
  padding: 10px;
  margin: 10px;
  background: black;
  color: white;
  border-radius: 10px
}

.product-price {
  padding: 3px;
  font-weight: 600;
}

.promo {
  text-decoration: line-through;
  font-weight: 400;
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
