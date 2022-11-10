<template>
  <div class="header">
    <Header></Header>
  </div>
  <div class="main">
    <router-view></router-view>
  </div>
  <div class="footer">
    <Footer></Footer>
  </div>
</template>

<script setup>
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';
</script>

<style scoped>
.main {
  width: 60%;
  /* background-color: white; */
  margin: 0 auto;
}
</style>
