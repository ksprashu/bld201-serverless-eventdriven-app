<template>
  <q-page class="flex flex-center">
    <LeaderBoard></LeaderBoard>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue'
import LeaderBoard from 'components/LeaderBoard.vue'

export default defineComponent({
  name: 'IndexPage',
  components: {
    LeaderBoard
  }
})
</script>
