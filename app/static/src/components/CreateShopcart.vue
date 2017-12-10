<template>
  <div class="card mb-3">
    <div class="card-header">
      Create Shopcart
    </div>
    <div class="card-body">
      <form @submit.prevent="submit" id="shopcart-create-form">
        <p id="form-error" class="form-text text-danger">{{ error }}</p>
        <div class="form-group">
          <input type="number" class="form-control" v-model="user_id" id="user_id" placeholder="Enter User Id" />
        </div>

        <products
          v-bind="$attrs"
          v-model="addedProducts" />

        <button type="submit" class="btn btn-primary" id="create-btn">Create</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Products from './Products';

export default {
  name: "CreateShopcart",

  components: { Products },

  data() {
    return {
      user_id: null,
      addedProducts: [],
      error: ''
    }
  },

  methods: {
    submit() {
      this.error = '';

      if (!this.user_id) {
        this.error = 'Please enter a user id.';
        return;
      }

      axios.post('/shopcarts', {
        user_id: this.user_id,
        products: this.addedProducts
      })
      .then(response => {
        this.$emit('created');
        this.user_id = null;
        this.addedProducts = [];
      })
      .catch(error => {
        this.error = "Status Code: " + error.response.status + ". ";
        this.error += error.response.data.error;
      });
    }
  }
};
</script>
