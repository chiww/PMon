<template>
  <el-row :gutter="20" class="panel-group">
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel">
        <div class="card-panel-icon-wrapper icon-people">
          <svg-icon icon-class="ip" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            开放IP
          </div>
          <span class="card-panel-num"> {{ ipset }} </span>
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            资产IP
          </div>
          <span class="card-panel-num"> {{ ipassets }} </span>
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :lg="10" class="card-panel-col">
      <div class="card-panel">
        <div class="card-panel-icon-wrapper icon-people">
          <svg-icon icon-class="risk" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            未报备
          </div>
          <span class="card-panel-num"> {{ unreported }} </span>
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            高危服务
          </div>
          <span class="card-panel-num"> {{ risk_serv }} </span>
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            高危端口
          </div>
          <span class="card-panel-num"> {{ risk_port }} </span>
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            开放端口
          </div>
          <span class="card-panel-num"> {{ open_port }} </span>
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :lg="8" class="card-panel-col">
      <div class="card-panel">
        <div class="card-panel-icon-wrapper icon-shopping">
          <svg-icon icon-class="task" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            失败数
          </div>
          <span class="card-panel-num"> {{ task_failure }} </span>
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            成功数
          </div>
          <span class="card-panel-num"> {{ task_success }} </span>
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            任务总数
          </div>
          <span class="card-panel-num"> {{ task_total }} </span>
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<script>

import { fetchPanelCount } from '../../../../api/dashboard'

export default {
  data() {
    return {
      panelData: null,
      ipset: 0,
      ipassets: 0,
      unreported: 0,
      risk_serv: 0,
      risk_port: 0,
      open_port: 0,
      task_failure: 0,
      task_success: 0,
      task_total: 0
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.listLoading = true
      fetchPanelCount().then(response => {
        this.panelData = response.data.count
        this.ipassets = this.panelData.ipassets
        this.ipset = this.panelData.ipset
        this.unreported = this.panelData.unreported
        this.open_port = this.panelData.open_port
        this.risk_port = this.panelData.risk_port
        this.risk_serv = this.panelData.risk_serv
        this.task_failure = this.panelData.task_failure
        this.task_success = this.panelData.task_success
        this.task_total = this.panelData.task_total
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.panel-group {
  margin-top: 18px;

  .card-panel-col {
    margin-bottom: 32px;
  }

  .card-panel {
    height: 108px;
    cursor: pointer;
    font-size: 12px;
    position: relative;
    overflow: hidden;
    color: #666;
    background: #fff;
    box-shadow: 4px 4px 40px rgba(0, 0, 0, .05);
    border-color: rgba(0, 0, 0, .05);

    &:hover {
      .card-panel-icon-wrapper {
        color: #fff;
      }

      .icon-people {
        background: #40c9c6;
      }

      .icon-message {
        background: #36a3f7;
      }

      .icon-money {
        background: #f4516c;
      }

      .icon-shopping {
        background: #34bfa3
      }
    }

    .icon-people {
      color: #40c9c6;
    }

    .icon-message {
      color: #36a3f7;
    }

    .icon-money {
      color: #f4516c;
    }

    .icon-shopping {
      color: #34bfa3
    }

    .card-panel-icon-wrapper {
      float: left;
      margin: 14px 0 0 14px;
      padding: 16px;
      transition: all 0.38s ease-out;
      border-radius: 6px;
    }

    .card-panel-icon {
      float: left;
      font-size: 48px;
    }

    .card-panel-description {
      float: right;
      font-weight: bold;
      margin: 26px;
      margin-left: 0px;

      .card-panel-text {
        line-height: 18px;
        color: rgba(0, 0, 0, 0.45);
        font-size: 16px;
        margin-bottom: 12px;
      }

      .card-panel-num {
        font-size: 20px;
      }
    }
  }
}

@media (max-width:550px) {
  .card-panel-description {
    display: none;
  }

  .card-panel-icon-wrapper {
    float: none !important;
    width: 100%;
    height: 100%;
    margin: 0 !important;

    .svg-icon {
      display: block;
      margin: 14px auto !important;
      float: none !important;
    }
  }
}
</style>
