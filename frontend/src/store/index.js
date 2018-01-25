import axios from 'axios'
import _ from 'lodash'
import Vuex from 'vuex'

export default new Vuex.Store({
  state: {
    todo: [],
    inProgress: [],
    done: [],

    boardPk: 'beczkowb'
  },

  getters: {
    todo: state => state.todo,
    inProgress: state => state.inProgress,
    done: state => state.done
  },

  mutations: {
    SET_TASKS (state, tasks) {
      state.todo = _.reduce(_.filter(tasks, t => t.status === 'todo'), (todo, task) => {
        todo[task.pk] = {body: task.body}
      })
      state.inProgress = _.reduce(_.filter(tasks, t => t.status === 'in_progress'), (inProgress, task) => {
        inProgress[task.pk] = {body: task.body}
      })
      state.done = _.reduce(_.filter(tasks, t => t.status === 'done'), (done, task) => {
        done[task.pk] = {body: task.body}
      })
    }
  },

  actions: {
    fetchTasks({ commit, state }) {
      axios
        .get('http://127.0.0.1:5000/api/boards/' + state.boardPk + '/tasks')
        .then(r => r.data)
        .then(tasks => {
          commit('SET_TASKS', tasks)
        })
    }
  }
})
