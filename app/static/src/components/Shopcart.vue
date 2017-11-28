<template>
  <div>
    <div class="card mb-3">
      <div class="card-header" id="shopcart-header">
        Shopcart for User: {{ cart.user_id }}
        <button class="btn btn-sm btn-danger float-right" @click="deleteCart" id="delete-btn">Delete Cart</button>
      </div>

      <spinner v-if="loading" />

      <div class="list-group list-group-flush" v-if="hasProducts" id="shopcart-products-list">
        <div class="list-group-item" v-for="product in cart.products" :id="`shopcart-product-${product.id}`">
          <div class="row">
            <div class="col-sm">
              <h5 class="mb-1">{{ product.name }}</h5>
              <small>{{ product.description }}</small>
            </div>

            <div class="col-sm">
              <input type="number"
                :id="`product-${product.id}-quantity`"
                class="form-control form-control-sm"
                v-model="product.quantity"
                @keydown.enter="updateProduct(product)" />
            </div>

            <div class="col-sm-2">
              <button
                :id="`product-${product.id}-delete`"
                class="btn btn-sm btn-outline-danger float-right"
                @click="deleteProduct(product)">
                  <span class="oi oi-trash"></span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="card-body" v-else>
        No products in this shopcart
      </div>
    </div>

    <products
      v-bind="$attrs"
      v-model="addedProducts">
    </products>
    <button class="btn btn-primary" @click="updateCart" id="update-btn">Update</button>

    <p>
      <button  class="btn btn-link" @click="navigate" id="back-btn">&laquo; Back</button>
    </p>
  </div>
</template>

<script>
import axios from 'axios';
import Spinner from './Spinner';
import Products from './Products';

export default {
  name: 'Shopcart',

  components: { Spinner, Products },

  props: {
    userId: {
      type: Number,
      required: true
    }
  },

  data() {
    return {
      loading: false,
      cart: { products: {}},
      addedProducts: {}
    }
  },

  computed: {
    hasProducts() {
      return Object.keys(this.cart.products).length;
    }
  },

  mounted() {
    this.loadCart();
  },

  methods: {
    loadCart() {
      this.loading = true;

      axios.get(`/shopcarts/${this.userId}`)
        .then(response => {
          this.cart = response.data;
          this.loading = false;
        });
    },

    updateProduct(product) {
      axios.put(`/shopcarts/${this.userId}/products/${product.id}`, {
          quantity: parseInt(product.quantity)
        })
        .then(() => {
          this.loadCart();
        });
    },

    deleteProduct(product) {
      axios.delete(`/shopcarts/${this.userId}/products/${product.id}`)
        .then(() => {
          this.loadCart();
        });
    },

    updateCart() {
      axios.post(`/shopcarts/${this.userId}/products`, this.addedProducts)
        .then(() => {
          this.loadCart();
          this.addedProducts = {};
        });
    },

    deleteCart() {
      axios.delete(`/shopcarts/${this.userId}`)
        .then(() => {
          this.navigate();
        });
    },

    navigate() {
      this.$emit('navigate', {
        view: 'Shopcarts'
      });
    },
  }
}
</script>
