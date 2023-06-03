<template>
  <div>
    <p @click="updateWatch">{{ watch }}</p>
  </div>
</template>

<script>
export default {
  name: 'WatchListItem',
  props: {
    watch: String,
  },
  methods: {
    updateWatch(data) {
      data.target.classList.toggle('line')
    }
  }
}
</script>

<style>
.line {
  text-decoration: line-through;
}
</style>