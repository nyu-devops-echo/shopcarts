<template>
  <div class="card mb-3">
    <div class="card-header">
      Create Shopcart
    </div>
    <div class="card-body">
      <form @submit.prevent="submit">
        <p id="form-error" class="form-text text-danger">{{ error }}</p>
        <div class="form-group">
          <input type="number" class="form-control" v-model="user_id" id="user_id" placeholder="Enter User Id" />
        </div>

        <button type="submit" class="btn btn-primary">Create</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "CreateShopcart",

  props: {
    products: {
      type: Array,
      required: true
    }
  },

  data() {
    return {
      user_id: null,
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
        user_id: this.user_id
      })
      .then(response => {
        this.$emit('created');
        this.user_id = null;
      })
      .catch(error => {
        this.error = "Status Code: " + error.response.status + ". ";
        this.error += error.response.data.error;
      });
    }
  }
};
</script>