<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated  class="bg-primary text-white" height-hint="98">
      <q-toolbar>
        <q-avatar square icon="assessment" font-size="36px">

        </q-avatar>
        <q-toolbar-title>
          Leaderboard App
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'MainLayout'
})
</script>

