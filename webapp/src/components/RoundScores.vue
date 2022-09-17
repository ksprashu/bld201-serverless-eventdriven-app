<template>
  <q-list bordered separator>
    <q-item>
      <q-item-section avatar>
        <q-avatar>
          <img v-bind:alt="username" src="https://cdn.quasar.dev/img/boy-avatar.png">
        </q-avatar>
      </q-item-section>
      <q-item-section>Single line item</q-item-section>
    </q-item>
  </q-list>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'RoundScores'
})
</script>
