<template>
  <div id="app" class="container">
    <h1 class="text-center mt-3">Shopcart Service</h1>
    <hr />

    <create-shopcart
      :products='products'
      @created='loadCarts' />

    <shopcarts
      :carts='carts'
      :products='products'
      @filter='loadCarts'
      @pruned='loadCarts' />
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
      carts: [],
      products: []
    }
  },

  mounted() {
    this.loadCarts();
    this.loadProducts();
  },

  methods: {
    loadCarts(productId) {
      const pid = productId || null;
      
      axios.get('/shopcarts', { params: { pid } })
        .then(response => {
          this.carts = response.data;
        });
    },

    loadProducts() {
      axios.get('/products')
        .then(response => {
          this.products = response.data;
        });
    }
  }
}
</script>