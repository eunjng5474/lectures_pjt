<template>
  <div>
    <div class="card-list">
      <img :src="`https://image.tmdb.org/t/p/original/${movie.poster_path}`" alt="">
      <h4>{{movie.title}}</h4>
      <p>{{ movie.overview}}</p>
    </div>
  </div>
</template>

<script>

export default {
  name: 'MovieCard',
  props: {
    movie: Object,
  }
}
</script>

<style>
.card-list {
  width: 500px;
  height: 700px;
}

.card-list > img {
  width: 60%;
  height: 60%;
}

</style>