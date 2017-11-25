<template>
  <div class="card mb-3">
    <div class="card-header">
      All Shopcarts
    </div>
    
    <spinner v-if="loading" />

    <div class="card-body">
      <div class="form-group row">
        <label for="filter" class="col-sm-4 col-form-label">Filter by product:</label>
        <div class="col-sm-8">
          <select class="form-control" id="filter" v-model='selected' @change="filter">
            <option value="" id="all-products-option">All Products</option>
            <option v-for="product in products"
              :value="product.id"
              :id="`product-${product.id}-option`">
                {{ product.name }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <table class="table table-custom" id="shopcarts-table-list">
      <thead>
        <tr>
          <th scope="col">User Id</th>
          <th scope="col"># of Products</th>
          <th scope="col"></th>
        </tr>
      </thead>
      <tbody>
        <template v-if='carts.length'>
          <tr v-for="cart in carts" :id="`shopcart-${cart.user_id}-row`">
            <th scope="row">{{ cart.user_id }}</th scope="row">
            <td>{{ Object.keys(cart.products).length }}</td>
            <td><button class="btn btn-link" @click="navigate(cart)" :id="`view-shopcart-${cart.user_id}`">View</button></td>
          </tr>
        </template>
        <tr v-else id="empty-shopcarts">
          <td colspan="3" style="padding: .375rem .75rem">No Shopcarts</td>
        </tr>
      </tbody>
    </table>
    
    <div class="card-body">
      <button class="btn btn-danger" @click="prune" id="prune-shopcarts">Prune</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Spinner from './Spinner';

export default {
  name: "ListShopcarts",

  components: { Spinner },

  props: {
    carts: {
      type: Array,
      required: true
    },

    products: {
      type: Array,
      required: true
    },

    loading: {
      type: Boolean,
      default: false
    }
  },

  data() {
    return {
      selected: ""
    }
  },

  methods: {
    navigate(cart) {
      this.$emit('navigate', { 
        view: 'Shopcart',
        userId: cart.user_id
      });
    },

    filter() {
      this.$emit('filter', this.selected);
    },

    prune() {
      axios.delete('/shopcarts/prune')
        .then(response => {
          this.selected = "";
          this.$emit('pruned');
        });
    }
  }
};
</script>

<style>
  .table.table-custom {
    margin-bottom: 0;
  }

  .table.table-custom td,
  .table.table-custom tbody th {
    padding: 0 .75rem;
    vertical-align: middle;
  }
</style>