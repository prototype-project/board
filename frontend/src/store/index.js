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
      state.todo = _.forEach(_.filter(tasks, t => t.status === 'todo'), t => t.changingStatus = false)
      state.inProgress = _.forEach(_.filter(tasks, t => t.status === 'inProgress'), t => t.changingStatus = false)
      state.done = _.forEach(_.filter(tasks, t => t.status === 'done'), t => t.changingStatus = false)
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
    },

    MARK_AS_CHANGING_STATUS (state, {taskPk, fromStatus}) {
      let toMark = _.find(state[fromStatus], t => t.pk === taskPk)
      toMark.changingStatus = true
      state[fromStatus] = _.filter(state[fromStatus], t => t.pk !== taskPk)
      state[fromStatus].push(toMark)
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
      commit('MARK_AS_CHANGING_STATUS', {taskPk, fromStatus})
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
      commit('MARK_AS_CHANGING_STATUS', {taskPk: taskPk, fromStatus: 'done'})
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
