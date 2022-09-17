<template>
  <div style="max-width: 350px">
    <div class="q-pa-md" style="max-width: 350px">
      <RoundScores
        v-for="score in roundScores"
        :key="score.userid"
        v-bind="score"/>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'RoundTab'
})
</script>
