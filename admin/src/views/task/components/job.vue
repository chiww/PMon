<template>
  <div class="app-container">

    <el-table
      v-loading="listLoading"
      :data="jobs"
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
      <el-table-column label="Name" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Function" align="center" width="200">
        <template slot-scope="scope">
          {{ scope.row.func }}
        </template>
      </el-table-column>
      <el-table-column label="Args" align="center" width="400">
        <template slot-scope="scope">
          {{ scope.row.args }}
        </template>
      </el-table-column>
      <!--      <el-table-column label="Kwargs" align="center" width="150">-->
      <!--        <template slot-scope="scope">-->
      <!--          {{ scope.row.kwargs }}-->
      <!--        </template>-->
      <!--      </el-table-column>-->
      <el-table-column label="Remark" align="center">
        <template slot-scope="scope">
          {{ scope.row.remark }}
        </template>
      </el-table-column>
      <el-table-column label="Actions" align="center" width="300" class-name="small-padding fixed-width">
        <template slot="header">
          <el-button class="filter-item" size="mini" type="primary" icon="el-icon-circle-plus-outline" @click="handleJobCreate">
            新增
          </el-button>
        </template>
        <template slot-scope="{row,$index}">
          <el-button type="primary" size="mini" icon="el-icon-edit-outline" @click="handleJobUpdate(row)">编辑</el-button>
          <el-button type="danger" size="mini" icon="el-icon-delete" @click="handleJobDelete(row,$index)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogJobFormVisible" width="35%">
      <el-form ref="dataForm" :model="jobItems" label-position="left" label-width="auto" style="width: 400px; margin-left:50px;">
        <el-form-item label="Name">
          <el-input v-model="jobItems.name" :autosize="{ minRows: 1, maxRows: 1}" type="textarea" placeholder="Please input" />
        </el-form-item>
        <el-form-item label="Function">
          <el-input v-model="jobItems.func" :autosize="{ minRows: 1, maxRows: 1}" type="textarea" placeholder="Please input" />
        </el-form-item>
        <el-form-item label="Args">
          <div class="text item">
            <el-tag
              v-for="tag in jobItems.args"
              :key="tag"
              closable
              :disable-transitions="false"
              @close="handleArgsClose(tag)"
            >
              {{ tag }}
            </el-tag>
            <el-input
              v-if="inputArgsVisible"
              ref="saveArgsTagInput"
              v-model="inputArgsValue"
              class="input-new-tag"
              @keyup.enter.native="handleArgsInputConfirm"
              @blur="handleArgsInputConfirm"
            />
            <el-button v-else class="button-new-tag" icon="el-icon-circle-plus-outline" @click="showArgsInput">新增参数</el-button>
          </div>
        </el-form-item>
        <!--        <el-form-item label="kwargs">-->
        <!--          <el-input v-model="jobItems.kwargs" :autosize="{ minRows: 1, maxRows: 1}" type="textarea" placeholder="Please input" />-->
        <!--        </el-form-item>-->
        <el-form-item label="Remark">
          <el-input v-model="jobItems.remark" :autosize="{ minRows: 1, maxRows: 4}" type="textarea" placeholder="Please input" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogJobFormVisible = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createJobData():updateJobData()">
          Confirm
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { fetchJob, modifyJob, deleteJob } from '@/api/schedule'

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
      listLoading: true,
      inputArgsValue: '',
      inputArgsVisible: false,
      jobItems: {
        uuid: '',
        name: '',
        func: '',
        args: [],
        kwargs: new Map(),
        remark: ''
      },
      dialogJobFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Edit',
        create: 'Create'
      }
    }
  },
  created() {
    this.getJobList()
  },
  methods: {
    getJobList() {
      this.listLoading = true
      fetchJob().then(response => {
        this.jobs = response.data.items
        this.total = response.data.length
      })
      this.listLoading = false
    },
    resetItems() {
      this.jobItems = {
        uuid: '',
        name: '',
        func: '',
        args: [],
        kwargs: new Map(),
        remark: ''
      }
    },
    handleJobCreate() {
      this.resetItems()
      this.dialogStatus = 'create'
      this.dialogJobFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createJobData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          modifyJob(this.jobItems).then(() => {
            this.jobs.push(this.jobItems)
            this.dialogJobFormVisible = false
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
    handleJobUpdate(row) {
      this.jobItems = Object.assign({}, row) // copy obj
      this.dialogStatus = 'update'
      this.dialogJobFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateJobData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.jobItems)
          modifyJob(tempData).then(() => {
            const index = this.jobs.findIndex(v => v.uuid === tempData.uuid)
            this.jobs.splice(index, 1, this.jobItems)
            this.dialogJobFormVisible = false
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
    handleJobDelete(row, index) {
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
    handleArgsClose(tag) {
      this.jobItems.args.splice(this.jobItems.args.indexOf(tag), 1)
    },
    handleArgsInputConfirm() {
      const inputValue = this.inputArgsValue
      if (inputValue) {
        this.jobItems.args.push(inputValue)
      }
      this.inputArgsVisible = false
      this.inputArgsValue = ''
    },
    showArgsInput() {
      this.inputArgsVisible = true
      this.$nextTick(_ => {
        this.$refs.saveArgsTagInput.$refs.input.focus()
      })
    }
  }
}
</script>

<style lang="scss" scoped>
  /*.item {*/
  /*  margin-bottom: 18px;*/
  /*}*/

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
    /*margin-bottom: 10px;*/
  }
  .button-new-tag {
    font-size: x-small;
    margin-left: 10px;
    height: 32px;
    line-height: 30px;
    padding-top: 0;
    padding-bottom: 0;
  }
  .input-new-tag {
    font-size: x-small;
    /*height: 30px;*/
    width: 90px;
    margin-left: 10px;
    vertical-align: bottom;
  }
</style>
