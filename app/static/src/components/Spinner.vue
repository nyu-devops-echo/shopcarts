<template>
  <div class="spinning">
    <vue-simple-spinner
      message="Loading..."
      text-fg-color="#000"
      line-bg-color="#000"
      class="position-absolute spinner" />
  </div>
</template>

<script>
import Spinner from 'vue-simple-spinner';

export default {
  name: 'Spinner',

  components: {
    VueSimpleSpinner: Spinner
  }
}
</script>

<style>
.spinning {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 100%;
  background-color: #ececec;
  opacity: .5;
  z-index: 100;
}

.spinning .spinner {
  top: 40%;
  right: 45%;
}
</style>