<template>
  <v-container grid-list-md text-xs-center>

    <v-layout row wrap>
      <v-flex xs4>
        <h1>TODO</h1>
        <task-list :tasks="todo" @taskMoved="movedTodo"></task-list>
        <form>
          <v-text-field v-model="newTaskBody"
          ></v-text-field>
          <v-btn color="success" small dark v-on:click="addTask" v-if="!addingNewTask">Add</v-btn>
          <v-progress-circular indeterminate v-bind:width="3" color="green" v-if="addingNewTask"></v-progress-circular>
        </form>
      </v-flex>
      <v-flex xs4>
        <h1>In Progress</h1>
        <task-list :tasks="inProgress" @taskMoved="movedInProgress"></task-list>
      </v-flex>
      <v-flex xs4>
        <h1>Done</h1>
        <task-list :tasks="done" @taskMoved="movedDone"></task-list>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  import TaskList from './TaskList'
  import _ from 'lodash'

  export default {
    data() {
      return {
        newTaskBody: ''
      }
    },

    components: {
      TaskList
    },

    created () {
      this.refresh()
    },

    computed: {
      todo () {
        return this.$store.getters.todo
      },

      inProgress () {
        return this.$store.getters.inProgress
      },

      done () {
        return this.$store.getters.done
      },

      addingNewTask() {
        console.log('blabla')
        return this.$store.getters.addingNewTask
      }
    },

    methods: {
      refresh() {
        this.$store.dispatch('setBoard', this.$route.params.pk)
        this.$store.dispatch('fetchTasks').catch(error => {
          console.log(error)
          this.$router.push('/not-found')
        })
      },

      movedTodo({taskPk}) {
        this.$store.dispatch('changedTaskStatus',
          {taskPk: taskPk, fromStatus: 'todo', toStatus: 'inProgress'})
      },

      movedInProgress({taskPk}) {
        this.$store.dispatch('changedTaskStatus',
          {taskPk: taskPk, fromStatus: 'inProgress', toStatus: 'done'})
      },

      movedDone({taskPk}) {
        this.$store.dispatch('movedDone', taskPk)
      },

      addTask() {
        this.$store.dispatch('addTask', this.newTaskBody)
        this.newTaskBody = ''
      },

      goHome() {
        this.$router.push({name: 'index'})
      }
    },

    watch:{
      $route (to, from){
        this.refresh()
      }
    }
  }
</script>
