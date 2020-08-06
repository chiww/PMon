<template>
  <div class="app-container">
    <el-tabs v-model="activeName" style="margin-top:15px;" type="border-card">
      <el-tab-pane v-for="item in tabMapOptions" :key="item.key" :label="item.label" :name="item.key">
        <keep-alive>
          <component :is="activeName" />
        </keep-alive>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import trigger from './components/trigger'
import job from './components/job'
import schedule from './components/schedule'

export default {
  name: 'Jobs',
  components: { trigger, job, schedule },
  filters: {
    statusFilter(status) {
      const statusMap = {
        true: 'success',
        false: 'danger'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      activeName: 'schedule',
      tabMapOptions: [
        { label: '调度器(Schedule)', key: 'schedule' },
        { label: '触发器(Trigger)', key: 'trigger' },
        { label: '本地任务(Job)', key: 'job' }
      ]
    }
  },
  created() {
    // init the default selected tab
    const tab = 'schedule'
    if (tab) {
      this.activeName = tab
    }
  },
  methods: {
  }
}
</script>
