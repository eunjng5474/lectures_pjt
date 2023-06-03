<template>
  <div class="movie">
    <h1>Movie</h1>
    <div class="container">
      <div class="card">
        <MovieCard v-for="movie in movielist" :key="movie.id" :movie="movie"/>
      </div> 
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import MovieCard from '@/components/MovieCard'

const API_URL = 'https://api.themoviedb.org/3/movie/top_rated'

// @ is an alias to /src

export default {
  name: 'MovieView',
  components: {
    MovieCard,
  },
  data() {
    return {
      movielist: []
    }
  },
  created() {
    this.getMovies()
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

        this.movielist = tmp
        // for (const i of tmp) {
        //   this.movielist.push(i)
        // }
        // console.log(res.data.results)
        // this.movielist.push(res.data.results)
      })
      .catch((err) => {
        console.log(err)
      })
    }
  }

}
</script>

<style scoped>
  /* .container {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
  } */

  .card {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
  }

  /* .card > img {
    width: 100%;
    height: 80%;
  } */
</style>