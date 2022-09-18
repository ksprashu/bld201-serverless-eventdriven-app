<template>
  <Suspense>
    <RoundAttempts />
  </Suspense>
</template>

<script>
import { defineComponent } from 'vue'
import RoundAttempts from './RoundAttempts.vue'

export default defineComponent({
  name: 'RoundTab',
  components: {
    RoundAttempts
  }
})
</script>
