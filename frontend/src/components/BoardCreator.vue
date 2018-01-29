<template>
  <v-parallax src="/static/background.jpg">
    <v-layout column align-center justify-center>
      <h1 class="white--text">Get your task board now!</h1>
      <div class="text-xs-center">
        <v-progress-circular indeterminate v-bind:size="50" color="white" v-if="creatingBoard"></v-progress-circular>

        <v-btn round color="success" dark v-on:click="createBoard" v-if="!creatingBoard">Create</v-btn>
      </div>
    </v-layout>
  </v-parallax>
</template>

<script>
  export default {
    data() {
      return {
        creatingBoard: false
      }
    },

    methods: {
      createBoard() {
        this.creatingBoard = true
        this.$store.dispatch('createBoard').then(() => {
          this.creatingBoard = false
          this.$router.push({name: 'board', params: {pk: this.$store.getters.boardPk}})
        })
      }
    }
  }
</script>
