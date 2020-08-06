<template>
  <div class="dashboard-editor-container">

    <panel-group :panel-data="panelData" />

    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
      <line-chart v-loading="listLoading" :chart-data="lineHistory" />
    </el-row>

    <el-row :gutter="10">
      <el-col :xs="24" :sm="24" :lg="8">
        <div class="chart-wrapper">
          <risk-bar :bar-data="barData" />
        </div>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="8">
        <div class="chart-wrapper">
          <report-status-pie />
        </div>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="8">
        <div class="chart-wrapper">
          <unreported-pie />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import PanelGroup from './components/PanelGroup'
import LineChart from './components/LineChart'

import RiskBar from './components/RiskBar'
import ReportStatusPie from './components/ReportStatusPie'
import UnreportedPie from './components/UnreportedPie'

import { fetchDashboard } from '../../../api/dashboard'

// const riskBarData = {
//   openport: [80, 100, 121, 104, 105, 90, 100],
//   riskport: [120, 82, 91, 154, 162, 140, 130],
//   riskservice: [120, 82, 91, 154, 162, 140, 145]
// }

export default {
  name: 'DashboardAdmin',
  components: {
    ReportStatusPie,
    UnreportedPie,
    RiskBar,
    PanelGroup,
    LineChart
    // TaskTable
  },
  data() {
    return {
      listLoading: true,
      // riskBarData: riskBarData,
      lineHistory: null,
      panelData: null,
      barData: null
    }
  },
  created() {
    this.getData()

    // 异步渲染问题： https://segmentfault.com/q/1010000010376165
    // fetchDashboard().then((res) => {
    //   this.$nextTick(() => {
    //     this.lineHistory = res.data.history
    //     this.panelData = res.data.count
    //     this.barData = res.data.risk
    //   })
    // })
  },
  methods: {
    getData() {
      this.listLoading = true
      fetchDashboard().then(response => {
        this.lineHistory = response.data.history
        this.panelData = response.data.count
        this.barData = response.data.risk
        setTimeout(() => {
          this.listLoading = false
        }, 2.5 * 1000)
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard-editor-container {
  padding: 32px;
  background-color: rgb(240, 242, 245);
  position: relative;

  .chart-wrapper {
    background: #fff;
    padding: 16px 16px 0;
    margin-bottom: 32px;
  }
}

@media (max-width:1024px) {
  .chart-wrapper {
    padding: 8px;
  }
}
</style>
