<template>
  <div class="app-container">
    <el-table
      v-loading="listLoading"
      :data="list"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
      style="width: 100%"
      size="mini"
    >
      <el-table-column align="center" label="UUID">
        <template slot-scope="scope">
          {{ scope.row.uuid }}
        </template>
      </el-table-column>
      <el-table-column label="Name" align="center">
        <template slot-scope="scope">
          {{ scope.row.name }}
        </template>
      </el-table-column>
      <el-table-column label="Api" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.api }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Scope" align="center">
        <template slot-scope="scope">
          {{ scope.row.scope }}
        </template>
      </el-table-column>
      <el-table-column class-name="status-col" label="Status" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.status | statusFilter">{{ scope.row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="Actions" align="center" width="210" class-name="small-padding fixed-width">
        <template slot="header">
          <el-button class="filter-item" size="mini" type="primary" icon="el-icon-circle-plus-outline" @click="handleCreate">
            新增节点
          </el-button>
        </template>
        <template slot-scope="{row,$index}">
          <el-button type="primary" size="mini" icon="el-icon-edit-outline" @click="handleUpdate(row)">编辑</el-button>
          <el-button size="mini" type="danger" icon="el-icon-delete" @click="handleDelete(row,$index)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible" width="35%">
      <el-form ref="dataForm" :rules="rulesNodeForm" :model="temp" label-position="left" label-width="auto">
        <el-form-item label="Name">
          <el-input v-model="temp.name" :autosize="{ minRows: 1, maxRows: 4}" type="textarea" placeholder="Please input" />
        </el-form-item>
        <el-form-item label="Api">
          <el-input v-model="temp.api" :autosize="{ minRows: 1, maxRows: 4}" type="textarea" placeholder="Please input" />
        </el-form-item>
        <el-form-item label="State">
          <el-select v-model="temp.status" class="filter-item" placeholder="Please select">
            <el-option v-for="item in statusOptions" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="Scope">
          <el-checkbox-group v-model="temp.scope" size="mini">
            <el-checkbox-button v-for="item in scopeOptions" :key="item" :label="item"> {{ item }} </el-checkbox-button>
          </el-checkbox-group>
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
import { fetchNode, modifyNode, deleteNode } from '@/api/node'

export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        enable: 'success',
        disable: 'danger'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      total: 0,
      list: null,
      listLoading: true,
      temp: {
        uuid: '',
        name: '',
        remark: '',
        api: '',
        scope: [],
        status: 'disable'
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Edit',
        create: 'Create'
      },
      statusOptions: ['disable', 'enable'],
      scopeOptions: ['10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16', '100.64.0.0/16', '0.0.0.0/0'],
      listQuery: {
        page: 1,
        limit: 20,
        api: undefined,
        name: undefined,
        uuid: undefined,
        scope: undefined
      },
      rulesNodeForm: {
        name: [{ required: true, message: 'type is required', trigger: 'change' }],
        status: [{ required: true, message: 'source is required', trigger: 'blur' }],
        scope: [{ required: true, message: 'remark is required', trigger: 'blur' }],
        remark: [{ required: true, message: 'status is required', trigger: 'blur' }]
      }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      fetchNode(this.listQuery).then(response => {
        this.list = response.data.items
        this.total = response.data.total
      })
      this.listLoading = false
    },
    resetTemp() {
      this.temp = {
        uuid: '',
        name: '',
        remark: '',
        api: '',
        scope: [],
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
          modifyNode(this.temp).then(() => {
            this.list.push(this.temp)
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
          modifyNode(tempData).then(() => {
            const index = this.list.findIndex(v => v.name === this.temp.name)
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
    handleDelete(row, index) {
      deleteNode(row).then(response => {
        if (response.code === 20000) {
          this.$notify({
            title: 'Success',
            message: 'Delete Successfully',
            type: 'success',
            duration: 2000
          })
          this.list.splice(index, 1)
        }
      })
    },
    handleModifyStatus(row, status) {
      this.$message({
        message: '操作Success',
        type: 'success'
      })
      row.status = status
    }
  }
}
</script>
