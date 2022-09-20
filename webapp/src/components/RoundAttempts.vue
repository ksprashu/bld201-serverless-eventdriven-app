<template>
  <div class="q-pa-md" style="max-width: 350px">
    <q-list bordered>
      <q-item>
        <q-item-section>
          <q-item-label header>Round</q-item-label>
        </q-item-section>
        <q-item-section>
          <q-item-label header>Statistics</q-item-label>
        </q-item-section>
        <q-item-section></q-item-section>
      </q-item>

      <q-item v-for="attempt in attempts" :key="attempt.roundid" class="q-my-sm" clickable v-ripple>
        <q-item-section avatar>
          <q-avatar text-color="black" size="60px">
            {{ attempt.roundid }}
          </q-avatar>
        </q-item-section>

        <q-item-section>
          <q-chip square color="orange" text-color="white">
            {{ attempt.best_attempt }} attempts
          </q-chip>
          <q-chip square color="cyan" text-color="white">
            {{ attempt.user_count }} users
          </q-chip>
        </q-item-section>
      </q-item>
    </q-list>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { apiAttempts } from 'boot/axios'

export default defineComponent({
  name: 'RoundAttempts',
  data () {
    return {
      attempts: []
    }
  },
  async mounted () {
    const resp = await apiAttempts.get('/')
    this.attempts = resp.data.data
  }
})
</script>
