<template>
  <div class="card mb-3">
    <div class="card-header">
      <a href="#" @click.prevent="show = !show" id="add-products-btn">Add-Products<span class="oi" :class="show ? 'oi-minus' : 'oi-plus'"></span>
      </a>
    </div>
    <div class="card-body" v-show="show">
      <div class="form-group row" v-for="product in products">
        <label :for="`product-${product.id}`" class="col-sm col-form-label col-form-label-sm">{{ product.name }}</label>
        <div class="col-sm">
          <input type="number" class="form-control" :id="`product-${product.id}-quantity`" v-model="value[product.id]" placeholder="0" @change="updateProducts"/>
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