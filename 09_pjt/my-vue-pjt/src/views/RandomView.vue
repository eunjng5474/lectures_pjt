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
import axios from 'axios'
import _ from 'lodash'

const API_URL = 'https://api.themoviedb.org/3/movie/top_rated'

export default {
  name: 'RandomView',
  data() {
    return {
      movielist: [],
      // randomMovie: '',
    }
  },
  computed: {
    getRandom() {
      // console.log(this.movielist.length)
      const randomIdx = _.random(0, this.movielist.length)
      // const randomMovie = this.movielist[randomIdx]
      // console.log(randomMovie)
      return this.movielist[randomIdx]
    }
  },
  created() {
    this.getMovies()
    // this.getRandom()
    // console.log(this.movielist)
  },
  methods: {
    getMovies() {
      axios({
        method: 'get',
        url: API_URL,
        params: {
          api_key: '',
          language: 'ko-KR',
          page: 1 
        }
      })
      .then((res) => {
        const tmp = res.data.results

        for (const i of tmp) {
          this.movielist.push(i)
        }
        // console.log(res.data.results)
        // this.movielist.push(res.data.results)
      })
      .catch((err) => {
        console.log(err)
      })
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
