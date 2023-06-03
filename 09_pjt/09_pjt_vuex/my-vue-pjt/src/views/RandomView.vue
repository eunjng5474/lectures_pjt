<template>
  <div class="random">
    <h1>Random</h1>
    <div class="card-list">
      <img :src="`https://image.tmdb.org/t/p/original/${getRandom?.poster_path}`" alt="">
      <h4>{{getRandom?.title}}</h4>
      <p>{{ getRandom?.overview}}</p>
    </div>
    <!-- {{ getRandom.title }} -->
  </div>
</template>

<script>
// import {mapGetters} from 'vuex'

// import axios from 'axios'
// import _ from 'lodash'


export default {
  name: 'RandomView',
  // data() {
  //   return {
  //     movielist: [],
  //     // randomMovie: '',
  //   }
  // },
  computed: {
    ////// {mapGetters} import 후 사용 가능
    // ...mapGetters(['getRandom'])
    getRandom() {
      return this.$store.getters.getRandom


      // // console.log(this.movielist.length)
      // const randomIdx = _.random(0, this.$store.state.movielist.length)
      // // const randomMovie = this.movielist[randomIdx]
      // // console.log(randomMovie)
      // return this.movielist[randomIdx]
    }
  },
  created() {
    this.getMovies()
    // this.getRandom()
    // console.log(this.movielist)
  },
  methods: {
    getMovies() {
      this.$store.dispatch('getMovies')
      // axios({
      //   method: 'get',
      //   url: API_URL,
      // })
      // .then((res) => {
      //   const tmp = res.data.results

      //   for (const i of tmp) {
      //     this.movielist.push(i)
      //   }
      //   // console.log(res.data.results)
      //   // this.movielist.push(res.data.results)
      // })
      // .catch((err) => {
      //   console.log(err)
      // })
    }
    // getRandom() {
    //   // console.log(this.movielist.length)
    //   const randomIdx = _.random(0, 20)
    //   this.randomMovie = this.movielist[randomIdx]
    //   console.log(randomIdx)
    //   // return randomMovie
    // }
  }

}
</script>
