<script setup lang="ts">
import { ref, computed, inject } from 'vue';
import router from '../Router';

interface ProductItem {
	pk: number;
	name: string;
	price: number;
	promo: number;
	image: string;
	description: string;
	quantity: number;
}

const isMobileMenuOpen = ref(false);

const cartOpen = inject('cartOpen');
const productsInCard = inject('productsInCard');
const productlist = inject('productlist');

const isSearchActive = ref(false);

const isConnected = document.cookie.includes("csrftoken");

async function handleEnterPress() {
  const filtre = document.getElementById("input-search");
  const searchTerm = filtre.value;
  try {
    const response = await fetch(`http://localhost:8000/product/search/?name=${searchTerm}`);
    const data = await response.json();
	productlist.value = data.products;
	router.push('/boutique');
  } catch (error) {
    console.error('Erreur lors de la recherche:', error);
  }
}


function focusSearch() {
	const inputSearch = document.getElementById("input-search");
	const btnSearch = document.getElementById("btn-search");

	if (inputSearch) {
		isSearchActive.value = true;
		inputSearch.style.display = 'block';
		inputSearch.focus();
		btnSearch.style.display = 'none';

		inputSearch.addEventListener('blur', () => {
			isSearchActive.value = false;
			btnSearch.style.display = 'inline-block';
		});
	}
}

const totalQuantity = computed(() => {
	return productsInCard.value.reduce((total, item) => total + item.quantity, 0);
});


function toggleMobileMenu() {
	isMobileMenuOpen.value = !isMobileMenuOpen.value;
}
</script>


<template>
	<div id="promo-border">Profitez de réductions exceptionnelles sur nos vins!</div>
	<ul class="ul-header-mobile">
		<router-link to="/">
			<div
				style="background-image: url('https://vinsurvin-bucket.s3.eu-west-3.amazonaws.com/logo.png'); width: 171px; height: 81px; background-size: cover; background-position: center; background-repeat: no-repeat; cursor: pointer; position: relative; left:0; margin-left: 15px; background-size: 110px;">
			</div>
		</router-link>
		<span @click="toggleMobileMenu" style="margin: 20px;"><i class="fa-solid fa-bars"></i></span>
	</ul>
	<dialog v-if="isMobileMenuOpen" class="mobile-menu-dialog">
		<div class="mobile-menu-content">
			<div class="close-menu" @click="toggleMobileMenu" id="closeMenuMobile">
				<i class="fa-solid fa-times"></i>
			</div>
			<ul class="mobile-menu-list">
				<li>
					<router-link to="/" @click="toggleMobileMenu">Accueil</router-link>
				</li>
				<li>
					<router-link to="/boutique" @click="toggleMobileMenu">Boutique</router-link>
				</li>
				<li>
					<router-link to="/account" @click="toggleMobileMenu">Se connecter / S'inscrire</router-link>
				</li>
				<li @click="cartOpen = true; toggleMobileMenu()">
					Panier ({{ totalQuantity }})
				</li>
			</ul>
		</div>
	</dialog>
	<ul class="ul-header">
		<router-link to="/">
			<div
				style="background-image: url('https://vinsurvin-bucket.s3.eu-west-3.amazonaws.com/logo.png'); width: 171px; height: 81px; background-size: cover; background-position: center; background-repeat: no-repeat; cursor: pointer; position: relative; left:0; margin-left: 15px; background-size: 110px;">
			</div>
		</router-link>

		<div style="
	          display: inline-flex;
	    gap: 2.5rem;
	    position: absolute;
	    right: 92px;">
			<li>
				<router-link to="/" :class="{ active: $route.path === '/' }">Accueil</router-link>
			</li>
			<li>
				<router-link to="/boutique" :class="{ active: $route.path === '/boutique' }">Boutique</router-link>
			</li>
			<li @click="focusSearch" @keyup.enter="handleEnterPress" class="search-container">
				<span id="btn-search">Rechercher</span>
				<input type="text" id="input-search" />
				<svg v-if="isSearchActive" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"
					class="search-icon">
					<g clip-path="url(#clip0_15_152)">
						<rect width="24" height="24" fill="white"></rect>
						<circle cx="10.5" cy="10.5" r="6.5" fill="white" stroke="#000000" stroke-linejoin="round"></circle>
						<path
							d="M19.6464 20.3536C19.8417 20.5488 20.1583 20.5488 20.3536 20.3536C20.5488 20.1583 20.5488 19.8417 20.3536 19.6464L19.6464 20.3536ZM20.3536 19.6464L15.3536 14.6464L14.6464 15.3536L19.6464 20.3536L20.3536 19.6464Z"
							fill="#000000"></path>
					</g>
					<defs>
						<clipPath id="clip0_15_152">
							<rect width="24" height="24" fill="white"></rect>
						</clipPath>
					</defs>
				</svg>
			</li>
			<li>
				<router-link v-if="isConnected" to="/account"
					:class="{ active: $route.path === '/account' }">Compte</router-link>
				<router-link v-else to="/account" :class="{ active: $route.path === '/account' }">Se connecter /
					S'inscrire</router-link>
			</li>
			<li>
				<div @click="cartOpen = true" style="
    display: inline-flex;
    align-items: center;
	gap:3px
">
					<svg width="19" height="24" viewBox="0 0 19 24" fill="none" xmlns="http://www.w3.org/2000/svg"
						class="block-header-cart__icon" data-v-12eef732="">
						<path fill-rule="evenodd" clip-rule="evenodd" d="M5.94636 5.35922C6.29451 3.00506 7.9363 1.39824 9.67973
							1.39824C11.4232 1.39824 13.0649 3.00506
							13.4131 5.35922H5.94636ZM4.53847 5.35922C4.90317 2.43147
							6.95866 0.000183105 9.67973 0.000183105C12.4008
							0.000183105 14.4563 2.43147 14.821 5.35922H17.2816H18.6797V6.75728V21.2039C18.6797
							22.7481 17.4278 24 15.8836
							24H3.4758C1.93155 24 0.679688 22.7481 0.679688
							21.2039V6.75728V5.35922H2.07775H4.53847ZM2.07775 6.75728H4.52596V9.08752C4.52596
							9.47359 4.83893 9.78655 5.22499 9.78655C5.61105 9.78655 5.92402 9.47359
							5.92402 9.08752V6.75728H13.5259V9.08752C13.5259 9.47359
							13.8389 9.78655 14.2249 9.78655C14.611 9.78655 14.9239
							9.47359 14.9239 9.08752V6.75728H17.2816V21.2039C17.2816 21.976 16.6557 22.6019
							15.8836 22.6019H3.4758C2.70368 22.6019 2.07775 21.976 2.07775 21.2039V6.75728Z" fill="currentColor"
							data-v-12eef732=""></path>
					</svg> ({{ totalQuantity }})
				</div>
			</li>
		</div>
	</ul>
</template>

<style scoped>
ul {
	display: flex;
	align-items: center;
	gap: 20px;
	list-style-type: none;
	padding: 0;
	color: black;
	top: 0;
	right: 0;
	margin-right: 150px;
	font-size: 1rem;
	margin-top: 50px;
	user-select: none;
}

li {
	height: 20px;
	cursor: pointer;
	position: relative;
}

li:hover {
	text-decoration: underline;
	text-underline-offset: 0.5em;
}

.active {
	text-decoration: underline;
	text-underline-offset: 0.5em;
}


#promo-border {
	height: 40px;
	width: 100%;
	background: #2c2c2c;
	position: absolute;
	top: 0;
	color: white;
	display: inline-flex;
	align-items: center;
	justify-content: center;
	text-transform: uppercase;
}

#input-search {
	height: 0;
	width: 0;
	border-style: none;
	padding: 10px;
	font-size: 18px;
	letter-spacing: 2px;
	outline: none;
	border-radius: 25px;
	transition: all .5s ease-in-out;
	display: none;
}

#input-search:focus {
	width: 300px;
	border-radius: 0px;
	background-color: transparent;
	transition: all 500ms cubic-bezier(0, 0.110, 0.35, 2);
}

.search-container {
	position: relative;
}

.search-icon {
	position: absolute;
	right: 10px;
	top: 50%;
	transform: translateY(-50%);
	width: 24px;
	height: 24px;
	fill: black;
}

.ul-header {
	position: sticky;
	z-index: 1000;
	background: white;
	width: 100%;
}

.ul-header-mobile {
	display: none;
	position: sticky;
	z-index: 1000;
	background: white;
	width: 100%;
	font-size: 2rem;
}

.mobile-menu-dialog {
	position: fixed;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	background: rgba(0, 0, 0, 0.8);
	display: flex;
	justify-content: flex-end;
	padding: 0;
	z-index: 1001;
}

.mobile-menu-content {
	background: white;
	height: 100%;
	width: 70%;
	display: inline-flex;
	flex-direction: column;
}

.mobile-menu-list {
	display: flex;
	flex-direction: column;
	font-size: 1.1rem;
	margin: auto;
	height: 100%;
	margin-top: 20px;
}

#closeMenuMobile {
	cursor: pointer;
	margin: 20px;
	text-align: right;
}

@media (max-width: 1091px) {
	.ul-header {
		display: none;
	}

	.ul-header-mobile {
		display: flex;
		justify-content: space-between;
		margin-bottom: 10px;
	}
}
</style>
