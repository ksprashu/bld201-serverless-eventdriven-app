<template>
  <Suspense>
    <AverageScores />
  </Suspense>
</template>

<script>
import { defineComponent } from 'vue'
import AverageScores from './AverageScores.vue'

export default defineComponent({
  name: 'AverageTab',
  components: {
    AverageScores
  }
})
</script>
