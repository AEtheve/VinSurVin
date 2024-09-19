<script setup lang="ts">
import { ref, onMounted, watch, inject } from 'vue';
import ProductBox from './ProductBox.vue';
import LowerPage from './LowerPage.vue';

const products = ref(inject('productlist'));

const showFilterMenu = ref(false);
const rangemax = ref(20000);
const minPrice = ref(0);
const maxPrice = ref(20000);
const currentPage = inject("currentPage");
const totalPages = inject("totalPages");
const filterSearch = inject("filterSearch");
const type = ref('');
const region = ref('');
const appellation = ref('');
const millesime = ref('');
const grape_variety = ref('');
let isActive = false


function activeFilters(){
  isActive = true
  fetchProduct();
}

function disabledFilters(){
  isActive = false
  fetchProduct();
}

function applyFilters() {
  const filters = {
    type: type.value,
    region: region.value,
    appellation: appellation.value,
    millesime: millesime.value,
    grape_variety: grape_variety.value,
    min_price: minPrice.value,
    max_price: maxPrice.value,
  };
  let response = `//${window.location.hostname}:8000/product/search/?`;
  for (const [key, value] of Object.entries(filters)) {
    if (value) {
      response += `${key}=${value}&`;
    }
  }
  return response; 
}




const fetchProduct = async (page = 1) => {
  window.scrollTo(0, 0);
  let data = [];
  let response: Response;
  if (filterSearch.value && isActive===true) {
    const result = applyFilters()+`&name=${filterSearch.value}&page=${page}`;
    response = await fetch(result);
  }
  else if (filterSearch.value) {
    response = await fetch(`//${window.location.hostname}:8000/product/search/?name=${filterSearch.value}&page=${page}`);
  } else if (isActive===true) {
    const result = applyFilters()+`&page=${page}`;
    response = await fetch(result);
  }
  else {
    response = await fetch(`//${window.location.hostname}:8000/product/?page=${page}`);
  }
  const dataJSON = await response.json();
  data = dataJSON.products;
  currentPage.value = dataJSON.current_page;
  totalPages.value = dataJSON.total_pages;


  products.value = data.map((productData) => {
    const product = productData.fields;
    const id = productData;

    return {
      pk: id.pk,
      name: product.name,
      price: product.price,
      promo: product.promo,
      image: product.image,
      grape_variety: product.grape_variety,
      region: product.region,
      millesime: product.millesime,
      appellation: product.appellation,
      type: product.type,
      Stock: product.stock,
    };
  });
}

onMounted(() => {
  fetchProduct();
});

watch(filterSearch, () => {
  fetchProduct();
});

function changePage(increment: number) {
  const newPage = currentPage.value + increment;
  if (newPage >= 1 && newPage <= totalPages.value) {
    fetchProduct(newPage);
  }
}

watch(minPrice, (newMinPrice) => {
  if (newMinPrice >= maxPrice.value) {
    minPrice.value = maxPrice.value;
  }
  if (newMinPrice == rangemax.value) {
    minPrice.value = maxPrice.value;
  }
});

watch(maxPrice, (newMaxPrice) => {
  if (newMaxPrice <= minPrice.value) {
    maxPrice.value = minPrice.value;
  }
});

function closeFilterMenu() {
  showFilterMenu.value = false;
}

function openFilterMenu() {
  showFilterMenu.value = true;
}
</script>


<template>
  <dialog v-if="showFilterMenu" @click.self="closeFilterMenu" ref="filterDialog">
    <div id="filter-menu">
      <div id="close_filter" @click="closeFilterMenu">
        <i class="fa-solid fa-times"></i>
      </div>
      <div class="filter-content">
        <div>
          <label for="min-price">Prix Min</label>
          <input type="range" id="min-price" name="min-price" min="0" max="20000" step="100" v-model="minPrice">
          <span class="price-display">{{ minPrice }}€</span>
        </div>
        <div>
          <label for="max-price">Prix Max</label>
          <input type="range" id="max-price" name="max-price" min="0" max="20000" step="100" v-model="maxPrice">
          <span class="price-display">{{ maxPrice }}€</span>
        </div>

        <div>
          <label for="type">Type</label>
          <select name="type" id="type" v-model="type">
            <option value=""></option>
            <option value="rouge">Rouge</option>
            <option value="blanc">Blanc</option>
            <option value="rosé">Rosé</option>
          </select>
        </div>

        <div>
          <label for="region">Région</label>
          <select name="region" id="region" v-model="region">
            <option value=""></option>
            <option value="bordeaux">Bordeaux</option>
            <option value="bourgogne">Bourgogne</option>
            <option value="alsace">Alsace</option>
            <option value="champagne">Champagne</option>
          </select>
        </div>

        <div>
          <label for="appellation">Appellation</label>
          <select name="appellation" id="appellation" v-model="appellation">
            <option value=""></option>
            <option value="médoc">Médoc</option>
            <option value="saint-émilion">Saint-Émilion</option>
            <option value="pomerol">Pomerol</option>
            <option value="chablis">Chablis</option>
          </select>
        </div>

        <div>
          <label for="millesime">Millésime</label>
          <select name="millesime" id="millesime" v-model="appellation">
            <option value=""></option>
            <option value="2023">2023</option>
            <option value="2022">2022</option>
            <option value="2021">2021</option>
            <option value="2020">2020</option>
            <option value="2019">2019</option>
            <option value="2018">2018</option>
            <option value="2017">2017</option>
            <option value="2016">2016</option>
          </select>
        </div>
        <div>
          <label for="grape_variety">Cépage</label>
          <select name="grape_variety" id="grape_variety" v-model="grape_variety">
            <option value=""></option>
            <option value="cabernet-sauvignon">Cabernet Sauvignon</option>
            <option value="merlot">Merlot</option>
            <option value="syrah">Syrah</option>
            <option value="chardonnay">Chardonnay</option>
          </select>
        </div>
      </div>
      <div class = "valid-action-filters">
        <button class="apply-filters-button" @click="activeFilters" @click.self="closeFilterMenu">Appliquer filtres</button>
        <button class="apply-filters-button" @click="disabledFilters" @click.self="closeFilterMenu">Supprimer les filtres</button>
      </div>
    </div>
  </dialog>

  <div style="display:inline-flex; flex-direction: column; align-items: flex-start; margin: 10px; width: 95%;">
    <div style="width: 95%; display: flex; justify-content: flex-end; position: sticky; z-index: 1001; top: 12%;">
    <button class="filter-button" @click="openFilterMenu">
      <i class="fa-solid fa-sliders"></i>Trier et filtrer
    </button></div>
    <div style="display: inline-flex; gap: 25px; flex-wrap: wrap; row-gap: 100px; justify-content: center;">
      <ProductBox v-for="product in products" :key="product.pk" :product="product" />
    </div>
    <div class="pagination-controls" style="text-align: center; margin-top: 120px; z-index: 0; width: 100%;">
      <button @click="changePage(-1)" :disabled="currentPage === 1">Précédent</button>
      <span>Page {{ currentPage }} / {{ totalPages }}</span>
      <button @click="changePage(1)" :disabled="currentPage === totalPages">Suivant</button>
    </div>
    <LowerPage />

  </div>
</template>

<style scoped>

.apply-filters-button {
  padding: 15px;
  margin: 20px;
  background: black;
  color: white;
  border-radius: 10px;
  font-size: 1.1rem;
  cursor: pointer;
}

.apply-filters-button:hover {
  background: white;
  color: black;
  border: 2px solid black;
}

.filter-button {
  cursor: pointer;
  background: #e9e9e9;
  border: none;
  color: black;
  padding: 15px;
  border-radius: 10px;
  width: fit-content;
}

dialog {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
}

#filter-menu {
  background: white;
  padding: 20px;
  border-radius: 10px;
  width: 500px;
  max-width: 80%;
  max-height: 80%;
}

#close_filter {
  cursor: pointer;
  text-align: right;
}

.filter-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.filter-content div {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 70%;
}

.filter-content label {
  font-weight: bold;
  min-width: 60px;
  flex: 0.5;
  margin-right: 50px;
}

.filter-content select,
.filter-content input[type="range"] {
  width: 50%;
  border: 1px solid #ccc;
  border-radius: 5px;
  flex-grow: 1;
  margin-right: 10px;
}

.price-display {
  min-width: 60px;
  text-align: right;
}

button {
  padding: 10px;
  margin: 10px;
  background: black;
  color: white;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

button:hover {
  background: white;
  color: black;
  border: 2px solid black;
}

.pagination-controls button:disabled {
  background: #e0e0e0;
  color: #b0b0b0;
  cursor: not-allowed;
}
</style>
