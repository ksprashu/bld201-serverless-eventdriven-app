<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-toolbar-title class="absolute-center">
          Leaderboard App
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <LeaderBoard></LeaderBoard>
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent } from 'vue'
import LeaderBoard from 'components/LeaderBoard.vue'

export default defineComponent({
  name: 'MainLayout',

  components: {
    LeaderBoard
  }
})
</script>
