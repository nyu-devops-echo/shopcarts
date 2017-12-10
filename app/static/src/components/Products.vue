<template>
  <div class="card mb-3">
    <div class="card-header">
      <a href="#" @click.prevent="show = !show" id="add-products-btn">Add-Products<span class="oi" :class="show ? 'oi-minus' : 'oi-plus'"></span>
      </a>
    </div>
    <div class="card-body" v-show="show">
      <div class="form-group row" v-for="product in products" :key="product.id">
        <label :for="`product-${product.id}`" class="col-sm col-form-label col-form-label-sm">{{ product.name }}</label>
        <div class="col-sm">
          <input type="number" class="form-control" :id="`product-${product.id}-select`" placeholder="0" @input="updateProducts" :data-pid="product.id"/>
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
      type: Array,
      required: true
    } 
  },

  data() {
    return {
      show: false,
      selected: []
    }
  },

  methods: {
    updateProducts($event) {
      const pid = $event.target.dataset.pid;
      const quantity = $event.target.value;
      
      this.selected[pid-1] = {
        pid: parseInt(pid),
        quantity: parseInt(quantity)
      };

      this.$emit('input', this.selected.filter(x => x));
    }
  }
}
</script>