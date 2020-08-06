<template>
  <div :class="className" :style="{height:height,width:width}" />
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import resize from './mixins/resize'

import { fetchHisLine } from '../../../../api/dashboard'

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
      default: '350px'
    },
    autoResize: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      chart: null,
      chartData: null
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
        xAxis: {
          data: [],
          boundaryGap: false,
          axisTick: {
            show: false
          }
        },
        grid: {
          left: 10,
          right: 10,
          bottom: 20,
          top: 30,
          containLabel: true
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          },
          padding: [5, 10]
        },
        yAxis: {
          axisTick: {
            show: false
          }
        },
        dataZoom: [
          {
            id: 'dataZoomX',
            type: 'slider',
            xAxisIndex: [0],
            filterMode: 'filter', // 设定为 'filter' 从而 X 的窗口变化会影响 Y 的范围。
            start: 0,
            end: 30
          }
        ],
        legend: {
          data: ['资产IP', '开放IP', '开放端口', '风险端口', '风险服务', '任务失败', '任务成功', '任务总数', '未报备端口']
        },
        series: [{
          name: '资产IP',
          itemStyle: {
            normal: {
              color: '#FF005A',
              lineStyle: {
                color: '#FF005A',
                width: 2
              }
            }
          },
          smooth: true,
          type: 'line',
          data: [],
          animationDuration: 2800,
          animationEasing: 'cubicInOut'
        },
        {
          name: '开放IP',
          smooth: true,
          type: 'line',
          itemStyle: {
            normal: {
              color: '#3888fa',
              lineStyle: {
                color: '#3888fa',
                width: 2
              },
              areaStyle: {
                color: '#f3f8ff'
              }
            }
          },
          data: [],
          animationDuration: 2800,
          animationEasing: 'quadraticOut'
        },
        {
          name: '开放端口',
          smooth: true,
          type: 'line',
          itemStyle: {
            normal: {
              color: '#3888fa',
              lineStyle: {
                color: '#3888fa',
                width: 2
              },
              areaStyle: {
                color: '#f3f8ff'
              }
            }
          },
          data: [],
          animationDuration: 2800,
          animationEasing: 'quadraticOut'
        },
        {
          name: '风险端口',
          smooth: true,
          type: 'line',
          itemStyle: {
            normal: {
              color: '#3888fa',
              lineStyle: {
                color: '#3888fa',
                width: 2
              },
              areaStyle: {
                color: '#f3f8ff'
              }
            }
          },
          data: [],
          animationDuration: 2800,
          animationEasing: 'quadraticOut'
        },
        {
          name: '风险服务',
          smooth: true,
          type: 'line',
          itemStyle: {
            normal: {
              color: '#3888fa',
              lineStyle: {
                color: '#3888fa',
                width: 2
              },
              areaStyle: {
                color: '#f3f8ff'
              }
            }
          },
          data: [],
          animationDuration: 2800,
          animationEasing: 'quadraticOut'
        },
        {
          name: '任务失败',
          smooth: true,
          type: 'line',
          itemStyle: {
            normal: {
              color: '#3888fa',
              lineStyle: {
                color: '#3888fa',
                width: 2
              },
              areaStyle: {
                color: '#f3f8ff'
              }
            }
          },
          data: [],
          animationDuration: 2800,
          animationEasing: 'quadraticOut'
        },
        {
          name: '任务成功',
          smooth: true,
          type: 'line',
          itemStyle: {
            normal: {
              color: '#3888fa',
              lineStyle: {
                color: '#3888fa',
                width: 2
              },
              areaStyle: {
                color: '#f3f8ff'
              }
            }
          },
          data: [],
          animationDuration: 2800,
          animationEasing: 'quadraticOut'
        },
        {
          name: '任务总数',
          smooth: true,
          type: 'line',
          itemStyle: {
            normal: {
              color: '#3888fa',
              lineStyle: {
                color: '#3888fa',
                width: 2
              },
              areaStyle: {
                color: '#f3f8ff'
              }
            }
          },
          data: [],
          animationDuration: 2800,
          animationEasing: 'quadraticOut'
        },
        {
          name: '未报备端口',
          smooth: true,
          type: 'line',
          itemStyle: {
            normal: {
              color: '#3888fa',
              lineStyle: {
                color: '#3888fa',
                width: 2
              },
              areaStyle: {
                color: '#f3f8ff'
              }
            }
          },
          data: [],
          animationDuration: 2800,
          animationEasing: 'quadraticOut'
        }
        ]
      })
      this.chart.showLoading()
    },
    fetchData() {
      this.listLoading = true
      fetchHisLine().then(response => {
        this.chartData = response.data.history
        this.chart.setOption({
          xAxis: {
            data: this.chartData.timestamp
          },
          series: [{
            name: '资产IP',
            data: this.chartData.ipassets
          }, {
            name: '开放IP',
            data: this.chartData.ipset
          }, {
            name: '开放端口',
            data: this.chartData.open_port
          }, {
            name: '风险端口',
            data: this.chartData.risk_port
          }, {
            name: '风险服务',
            data: this.chartData.risk_serv
          }, {
            name: '任务失败',
            data: this.chartData.task_failure
          }, {
            name: '任务成功',
            data: this.chartData.task_success
          }, {
            name: '任务总数',
            data: this.chartData.task_total
          }, {
            name: '未报备端口',
            data: this.chartData.unreported
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
