<template>
  <div class="q-pa-md" style="max-width: 450px">
    <q-list bordered>
      <q-item>
        <q-item-section>
          <q-item-label header>User</q-item-label>
        </q-item-section>
        <q-item-section></q-item-section>
        <q-item-section></q-item-section>
        <q-item-section>
          <q-item-label header>Average</q-item-label>
        </q-item-section>
        <q-item-section>
          <q-item-label header>Overall</q-item-label>
        </q-item-section>
        <q-item-section>
          <q-item-label header>Streak</q-item-label>
        </q-item-section>
      </q-item>

      <q-item v-for="score in topScores" :key="score.username" class="q-my-sm" clickable v-ripple>
        <q-item-section avatar>
          <q-avatar>
            <img :alt="score.username" :src="score.profile_image_url">
          </q-avatar>
        </q-item-section>

        <q-item-section>
          <q-item-label>{{ score.username }}</q-item-label>
          <q-item-label caption lines="1">{{ score.name }}</q-item-label>
        </q-item-section>

        <q-item-section side>
          <q-chip size="lg" square color="primary" text-color="white">
            {{ score.average_score }}
          </q-chip>
        </q-item-section>
        <q-item-section side>
          <q-chip size="lg" square color="blue" text-color="white">
            {{ score.total_score }}
          </q-chip>
        </q-item-section>
        <q-item-section side>
          <q-chip size="lg" square color="primary" text-color="white">
            {{ score.max_streak }}
          </q-chip>
        </q-item-section>
      </q-item>
    </q-list>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { apiScores } from 'boot/axios'

export default defineComponent({
  name: 'AverageScores',
  data () {
    return {
      topScores: []
    }
  },
  async mounted () {
    const resp = await apiScores.get('/')
    this.topScores = resp.data.data
  }
})
</script>
