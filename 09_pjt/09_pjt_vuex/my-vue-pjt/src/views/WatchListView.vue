<template>
  <div>
    <h1>보고싶은 영화</h1>
    <div class="watchForm">
      <input type="text" v-model="watchTitle" @keyup.enter="createWatch">
      <button @click="createWatch">Add</button>
    </div>
    <div class="WatchItem">
      <WatchListItem v-for="(watch, idx) in watchList" :key="idx" :watch="watch"/>
    </div>
  </div>
</template>

<script>
import WatchListItem from '@/components/WatchListItem'

export default {
  name: 'WatchListView',
  components: {
    WatchListItem
  },
  data() {
    return {
      watchTitle: null,
      watchList: [],
    }
  },
  methods: {
    createWatch() {
      if (this.watchTitle) {
        this.watchList.push(this.watchTitle)
      } else {
        alert('보고싶은 영화를 입력하세요!')
      }
      this.watchTitle = null
    }
  }
}
</script>

<style>

</style>