<template>
  <div :class="className" :style="{height:height,width:width}" />
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import resize from './mixins/resize'

import { fetchUnreportedPie } from '../../../../api/dashboard'

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
      chart: null
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
          text: '未报备分布',
          left: 'left',
          textStyle: {
            fontSize: 17
          }
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        legend: {
          left: 'center',
          bottom: '10',
          data: []
        },
        series: [
          {
            name: '未报备端口',
            type: 'pie',
            radius: [15, 100],
            center: ['50%', '48%'],
            data: [],
            label: {
              position: 'inside',
              formatter: '{b} \n {d}%'
            },
            animationEasing: 'cubicInOut',
            animationDuration: 2600
          }
        ]
      })
    },
    fetchData() {
      this.listLoading = true
      fetchUnreportedPie().then(response => {
        this.chartData = response.data.unreported_pie
        console.log(this.chartData)
        this.chart.setOption({
          legend: {
            data: this.chartData.legend
          },
          series: [{
            name: '报备状态',
            data: this.chartData.data
          }]
        })
        setTimeout(() => {
          this.listLoading = false
        }, 2.5 * 1000)
      })
    }
  }
}
</script>
