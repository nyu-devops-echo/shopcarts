<template>
  <div id="app" class="container">
    <h1 class="text-center mt-3">Shopcart Service</h1>
    <hr />

    <create-shopcart @created='loadData' />

    <shopcarts :carts='carts' />
  </div>
</template>

<script>
import axios from 'axios';
import CreateShopcart from './components/CreateShopcart';
import Shopcarts from './components/Shopcarts';

export default {
  name: 'App',

  components: { CreateShopcart, Shopcarts },

  data() {
    return {
      carts: []
    }
  },

  mounted() {
    this.loadData();
  },

  methods: {
    loadData() {
      axios.get('/shopcarts')
        .then(response => {
          this.carts = response.data;
        });
    }
  }
}
</script>