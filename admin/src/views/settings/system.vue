<template>
  <div class="dashboard-editor-container">

    <el-row>
      <el-col :span="24">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>高危端口</span>
            <el-button style="float: right;" size="mini" type="primary" icon="el-icon-upload2" @click="handleRiskPortUpdate">更新</el-button>
          </div>
          <div class="text item">
            <el-tag
              v-for="tag in riskPort"
              :key="tag"
              closable
              :disable-transitions="false"
              @close="handleRiskPortClose(tag)"
            >
              {{ tag }}
            </el-tag>
            <el-input
              v-if="inputRiskPortVisible"
              ref="saveRiskPortTagInput"
              v-model="inputRiskPortValue"
              class="input-new-tag"
              @keyup.enter.native="handleRiskPortInputConfirm"
              @blur="handleRiskPortInputConfirm"
            />
            <el-button v-else class="button-new-tag" icon="el-icon-circle-plus-outline" @click="showRiskPortInput">新增端口</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row>
      <el-col :span="24">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>高危服务</span>
            <el-button style="float: right;" size="mini" type="primary" icon="el-icon-upload2" @click="handleRiskServUpdate">更新</el-button>
          </div>
          <div class="text item">
            <el-tag
              v-for="tag in riskServ"
              :key="tag"
              closable
              :disable-transitions="false"
              @close="handleRiskServClose(tag)"
            >
              {{ tag }}
            </el-tag>
            <el-input
              v-if="inputRiskServVisible"
              ref="saveRiskServTagInput"
              v-model="inputRiskServValue"
              class="input-new-tag"
              @keyup.enter.native="handleRiskServInputConfirm"
              @blur="handleRiskServInputConfirm"
            />
            <el-button v-else class="button-new-tag" icon="el-icon-circle-plus-outline" @click="showRiskServInput">新增服务</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { fetchSettings, updateSettings } from '@/api/settings'

export default {
  name: 'Settings',
  data() {
    return {
      riskPort: [],
      inputRiskPortVisible: false,
      inputRiskPortValue: '',
      riskServ: [],
      inputRiskServVisible: false,
      inputRiskServValue: ''
    }
  },
  computed: {
  },
  created() {
    this.getSettings()
  },
  methods: {
    getSettings() {
      fetchSettings().then(response => {
        const items = response.data.items
        for (let i = 0; i < items.length; i++) {
          if (items[i].name === 'risk_port') {
            this.riskPort = items[i].value
          }
          if (items[i].name === 'risk_serv') {
            this.riskServ = items[i].value
          }
        }
      })
    },
    handleRiskPortClose(tag) {
      this.riskPort.splice(this.riskPort.indexOf(tag), 1)
    },
    showRiskPortInput() {
      this.inputRiskPortVisible = true
      this.$nextTick(_ => {
        this.$refs.saveRiskPortTagInput.$refs.input.focus()
      })
    },
    handleRiskPortInputConfirm() {
      const inputValue = this.inputRiskPortValue
      if (inputValue) {
        this.riskPort.push(inputValue)
      }
      this.inputRiskPortVisible = false
      this.inputRiskPortValue = ''
    },
    handleRiskPortUpdate() {
      updateSettings({ name: 'risk_port', value: this.riskPort }).then(response => {
        if (response.code === 20000) {
          this.$notify({
            title: 'Success',
            message: 'Delete Successfully',
            type: 'success',
            duration: 2000
          })
        }
      })
    },
    // this is risk service
    handleRiskServClose(tag) {
      this.riskServ.splice(this.riskServ.indexOf(tag), 1)
    },
    showRiskServInput() {
      this.inputRiskServVisible = true
      this.$nextTick(_ => {
        this.$refs.saveRiskServTagInput.$refs.input.focus()
      })
    },
    handleRiskServInputConfirm() {
      const inputValue = this.inputRiskServValue
      if (inputValue) {
        this.riskServ.push(inputValue)
      }
      this.inputRiskServVisible = false
      this.inputRiskServValue = ''
    },
    handleRiskServUpdate() {
      updateSettings({ name: 'risk_serv', value: this.riskServ }).then(response => {
        if (response.code === 20000) {
          this.$notify({
            title: 'Success',
            message: 'Delete Successfully',
            type: 'success',
            duration: 2000
          })
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
  .text {
    font-size: 14px;
  }

  .item {
    margin-bottom: 18px;
  }

  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }
  .clearfix:after {
    clear: both
  }

  .box-card {
    width: 100%;
  }
  .el-tag + .el-tag {
    margin-left: 10px;
    margin-bottom: 10px;
  }
  .button-new-tag {
    margin-left: 10px;
    height: 32px;
    line-height: 30px;
    padding-top: 0;
    padding-bottom: 0;
  }
  .input-new-tag {
    width: 90px;
    margin-left: 10px;
    vertical-align: bottom;
  }
</style>
