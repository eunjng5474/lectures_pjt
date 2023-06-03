import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import _ from 'lodash'


// const API_URL = 'https://api.themoviedb.org/3/movie/top_rated'
const API_URL = 'https://api.themoviedb.org/3/discover/movie'
Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    movielist: [],
  },
  getters: {
    listLength(state) {
      return state.movielist.length
    },
    getRandom(state, getters) {
      const randomIdx = _.random(0, getters.listLength)
      // console.log(state.movielist[randomIdx])
      return state.movielist[randomIdx]
    }
  },
  mutations: {
    GET_MOVIES(state, moviesList) {
      state.movielist = moviesList
      // for (const i of moviesList) {
      //   state.movielist.push(i)
      // }
      console.log(state.movielist)
    }
  },
  actions: {
    getMovies(context) {
      axios({
        method: 'get',
        url: API_URL,
        params: {
          api_key: '8254428aabea05691b14e62f42a3d4a3',
          language: 'ko-KR',
          page: 1 ,
          with_companies:'%2C',
          with_people:'%2C',
          // with_genres: 878
        }
      })
      .then((res) => {
        context.commit('GET_MOVIES', res.data.results)
        // const tmp = res.data.results

        // for (const i of tmp) {
        //   this.movielist.push(i)
        // }
      })
      .catch((err) => {
        console.log(err)
      })
    }
  },
  modules: {
  }
})
