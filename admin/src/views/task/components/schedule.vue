<template>
  <div class="app-container">
    <el-table
      v-loading="listLoading"
      :data="schedules"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
      style="width: 100%"
      size="mini"
    >
      <el-table-column label="UUID" align="center" width="270">
        <template slot-scope="scope">
          <span>{{ scope.row.uuid }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Name" align="center" width="300">
        <template slot-scope="scope">
          <span>{{ scope.row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Job" align="center" width="300">
        <template slot-scope="scope">
          {{ scope.row.job_name }}
        </template>
      </el-table-column>
      <el-table-column label="Trigger" align="center" width="150">
        <template slot-scope="scope">
          {{ scope.row.trigger_name }}
        </template>
      </el-table-column>
      <el-table-column label="Remark" align="center" width="150">
        <template slot-scope="scope">
          {{ scope.row.remark }}
        </template>
      </el-table-column>
      <el-table-column label="Status" align="center" width="150">
        <template slot-scope="scope">
          <el-tag :type="scope.row.status | statusFilter">{{ scope.row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="Actions" align="center" width="300" class-name="small-padding fixed-width">
        <template slot="header">
          <el-button class="filter-item" size="mini" type="primary" icon="el-icon-circle-plus-outline" @click="handleScheduleCreate">
            新增
          </el-button>
        </template>
        <template slot-scope="{row,$index}">
          <el-button type="primary" size="mini" icon="el-icon-edit-outline" @click="handleScheduleUpdate(row)">编辑</el-button>
          <el-button v-if="row.status === 'UNLOADED'" type="success" size="mini" icon="el-icon-video-play" @click="handleScheduleLoad(row)">加载</el-button>
          <el-button v-if="row.status === 'LOADED'" type="warning" size="mini" icon="el-icon-video-pause" @click="handleScheduleUnload(row)">卸载</el-button>
          <el-button type="danger" size="mini" icon="el-icon-delete" @click="handleScheduleDelete(row,$index)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogScheduleFormVisible" width="35%">
      <el-form ref="dataForm" :model="scheduleItems" label-position="left" label-width="auto">
        <el-form-item label="UUID">
          <el-input v-model="scheduleItems.uuid" :autosize="{ minRows: 1, maxRows: 1}" disabled type="textarea" placeholder="Please input" />
        </el-form-item>
        <el-form-item label="Name">
          <el-input v-model="scheduleItems.name" :autosize="{ minRows: 1, maxRows: 1}" disabled type="textarea" placeholder="Please input" />
        </el-form-item>
        <el-form-item label="Trigger">
          <el-select v-model="scheduleItems.trigger_name" class="filter-item" placeholder="Please select">
            <el-option v-for="item in triggerOptions" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="Job">
          <el-select v-model="scheduleItems.job_name" class="filter-item" placeholder="Please select">
            <el-option v-for="item in jobOptions" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="Remark">
          <el-input v-model="scheduleItems.remark" :autosize="{ minRows: 1, maxRows: 2}" type="textarea" placeholder="Please input" />
        </el-form-item>
        <!--        <el-form-item label="Status">-->
        <!--          <el-select v-model="scheduleItems.status" class="filter-item" placeholder="Please select">-->
        <!--            <el-option v-for="item in statusOptions" :key="item" :label="item" :value="item" />-->
        <!--          </el-select>-->
        <!--        </el-form-item>-->
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogScheduleFormVisible = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createScheduleData():updateScheduleData()">
          Confirm
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { fetchSchedule, modifySchedule, deleteSchedule } from '@/api/schedule'
import { loadJob, unloadJob } from '@/api/scheduler'

export default {
  name: 'Schedule',
  filters: {
    statusFilter(status) {
      const statusMap = {
        LOADED: 'success',
        UNLOADED: 'danger'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      total: 0,
      schedules: [],
      listLoading: true,
      // statusOptions: ['disable', 'enable'],
      scheduleItems: {
        uuid: '',
        name: '',
        trigger_name: '',
        job_name: '',
        status: ''
      },
      schedTypeOptions: ['job', 'task'],
      schedNameOptions: [],
      triggerOptions: [],
      jobOptions: [],
      taskOptions: [],
      dialogScheduleFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Edit',
        create: 'Create'
      }
    }
  },
  created() {
    this.getScheduleList()
    this.optionsList()
  },
  methods: {
    getScheduleList() {
      this.listLoading = true
      fetchSchedule().then(response => {
        this.schedules = response.data.items
        this.total = response.data.length
      })
      this.listLoading = false
    },
    optionsList() {
      fetchSchedule({ action: 'options' }).then(response => {
        this.triggerOptions = response.data.trigger
        this.jobOptions = response.data.job
      })
    },
    resetItems() {
      this.scheduleItems = {
        uuid: undefined,
        name: undefined,
        trigger_name: '',
        job_name: '',
        status: 'UNLOADED'
      }
    },
    handleScheduleCreate() {
      this.resetItems()
      this.dialogStatus = 'create'
      this.dialogScheduleFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createScheduleData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          modifySchedule(this.scheduleItems).then(() => {
            this.schedules.push(this.scheduleItems)
            this.dialogScheduleFormVisible = false
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
    handleScheduleUpdate(row) {
      this.scheduleItems = Object.assign({}, row) // copy obj
      this.dialogStatus = 'update'
      this.dialogScheduleFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateScheduleData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.scheduleItems)
          modifySchedule(tempData).then(() => {
            const index = this.schedules.findIndex(v => v.uuid === tempData.uuid)
            this.schedules.splice(index, 1, this.scheduleItems)
            this.dialogScheduleFormVisible = false
            this.$notify({
              title: 'Success',
              message: 'Update Successfully',
              type: 'success',
              duration: 2000
            })
            this.getScheduleList()
          })
        }
      })
    },
    handleScheduleDelete(row, index) {
      deleteSchedule(row).then(() => {
        this.$notify({
          title: 'Success',
          message: 'Delete Successfully',
          type: 'success',
          duration: 2000
        })
        this.schedules.splice(index, 1)
      })
    },
    handleScheduleLoad(row) {
      loadJob(row).then((response) => {
        this.$notify({
          title: response.title,
          message: response.message,
          type: response.type,
          duration: 2000
        })
        row.status = 'LOADED'
      }).catch(err => {
        console.log('tttt' + err)
      })
    },
    handleScheduleUnload(row) {
      unloadJob(row).then((response) => {
        this.$notify({
          title: response.title,
          message: response.message,
          type: response.type,
          duration: 2000
        })
        row.status = 'UNLOADED'
      })
    }
  }
}
</script>

