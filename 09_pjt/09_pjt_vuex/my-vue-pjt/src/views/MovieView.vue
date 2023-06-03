<template>
  <div class="movie">
    <h1>Movie</h1>
    <!-- {{ movielist }} -->
    <div class="container">
      <div class="card">
        <MovieCard v-for="movie in movielist" :key="movie.id" :movie="movie"/>
      </div> 
    </div>
    <!-- <img src="@/assets/star.gif" alt=""> -->
  </div>
</template>

<script>
// import axios from 'axios'
import MovieCard from '@/components/MovieCard'

// const API_URL = 'https://api.themoviedb.org/3/movie/top_rated?api_key=8254428aabea05691b14e62f42a3d4a3&language=ko-KR&page=1'

// @ is an alias to /src

export default {
  name: 'MovieView',
  components: {
    MovieCard,
  },
  computed: {
    movielist() {
      return this.$store.state.movielist
    }
  },
  // data() {
  //   return {
  //     // movielist: []
  //   }
  // },
  created() {
    this.getMovies()
    // console.log(this.movielist)
  },
  methods: {
    getMovies() {
      this.$store.dispatch('getMovies')
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