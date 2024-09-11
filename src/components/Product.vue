@ -1,46 +0,0 @@
<script setup lang="ts">
import { defineProps } from 'vue';

defineProps<{
  product: {
    id: number;
    name: string;
    price: number;
    promo: number;
    image: string;
    description: string;

    cepage?: string;
    region?: string;
    millesime?: number;
    appellation?: string;
    type?: string;
  };
}>();


</script>

<template>
  <div  style="padding-left: 3%;">
  PAGE PRODUIT
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