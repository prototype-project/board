<template>
  <v-list>
    <v-list-tile avatar v-for="task in tasks" v-bind:key="task.pk" @click="">
      <v-list-tile-content>
        <v-list-tile-title v-text="task.body"></v-list-tile-title>
      </v-list-tile-content>
      <v-btn color="primary" fab small dark v-on:click="onMove(task.pk)" v-if="!task.changingStatus">
        <v-icon>forward</v-icon>
      </v-btn>
      <v-progress-circular indeterminate v-bind:width="3" color="primary" v-if="task.changingStatus"></v-progress-circular>
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
    }

  }
</script>
