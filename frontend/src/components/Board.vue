<template>
  <v-container grid-list-md text-xs-center>
    <v-layout row wrap>
      <v-flex xs4>
        <h1>TODO</h1>
        <task-list :tasks="todo" @taskMoved=""></task-list>
        <form>
          <v-text-field
          ></v-text-field>
          <v-btn color="success" small dark v-on:click="">Add</v-btn>
        </form>
      </v-flex>
      <v-flex xs4>
        <h1>In Progress</h1>
        <task-list :tasks="inProgress" @taskMoved=""></task-list>
      </v-flex>
      <v-flex xs4>
        <h1>Done</h1>
        <task-list :tasks="done" @taskMoved=""></task-list>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  import TaskList from './TaskList'
  import _ from 'lodash'

  export default {
    components: {
      TaskList
    },

    created () {
      this.$store.dispatch('fetchTasks')
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
    }

  }
</script>
