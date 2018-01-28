import axios from 'axios'
import _ from 'lodash'
import Vuex from 'vuex'

export default new Vuex.Store({
  state: {
    todo: [],
    inProgress: [],
    done: [],

    boardPk: null
  },

  getters: {
    todo: state => state.todo,
    inProgress: state => state.inProgress,
    done: state => state.done,
    boardPk: state => state.boardPk
  },

  mutations: {
    SET_TASKS (state, tasks) {
      state.todo = _.filter(tasks, t => t.status === 'todo')
      state.inProgress = _.filter(tasks, t => t.status === 'inProgress')
      state.done = _.filter(tasks, t => t.status === 'done')
    },

    CHANGE_STATUS (state, {taskPk, fromStatus, toStatus}) {
      let toMove = _.find(state[fromStatus], t => t.pk === taskPk)
      state[fromStatus] = _.filter(state[fromStatus], t => t.pk !== taskPk)
      state[toStatus].push({body: toMove.body, pk: toMove.pk, status: toStatus})
    },

    DELETE_DONE (state, taskPk) {
      state.done = _.filter(state.done, t => t.pk !== taskPk)
    },

    ADD_TASK (state, task) {
      state.todo.push(task)
    },

    SET_BOARD (state, boardPk) {
      state.boardPk = boardPk
    }
  },

  actions: {
    fetchTasks ({ commit, state }) {
      axios
        .get('/api/boards/' + state.boardPk + '/tasks')
        .then(r => r.data)
        .then(tasks => {
          commit('SET_TASKS', tasks)
        })
    },

    changedTaskStatus ({commit, state}, {taskPk, fromStatus, toStatus}) {
      console.log(taskPk)
      console.log(fromStatus)
      console.log(toStatus)
      let task = _.find(state[fromStatus], t => t.pk === taskPk)
      console.log(task)
      let updatedTask = {
        pk: taskPk,
        body: task.body,
        status: toStatus
      }
      axios
        .put('/api/boards/' + state.boardPk + '/tasks/' + taskPk, updatedTask)
        .then(() => {
          commit('CHANGE_STATUS', {taskPk, fromStatus, toStatus})
        })
    },

    movedDone ({commit, state}, taskPk) {
      axios
        .delete('/api/boards/' + state.boardPk + '/tasks/' + taskPk)
        .then(() => {
          commit('DELETE_DONE', taskPk)
        })
    },

    addTask ({commit, state}, body) {
      let newTask = {status: 'todo', body: body}
      axios
        .post('/api/boards/' + state.boardPk + '/tasks', newTask)
        .then(r => r.data)
        .then(task => {
          commit('ADD_TASK', task)
        })
    },

    createBoard ({commit, state}) {
      return axios
        .post('/api/boards')
        .then(r => r.data)
        .then(board => {
          return commit('SET_BOARD', board.pk)
        })
    },

    setBoard ({commit, state}, boardPk) {
      commit('SET_BOARD', boardPk)
    }
  }
})
