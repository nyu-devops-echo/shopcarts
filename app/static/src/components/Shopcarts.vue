<template>
  <div class="card mb-3">
    <div class="card-header">
      All Shopcarts
    </div>
    <div class="card-body">
      <div class="form-group row">
        <label for="filter" class="col-sm-4 col-form-label">Filter by product:</label>
        <div class="col-sm-8">
          <select class="form-control" id="filter" v-model='selected' @change="filter">
            <option value="">All Products</option>
            <option v-for="product in products" :value="product.id">{{ product.name }}</option>
          </select>
        </div>
      </div>
    </div>

    <table class="table table-custom">
      <thead>
        <tr>
          <th scope="col">User Id</th>
          <th scope="col"># of Products</th>
          <th scope="col"></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="cart in carts">
          <th scope="row">{{ cart.user_id }}</th scope="row">
          <td>{{ Object.keys(cart.products).length }}</td>
          <td><button class="btn btn-link">View</button></td>
        </tr>
      </tbody>
    </table>
    
    <div class="card-body">
      <button class="btn btn-danger" @click="prune">Prune</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "Shopcarts",

  props: {
    carts: {
      type: Array,
      required: true
    },

    products: {
      type: Array,
      required: true
    }
  },

  data() {
    return {
      selected: ""
    }
  },

  methods: {
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