<script setup lang="ts">
import { ref, onMounted, inject } from 'vue';
import LowerPage from './LowerPage.vue';

const registerFormMessage = ref("");
const registerFormError = ref("");
const loginFormMessage = ref("");
const loginFormError = ref("");
const isLoading = ref(false); 

const isConnected = inject('isConnected');

const accountInfo = ref({});
const orders = ref([]);

onMounted(() => {
  if (isConnected.value) {
    getInfos();
    getOrders();
  } else {
    document.getElementById("formRegister").addEventListener("submit", function (event) {
      event.preventDefault();

      fetch(`//${window.location.hostname}:8000/user/new`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: event.target.email.value,
          password: event.target.password.value,
          username: event.target.username.value
        })
      })
        .then(response => response.json())
        .then(data => {
          if (data.error == "Email already exists") {
            registerFormError.value = "Un compte existe déjà avec cette adresse email";
          } 
          if (data.error == "Username already exists") {
            registerFormError.value = "Un compte existe déjà avec ce nom d'utilisateur";
          }
          else {
            loginFormError.value = "";
            loginFormMessage.value = "";
            registerFormError.value = "";
            registerFormMessage.value = "Votre compte a bien été créé";
            fetch(`//${window.location.hostname}:8000/user/login`, {
                method: "POST",
                credentials: "include",
                mode: 'cors',
                body: JSON.stringify({
                  username: event.target.username.value,
                  password: event.target.password.value
                })
              })
                .then(response => response.json())
                .then(data => {
                  if (data.error) {
                    registerFormError.value = "Une erreur est survenue lors de la connexion";
                  } else {
                    localStorage.setItem('isConnected', 'true');
                    isLoading.value = true; 

                    setTimeout(() => {
                      location.href = "/boutique";
                    }, 1000); 
                  }
                })
            
          }
        })
    });

    document.getElementById("formLogin").addEventListener("submit", function (event) {
      event.preventDefault();

      fetch(`//${window.location.hostname}:8000/user/login`, {
        method: "POST",
        credentials: "include",
        mode: 'cors',

        body: JSON.stringify({
          username: event.target.username.value,
          password: event.target.password.value
        })
      })
        .then(response => response.json())
        .then(data => {
          if (data.error) {
            loginFormMessage.value = "";
            loginFormError.value = "Nom d'utilisateur ou mot de passe incorrect";
          } else {
            localStorage.setItem('isConnected', 'true');
            loginFormError.value = "";
            loginFormMessage.value = "Vous êtes connecté";
            isLoading.value = true; 

            setTimeout(() => {
              location.reload();
            }, 1000); 
          }
        })
    });
  }
});

function formatDate(date) {
  const d = new Date(date);
  return `${d.getDate()}/${d.getMonth() + 1}/${d.getFullYear()} ${d.getHours()}:${d.getMinutes()}`;
}

function getInfos() {
  fetch(`//${window.location.hostname}:8000/user/info`, {
    method: "GET",
    credentials: "include",
    mode: 'cors',
  })
    .then(response => response.json())
    .then(data => {
      accountInfo.value = {
        username: data.username,
        email: data.email,
        createdAt: formatDate(data.createdAt),
        lastLogin: formatDate(data.lastLogin),
      };
    })
}

function logout() {
  document.cookie = "csrftoken=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
  localStorage.removeItem('isConnected');
  location.reload();
}

async function getProductName(id:number) {
  const response = await fetch(`//${window.location.hostname}:8000/product/${id}`, {
    method: "GET",
    credentials: "include",
    mode: 'cors',
  });

  const data = await response.json();
  return data.fields.name;
}
async function getOrders() {
  try {
    const response = await fetch(`//${window.location.hostname}:8000/get-orders/`, {
      method: "GET",
      credentials: "include",
      mode: 'cors',
    });
    const data = await response.json();
    console.log(data);
    if (Array.isArray(data.orders)) {
      orders.value = await Promise.all(data.orders.map(async order => {
        const orderlines = await Promise.all(order.order_lines.map(async orderline => {
          const name = await getProductName(orderline.product_id);
          console.log("name", name);
          return {
            id: orderline.product_id,
            name,
            quantity: orderline.quantity,
            price: orderline.price,
          };
        }));
        return {
          id: order.id,
          date: formatDate(order.created_at),
          total: order.total_price,
          status: order.status === "in progress" ? "En cours" : "Terminée",
          address: {
            street: order.address.street,
            city: order.address.city,
            zip_code: order.address.zip_code,
          },
          orderlines,
        };
      }));
    } else {
      console.error('Aucune commande trouvée:', data);
    }
  } catch (error) {
    console.error('Erreur lors de la récupération des commandes:', error);
  }
}
</script>

<template>
  <div>
    <div v-if="isLoading" class="loading-overlay">
      <img src="/src/assets/gif2.gif" alt="Loading..." class="loading-spinner" />
    </div>
    
    <div v-if="!isConnected" id="account-forms">
      <div id="form_account" class="form-wrapper">
        <form id="formLogin" method="POST">
          <h2>Connectez-vous</h2>
          Vous avez déjà un compte sur VinSurVin ?
          <input type="text" name="username" placeholder="Adresse Mail" />
          <input type="password" name="password" placeholder="Mot de passe" />
          <input type="submit" value="Se connecter" />

          <p v-if="loginFormMessage != ''">{{ loginFormMessage }}</p>
          <p v-if="loginFormError != ''">{{ loginFormError }}</p>
        </form>

        <div class="divider"></div>

        <form id="formRegister" method="POST">
          <h2>Nouveau client ?</h2>
          <input type="text" name="email" placeholder="Adresse Mail" />
          <input type="text" name="username" placeholder="Nom d'utilisateur" />
          <input type="password" name="password" placeholder="Mot de passe" />
          <input type="submit" value="Poursuivre l'inscription" />

          <p v-if="registerFormMessage != ''">{{ registerFormMessage }}</p>
          <p v-if="registerFormError != ''">{{ registerFormError }}</p>
        </form>
      </div>

      <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;">
        <video src="https://vinsurvin-bucket.s3.eu-west-3.amazonaws.com/wine_video.mp4" autoplay loop muted
          style="width: 100%; height: 100%; object-fit: cover; opacity: 0.7; background-color: black;"
          playsinline></video>
      </div>

    </div>

    <div v-else class="account-wrapper">
      <div class="account-container">
        <h1 class="account-title">Mon compte</h1>
        <div class="account-info">
          <div class="account-info-row">
            <span class="account-info-label">Nom d'utilisateur:</span>
            <span class="account-info-value">{{ accountInfo.username }}</span>
          </div>
          <div class="account-info-row">
            <span class="account-info-label">Email:</span>
            <span class="account-info-value">{{ accountInfo.email }}</span>
          </div>
          <div class="account-info-row">
            <span class="account-info-label">Date de création:</span>
            <span class="account-info-value">{{ accountInfo.createdAt }}</span>
          </div>
          <div class="account-info-row">
            <span class="account-info-label">Dernière connexion:</span>
            <span class="account-info-value">{{ accountInfo.lastLogin }}</span>
          </div>
        </div>
        <div style="display: flex; justify-content: center;">
          <button @click="logout">Se déconnecter</button>
        </div>
      </div>
      <div class="account-histo">
        <h1 class="account-title">Historique de commandes</h1>
        <ul>
          <li v-for="order in orders" :key="order.id">
            <div>Date de la commande : {{ order.date }}</div>
            <div>Prix Total : {{ order.total }} €</div>
            <div>Status : {{ order.status }}</div>
            <div>Adresse de livraison : {{ order.address.street }}</div>
            <div>Ville : {{ order.address.city }}</div>
            <div>Code Postale : {{ order.address.zip_code }}</div>
            <ul>
              <li v-for="orderline in order.orderlines" :key="orderline.id">
                <div>Produit : {{ orderline.name }}</div>
                <div>Quantité : {{ orderline.quantity }}</div>
                <div>Prix : {{ orderline.price }} €</div>
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </div>
  <LowerPage></LowerPage>
</template>

<style scoped>
#cart_content {
  position: fixed;
  top: 0;
  right: 0;
  background: white;
  padding: 20px;
  height: 100%;
}

.form-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: white;
  padding: 10px;
  border-radius: 10px;
  z-index: 1;
  width: 80%;
  max-width: 1000px;
}

form input[type="submit"] {
  padding: 10px;
  background: #2c2c2c;
  color: white;
  border-radius: 10px;
  cursor: pointer;
  border: 1px solid #2c2c2c;
  transition: background-color 0.3s, color 0.3s, border 0.3s, transform 0.3s, box-shadow 0.3s;
}

form input[type="submit"]:hover {
  background: white;
  color: #2c2c2c;
  border: 1px solid #2c2c2c;
  transform: scale(1.05); 
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); 
}

form input[type="submit"]:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(0, 0, 0, 0.2); 
  border: 1px solid #2c2c2c;
}


form {
  display: flex;
  flex-direction: column;
  width: 45%;
  margin-left: 70px;
  margin-right: 70px;
  border: 1x solid;

}

input {
  padding: 10px;
  margin: 10px 0;
  border-radius: 10px;
  border: 0.5px solid;
}

input[type=submit] {
  padding: 10px;
  background: #2c2c2c;
  color: white;
  border-radius: 10px;
  cursor: pointer;
}

.divider {
  width: 1px;
  background-color: #ddd;
  height: 300px;
}

.account-wrapper {
  display: flex; 
  justify-content: space-between; 
  gap: 30px; 
  padding: 30px;
}

.account-container {
  background: #f9f9f9;
  border-radius: 10px;
  padding: 30px;
  max-width: 600px;
  flex: 1; 
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}

.account-histo {
  background: #f9f9f9;
  border-radius: 10px;
  padding: 30px;
  max-width: 600px;
  flex: 1; 
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}

.account-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
  text-align: center;
}

.account-info {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.account-info-row {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

.account-info-label {
  font-weight: bold;
  color: #666;
}

.account-info-value {
  color: #333;
  text-align: right;
}

#account-forms {
  background: rgb(55, 67, 50);
  height: 560px;
  mask-image: linear-gradient(rgb(0 0 0 / 90%), rgb(0 0 0));
  display: flex;
  align-items: center;
  justify-content: center;
}

button {
  padding: 15px;
  margin: 20px;
  background: black;
  color: white;
  border-radius: 10px;
  font-size: 1.1rem;
  cursor: pointer;
  border: 1px solid white;
}

button:hover {
  background: white;
  color: black;
  border: 1px solid black;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.loading-spinner {
  width: 100px;
  height: 100px;
}
</style>
