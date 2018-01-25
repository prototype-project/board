import Vue from 'vue'
import Vuex from 'vuex'

import Router from 'vue-router'
import Board from '@/components/Board'
import BoardCreator from '@/components/BoardCreator'

Vue.use(Vuex)
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: BoardCreator
    },
    {
      path: '/boards/:pk',
      name: 'Board',
      component: Board
    }
  ]
})
