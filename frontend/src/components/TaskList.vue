<template>
  <v-list>
    <v-list-tile avatar v-for="task in taskList" v-bind:key="task.pk" @click="">
      <v-list-tile-content>
        <v-list-tile-title v-text="task.body"></v-list-tile-title>
      </v-list-tile-content>
      <v-btn color="primary" fab small dark v-on:click="onMove(task.pk)">
        <v-icon>forward</v-icon>
      </v-btn>
    </v-list-tile>
  </v-list>
</template>

<script>
  export default {
    name: 'task-list',
    props: ['tasks'],
    methods: {
      onMove(taskPk) {
        this.$emit('taskMoved', {
          taskPk: taskPk
        })
      }
    },

    computed: {
      taskList() {
        let taskList = []
        for (let taskPk in this.tasks) {
          if (this.tasks.hasOwnProperty(taskPk)) {
            taskList.push({
              body: this.tasks[taskPk].body,
              pk: taskPk
            })
          }
        }
        return taskList
      }
    }
  }
</script>
