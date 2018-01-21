<template>
  <v-container grid-list-md text-xs-center>
    <v-layout row wrap>
      <v-flex xs4>
        <h1>TODO</h1>
        <task-list :tasks="todo" @taskMoved="todoToInProgress"></task-list>
        <form>
          <v-text-field
            v-model="newTaskBody"
          ></v-text-field>
          <v-btn color="success" small dark v-on:click="addTask">Add</v-btn>
        </form>
      </v-flex>
      <v-flex xs4>
        <h1>In Progress</h1>
        <task-list :tasks="inProgress" @taskMoved="inProgressToDone"></task-list>
      </v-flex>
      <v-flex xs4>
        <h1>Done</h1>
        <task-list :tasks="done" @taskMoved="doneToTrash"></task-list>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  import TaskList from './TaskList'

  export default {
    components: {
      TaskList
    },

    data() {
      return {
        newTaskBody: '',
        todo: {
          '3': {
            'body': 'trdddddd'
          }
        },
        inProgress: {
          '9': {
            'body': 'awwweeeeeeee'
          }
        },
        done: {
          '12': {
            'body': 'blablabla'
          }
        }
      }
    },

    methods: {
      addTask() {
        if (this.newTaskBody !== '') {
          let newTaskList = this.copyTasks(this.todo)
          newTaskList[this.newTaskBody] = {body: this.newTaskBody}
          this.todo = newTaskList
        }
        this.newTaskBody = ''
      },

      todoToInProgress({taskPk}) {
        this.moveTask('todo', 'inProgress', taskPk)
      },

      inProgressToDone({taskPk}) {
        this.moveTask('inProgress', 'done', taskPk)
      },

      doneToTrash({taskPk}) {
        let newDone = this.copyTasks(this.done)
        delete newDone[taskPk]
        this.done = newDone
      },

      copyTasks(tasks) {
        let newTaskList = {}
        for (let taskPk in tasks) {
          if (tasks.hasOwnProperty(taskPk)) {
            newTaskList[taskPk] = tasks[taskPk]
          }
        }
        return newTaskList
      },

      moveTask(fromStage, toStage, taskPk) {
        let fromStageTasks = this.copyTasks(this[fromStage])
        let toStageTasks = this.copyTasks(this[toStage])
        toStageTasks[taskPk] = fromStageTasks[taskPk]
        delete fromStageTasks[taskPk]
        this[fromStage] = fromStageTasks
        this[toStage] = toStageTasks
      }
    }

  }
</script>
