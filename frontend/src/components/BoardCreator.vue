<template>
  <v-parallax src="/static/background.jpg">
    <v-layout column align-center justify-center>
      <h1 class="white--text">Get your task board now!</h1>
      <div class="text-xs-center">
        <v-btn round color="success" dark v-on:click="createBoard">Create</v-btn>
      </div>
    </v-layout>
  </v-parallax>
</template>

<script>
  export default {
    methods: {
      createBoard() {
        this.$store.dispatch('createBoard').then(() => {
          this.$router.push({name: 'board', params: {pk: this.$store.getters.boardPk}})
        })
      }
    }
  }
</script>
