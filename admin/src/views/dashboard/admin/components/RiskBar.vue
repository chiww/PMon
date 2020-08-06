<template>
  <div :class="className" :style="{height:height,width:width}" />
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import resize from './mixins/resize'

import { fetchRiskBar } from '../../../../api/dashboard'

const animationDuration = 6000

export default {
  mixins: [resize],
  props: {
    className: {
      type: String,
      default: 'chart'
    },
    width: {
      type: String,
      default: '100%'
    },
    height: {
      type: String,
      default: '300px'
    }
  },
  data() {
    return {
      chart: null,
      barData: null
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart()
    })
  },
  created() {
    this.fetchData()
  },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  },
  methods: {
    initChart() {
      this.chart = echarts.init(this.$el, 'macarons')
      this.chart.setOption({
        title: {
          text: '风险统计',
          left: 'left',
          textStyle: {
            fontSize: 17
          }
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: { // 坐标轴指示器，坐标轴触发有效
            type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
          }
        },
        grid: {
          top: 30,
          left: '2%',
          right: '2%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: [{
          type: 'category',
          data: [],
          axisTick: {
            alignWithLabel: true
          }
        }],
        yAxis: [{
          type: 'value',
          axisTick: {
            show: false
          }
        }],
        series: [{
          name: 'openport',
          type: 'bar',
          stack: 'vistors',
          barWidth: '60%',
          data: [],
          animationDuration
        }, {
          name: 'riskport',
          type: 'bar',
          stack: 'vistors',
          barWidth: '60%',
          data: [],
          animationDuration
        }, {
          name: 'riskservice',
          type: 'bar',
          stack: 'vistors',
          barWidth: '60%',
          data: [],
          animationDuration
        }]
      })
      this.chart.showLoading()
    },
    fetchData() {
      this.listLoading = true
      fetchRiskBar().then(response => {
        this.barData = response.data.risk
        this.chart.setOption({
          xAxis: {
            data: this.barData.date
          },
          series: [{
            name: 'openport',
            data: this.barData.open_port
          }, {
            name: 'riskport',
            data: this.barData.risk_port
          }, {
            name: 'riskservice',
            data: this.barData.risk_serv
          }]
        })
        this.chart.hideLoading()
        setTimeout(() => {
          this.listLoading = false
        }, 2.5 * 1000)
      })
    }
  }
}
</script>
