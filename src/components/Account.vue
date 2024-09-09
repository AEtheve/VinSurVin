<script setup lang="ts">
import { ref } from 'vue';
const cartOpen = ref(false);
</script>

<template>
  <div>
    <div style="background: rgb(55, 67, 50); height: 560px;
    mask-image: linear-gradient(rgb(0 0 0 / 90%), rgb(0 0 0));
    display: flex;
    align-items: center;
    justify-content: center;
    ">
      <div>
        <div id="form_account">
          <form>
            <h2>Connectez-vous</h2>
            Vous avez déjà un compte sur VinSurVin ?
            <input type="email" name="email" placeholder="Adresse email" />
            <input type="password" name="password" placeholder="Mot de passe" />
            <input type="submit" value="Se connecter" />
          </form>

          <form>
            <h2>Nouveau client ?</h2>
            <input type="email" name="email" placeholder="Adresse email" />
            <input type="submit" value="Poursuivre l'inscription"/>
          </form>
        </div>
      </div>


      <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;">
        <video src="../assets/wine_video.mp4" autoplay loop muted style="width: 100%; height: 100%; object-fit: cover; opacity: 0.7; background-color: black;
      
      "></video>

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

#form_account {
  position: relative;
  background: white;
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 1;
  padding: 15px;
  border-radius: 10px;
}

form {
  display: inline-flex;
  flex-direction: column;
}

input{
  padding: 10px;
  margin: 10px;
  border-radius: 10px;
  border: 0.5px solid;
}

input[type=submit]{
  padding: 10px;
  margin: 10px;
  background: #2c2c2c;
  color: white;
  border-radius: 10px
}
</style>
