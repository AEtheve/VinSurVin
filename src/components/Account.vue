<script setup lang="ts">
import { ref, onMounted } from 'vue';
import LowerPage from './LowerPage.vue';
const registerFormMessage = ref("");
const registerFormError = ref("");
const loginFormMessage = ref("");
const loginFormError = ref("");

const isConnected = document.cookie.includes("csrftoken");

const accountInfo = ref({});

onMounted(() => {
  if (isConnected) {
    getInfos();
  } else {
    document.getElementById("formRegister").addEventListener("submit", function (event) {
      event.preventDefault();

      fetch("http://localhost:8000/user/new", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: event.target.email.value,
          password: event.target.password.value,
          username: event.target.email.value
        })
      })
        .then(response => response.json())
        .then(data => {
          if (data.error) {
            registerFormError.value = data.error;
          } else {
            registerFormMessage.value = data.message;
          }
        })
    });

    document.getElementById("formLogin").addEventListener("submit", function (event) {
      event.preventDefault();

      fetch("http://localhost:8000/user/login", {
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
            loginFormError.value = data.error;
          } else {
            loginFormMessage.value = data.message;
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
  fetch("http://localhost:8000/user/info", {
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
</script>

<template>
  <div>
    <div v-if="!isConnected" style="background: rgb(55, 67, 50); height: 560px;
    mask-image: linear-gradient(rgb(0 0 0 / 90%), rgb(0 0 0));
    display: flex;
    align-items: center;
    justify-content: center;">
      <!-- Conteneur des deux formulaires et du diviseur -->
      <div id="form_account" class="form-wrapper">
        <form id="formLogin" method="POST">
          <h2>Connectez-vous</h2>
          Vous avez déjà un compte sur VinSurVin ?
          <input type="text" name="username" placeholder="Nom d'utilisateur" />
          <input type="password" name="password" placeholder="Mot de passe" />
          <input type="submit" value="Se connecter" />

          <p v-if="loginFormMessage != ''">{{ loginFormMessage }}</p>
          <p v-if="loginFormError != ''">{{ loginFormError }}</p>
        </form>

        <!-- Ligne séparatrice -->
        <div class="divider"></div>

        <!-- Formulaire d'inscription -->
        <form id="formRegister" method="POST">
          <h2>Nouveau client ?</h2>
          <input type="text" name="email" placeholder="Adresse email" />
          <input type="password" name="password" placeholder="Mot de passe" />
          <input type="submit" value="Poursuivre l'inscription" />

          <p v-if="registerFormMessage != ''">{{ registerFormMessage }}</p>
          <p v-if="registerFormError != ''">{{ registerFormError }}</p>
        </form>
      </div>

      <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;">
        <video src="https://vinsurvin-bucket.s3.eu-west-3.amazonaws.com/wine_video.mp4" autoplay loop muted style="width: 100%; height: 100%; object-fit: cover; opacity: 0.7; background-color: black;"></video>
      </div>

    </div>

    <div v-else class="account-container">
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
    </div>

    <LowerPage></LowerPage>
  </div>
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

form {
  display: flex;
  flex-direction: column;
  width: 45%;
  margin-left: 70px;
  margin-right: 70px;
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

.account-container {
  background: #f9f9f9;
  border-radius: 10px;
  padding: 30px;
  max-width: 600px;
  margin: 0 auto;
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
</style>
