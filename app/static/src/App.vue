<template>
  <div id="app-js" class="container">
    <h1 class="text-center mt-3">Shopcarts REST API Service</h1>
    <a href="/apidocs/index.html">Documentation</a>
    <hr />

    <transition name="component-fade" mode="out-in">
      <component
        :is="view"
        :products='products'
        :userId='userId'
        @navigate='changeView' />
    </transition>
  </div>
</template>

<script>
import axios from 'axios';
import Shopcart from './components/Shopcart';
import Shopcarts from './components/Shopcarts';

export default {
  name: 'App',

  components: { Shopcart, Shopcarts },

  data() {
    return {
      view: 'Shopcarts',
      products: [],
      userId: null
    }
  },

  mounted() {
    this.loadProducts();
  },

  methods: {
    loadProducts() {
      axios.get('/products')
        .then(response => {
          this.products = response.data;
        });
    },

    changeView({ view, userId }) {
      this.view = view;
      this.userId = userId || null;
    }
  }
}
</script>

<style>
  .component-fade-enter-active,
  .component-fade-leave-active {
    transition: opacity .3s ease;
  }

  .component-fade-enter,
  .component-fade-leave-to {
    opacity: 0;
  }
</style>