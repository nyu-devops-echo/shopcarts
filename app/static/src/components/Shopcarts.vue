<template>
  <div class="card mb-3">
    <div class="card-header">
      All Shopcarts
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
  </div>
</template>

<script>
export default {
  name: "Shopcarts",

  props: {
    carts: {
      type: Array,
      required: true
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