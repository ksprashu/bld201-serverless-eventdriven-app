<template>
  <div style="max-width: 350px">
    <div class="q-pa-md" style="max-width: 350px">
      <UserScores
        v-for="score in topScores"
        :key="score.userid"
        v-bind="score"/>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import UserScores from './UserScores.vue'

export default defineComponent({
  name: 'OverallTab',
  components: {
    UserScores
  }
})
</script>
