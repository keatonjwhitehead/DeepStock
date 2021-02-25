<template>
  <div :class="custom">
      <div class="card-body p-1">
      <slot></slot>
    </div>
  </div>
</template>
<script>

export default {
  name: 'main-card',
  props: {
    title: {
      type: String,
      default: ''
    },
    custom:{
      type: String,
      default: ''
    }
  },
  data(){
    return {
    }
  }
}

</script>
<style scoped>

</style>
