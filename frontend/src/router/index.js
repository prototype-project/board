import Vue from 'vue'
import Vuex from 'vuex'

import Router from 'vue-router'
import Board from '@/components/Board'
import BoardCreator from '@/components/BoardCreator'
import NotFoundPage from '@/components/NotFoundPage'

Vue.use(Vuex)
Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'index',
      component: BoardCreator
    },
    {
      path: '/boards/:pk',
      name: 'board',
      component: Board
    },
    {
      path: '/not-found',
      name: 'notFound',
      component: NotFoundPage
    },
    { path: '*', component: NotFoundPage }
  ]
})
