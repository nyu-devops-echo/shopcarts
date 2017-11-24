<template>
  <div>
    <div class="card mb-3">
      <div class="card-header">
        Shopcart for User: {{ cart.user_id }}
      </div>
      <div class="list-group list-group-flush" v-if="Object.keys(cart.products).length">
        <div class="list-group-item" v-for="product in cart.products">
          <div class="row">
            <div class="col-sm">
              <h5 class="mb-1">{{ product.name }}</h5>
              <small>{{ product.description }}</small>
            </div>
            <div class="col-sm">
              <input type="number" class="form-control form-control-sm" v-model="product.quantity" @keydown.enter="update(product)" />
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
      <button class="btn btn-primary" @click="updateCart">Update</button>
    </products>

    <p>
      <button class="btn btn-link" @click="navigate">&laquo; Back</button>
    </p>
  </div>
</template>

<script>
import axios from 'axios';
import Products from './Products';

export default {
  name: 'Shopcart',

  components: { Products },

  props: {
    userId: {
      type: Number,
      required: true
    }
  },

  data() {
    return {
      cart: { products: {}},
      addedProducts: {}
    }
  },

  mounted() {
    this.loadCart();
  },

  methods: {
    loadCart() {
      axios.get(`/shopcarts/${this.userId}`)
        .then(response => {
          this.cart = response.data;
        });
    },

    update(product) {
      axios.put(`/shopcarts/${this.userId}/products/${product.id}`, {
          quantity: parseInt(product.quantity)
        })
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

    navigate() {
      this.$emit('navigate', { 
        view: 'Shopcarts'
      });
    },
  }
}
</script>