<template>
  <div class="app-container">
    <el-tag :type="info.running | statusFilter" style="margin-right: 10px">APScheduler Running: {{ info.running }}</el-tag>
    <el-button v-if="info.running === false" class="filter-item" size="mini" type="success" icon="el-icon-switch-button" @click="handleStart">
      打开Schedule
    </el-button>
    <el-button v-if="info.running === true" class="filter-item" size="mini" type="danger" icon="el-icon-switch-button" @click="handleShutdown">
      关闭Schedule
    </el-button>
    <el-button v-if="info.running === true" class="filter-item" size="mini" type="warning" icon="el-icon-refresh-right" @click="handleLoadJobs">
      重载已有
    </el-button>
    <el-button class="filter-item" size="mini" type="danger" icon="el-icon-delete" @click="handleRemove">
      删除所有
    </el-button>
    <el-table
      v-loading="listLoading"
      :data="jobs"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
      style="width: 100%; margin-top: 10px;"
      size="mini"
    >
      <el-table-column label="id" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.id }}</span>
        </template>
      </el-table-column>
      <el-table-column label="name" align="center">
        <template slot-scope="scope">
          {{ scope.row.name }}
        </template>
      </el-table-column>
      <el-table-column label="func" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.func }}</span>
        </template>
      </el-table-column>
      <el-table-column label="trigger" align="center" width="100px">
        <template slot-scope="scope">
          <span>{{ scope.row.trigger }}</span>
        </template>
      </el-table-column>
      <el-table-column label="start_date" align="center">
        <template slot-scope="scope">
          {{ scope.row.start_date }}
        </template>
      </el-table-column>
      <el-table-column label="next_run_time" align="center">
        <template slot-scope="scope">
          {{ scope.row.next_run_time }}
        </template>
      </el-table-column>
      <el-table-column label="Actions" align="center" width="300" class-name="small-padding fixed-width">
        <template slot="header">
          <el-button class="filter-item" size="mini" type="primary" icon="el-icon-circle-plus-outline" disabled @click="handleCreate">
            新增任务
          </el-button>
        </template>
        <template slot-scope="{row,$index}">
          <el-button type="info" size="mini" icon="el-icon-info" @click="showDetail(row, $index)">详情</el-button>
          <el-button type="warning" size="mini" icon="el-icon-video-play" @click="handleRunJob(row)">运行</el-button>
          <el-button type="danger" size="mini" icon="el-icon-delete" @click="handleDeleteJob(row,$index)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog title="详情" :visible.sync="dialogDetailVisible">

      <el-form ref="dataForm" :model="detailItem" label-position="left" label-width="150px" style="width: 300px; margin-left:50px;">
        <el-form-item v-for="(value, name) in detailItem" :key="name" :label="name" style="margin: 0; padding: 0">
          <el-input v-model="temp.ip" :autosize="{ minRows: 1, maxRows: 1}" type="textarea" :placeholder="value" :label="name" resize="horizontal" size="mini" style="width: 300px; margin: 0; padding: 0" />
        </el-form-item>
      </el-form>

    </el-dialog>

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :rules="rulesJobForm" :model="temp" label-position="left" label-width="70px" style="width: 400px; margin-left:50px;">
        <el-form-item label="Name">
          <el-input v-model="temp.name" :autosize="{ minRows: 1, maxRows: 4}" type="textarea" placeholder="Please input" />
        </el-form-item>
        <el-form-item label="IP">
          <el-input v-model="temp.ip" :autosize="{ minRows: 1, maxRows: 4}" type="textarea" placeholder="Please input" />
        </el-form-item>
        <el-form-item label="State">
          <el-select v-model="temp.status" class="filter-item" placeholder="Please select">
            <el-option v-for="item in statusOptions" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="Scope">
          <el-select v-model="temp.scope" class="filter-item" placeholder="Please select">
            <el-option v-for="item in scopeTypeOptions" :key="item.key" :label="item.display_name" :value="item.key" />
          </el-select>
        </el-form-item>
        <el-form-item label="Remark">
          <el-input v-model="temp.remark" :autosize="{ minRows: 2, maxRows: 4}" type="textarea" placeholder="Please input" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">
          Confirm
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getJobs, addJob, schedulerInfo, runJob, deleteJob, shutdown, start, loadJobs, removeJobs } from '@/api/scheduler'

const scopeTypeOptions = []

export default {
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
      total: 0,
      jobs: [],
      info: { running: false },
      listLoading: true,
      temp: {
        id: '',
        name: '',
        remark: '',
        ip: '',
        scope: '',
        status: 'disable'
      },
      jobDialogItem: {
        id: '',
        name: '',
        func: '',
        args: '',
        kwargs: {},
        trigger: ''
      },
      dialogFormVisible: false,
      dialogDetailVisible: false,
      detailItem: null,
      dialogStatus: '',
      textMap: {
        update: 'Edit',
        create: 'Create'
      },
      statusOptions: ['disable', 'enable'],
      scopeTypeOptions,
      listQuery: {
        job_id: undefined
      },
      rulesJobForm: {
        name: [{ required: true, message: 'type is required', trigger: 'change' }],
        ip: [{ type: 'date', required: true, message: 'timestamp is required', trigger: 'change' }],
        status: [{ required: true, message: 'source is required', trigger: 'blur' }],
        scope: [{ required: true, message: 'remark is required', trigger: 'blur' }],
        remark: [{ required: true, message: 'status is required', trigger: 'blur' }]
      }
    }
  },
  created() {
    this.getJobList()
    // this.getSchedulerInfo()

    schedulerInfo().then((res) => {
      this.$nextTick(() => {
        this.info = res
      })
    })
  },
  methods: {
    getJobList() {
      this.listLoading = true
      getJobs().then(response => {
        this.jobs = response
        this.total = response.length
      })
      this.listLoading = false
    },
    showDetail(row, index) {
      this.dialogDetailVisible = true
      this.detailItem = this.jobs[index]
    },
    resetTemp() {
      this.temp = {
        id: '',
        name: '',
        remark: '',
        ip: '',
        scope: '',
        status: 'disable'
      }
    },
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          addJob(this.temp).then(() => {
            this.list.unshift(this.temp)
            this.dialogFormVisible = false
            this.$notify({
              title: 'Success',
              message: 'Created Successfully',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row) // copy obj
      this.temp.timestamp = new Date(this.temp.timestamp)
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.timestamp = +new Date(tempData.timestamp) // change Thu Nov 30 2017 16:41:05 GMT+0800 (CST) to 1512031311464
          addJob(tempData).then(() => {
            const index = this.list.findIndex(v => v.id === this.temp.id)
            this.list.splice(index, 1, this.temp)
            this.dialogFormVisible = false
            this.$notify({
              title: 'Success',
              message: 'Update Successfully',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    handleDeleteJob(row, index) {
      deleteJob(row).then(() => {
        this.$notify({
          title: 'Success',
          message: 'Delete Successfully',
          type: 'success',
          duration: 2000
        })
        this.jobs.splice(index, 1)
      })
    },
    // handleModifyStatus(row, status) {
    //   this.$message({
    //     message: '操作Success',
    //     type: 'success',
    //     duration: 2000
    //   })
    //   row.status = status
    // },
    handleRunJob(row) {
      runJob(row).then(() => {
        this.$notify({
          title: 'Success',
          message: 'Run job Successfully',
          type: 'success',
          duration: 2000
        }).catch(err => {
          console.log(err)
        })
      })
    },
    handleLoadJobs(row) {
      loadJobs(row).then(() => {
        this.$notify({
          title: 'Success',
          message: 'Load job Successfully',
          type: 'success',
          duration: 2000
        })
      })
      this.getJobList()
    },
    handleShutdown() {
      shutdown().then(() => {
        this.$notify({
          title: 'Success',
          message: 'Shutdown Successfully',
          type: 'success',
          duration: 2000
        })
        schedulerInfo().then((res) => {
          this.$nextTick(() => {
            this.info = res
          })
        })
      })
    },
    handleStart() {
      start().then(() => {
        this.$notify({
          title: 'Success',
          message: 'Start Successfully',
          type: 'success',
          duration: 2000
        })
        schedulerInfo().then((res) => {
          this.$nextTick(() => {
            this.info = res
          })
        })
      })
    },
    handleRemove(row) {
      removeJobs(row).then(() => {
        this.$notify({
          title: 'Success',
          message: 'Remove job Successfully',
          type: 'success',
          duration: 2000
        })
      })
      this.getJobList()
    }
  }
}
</script>
