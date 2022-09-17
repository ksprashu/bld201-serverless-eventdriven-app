<template>
  <q-card>
    <q-tabs
      v-model="tab"
      dense
      class="text-grey"
      active-color="primary"
      indicator-color="primary"
      align="justify"
      narrow-indicator
    >
      <q-tab name="overall" label="Top Overall" />
      <q-tab name="average" label="Top Average" />
      <q-tab name="round" label="Per Round Scores" />
    </q-tabs>

    <q-separator />

    <q-tab-panels v-model="tab" animated>
      <q-tab-panel name="overall">
        <OverallTab />
      </q-tab-panel>

      <q-tab-panel name="average">
        <AverageTab />
      </q-tab-panel>

      <q-tab-panel name="round">
        <RoundTab />
      </q-tab-panel>
    </q-tab-panels>
  </q-card>
</template>

<script>
import { defineComponent, ref } from 'vue'
import AverageTab from './AverageTab.vue'
import OverallTab from './OverallTab.vue'
import RoundTab from './RoundTab.vue'

export default defineComponent({
  name: 'LeaderBoard',
  components: {
    AverageTab,
    OverallTab,
    RoundTab
  },
  setup () {
    return {
      tab: ref('overall')
    }
  }
})
</script>
