<template>
  <div>
    <p><strong>{{ id }}</strong> | {{ name }}</p>
  </div>
</template>

<script>
export default {
  name: 'Article',
  props: {
    name: {
      type: String,
      required: true
    },
    id: {
      type: [String, Number],
      required: true
    }
  }
}
</script>

<style scoped>
p {
  font-size: 16px;
  margin: 4px 0;
}
</style>
