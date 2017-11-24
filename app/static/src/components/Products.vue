<template>
  <div class="card mb-3">
    <div class="card-header">
      <a href="#" @click.prevent="show = !show" id="toggle-products">
        Add Products  <span class="oi" :class="show ? 'oi-minus' : 'oi-plus'"></span>
      </a>
    </div>
    <div class="card-body" v-show="show">
      <div class="form-group row" v-for="product in products">
        <label :for="`product-${product.id}`" class="col-sm col-form-label col-form-label-sm">{{ product.name }}</label>
        <div class="col-sm">
          <select class="form-control form-control-sm"
            :id="`product-${product.id}`"
            v-model="value[product.id]"
            @change="updateProducts">
            <option>1</option>
            <option>2</option>
            <option>3</option>
            <option>4</option>
            <option>5</option>
          </select>
        </div>
      </div>

      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Products',

  props: {
    products: {
      type: Array,
      required: true
    },

    value: {
      type: Object,
      required: true
    } 
  },

  data() {
    return {
      show: false
    }
  },

  methods: {
    updateProducts() {
      for (let productId in this.value) {
        this.value[productId] = parseInt(this.value[productId]);
      }
    }
  }
}
</script>