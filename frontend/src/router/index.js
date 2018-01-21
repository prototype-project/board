import Vue from 'vue'
import Router from 'vue-router'
import Board from '@/components/Board'
import BoardCreator from '@/components/BoardCreator'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: BoardCreator
    },
    {
      path: '/boards',
      name: 'Board',
      component: Board
    }
  ]
})
