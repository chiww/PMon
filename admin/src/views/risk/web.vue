<template>
  <div class="app-container">
    <div class="filter-container" style="margin-bottom: 10px">
      <el-row class="tables-search" style="width: 100%">
        <el-col :span="24">
          <div>
            <el-input v-model="listQuery.url" placeholder="URL" style="width: 130px;" class="filter-item" size="mini" @keyup.enter.native="handleFilter" />
            <el-select v-model="listQuery.code" placeholder="响应码" clearable style="width: 140px" size="mini" class="filter-item">
              <el-option v-for="item in codeOptions" :key="item" :label="item" :value="item" />
            </el-select>
            <el-select v-model="listQuery.tag" placeholder="标签" clearable style="width: 140px" size="mini" class="filter-item">
              <el-option v-for="item in tagOptions" :key="item" :label="item" :value="item" />
            </el-select>
            <el-select v-model="listQuery.status" placeholder="状态" clearable style="width: 140px" size="mini" class="filter-item">
              <el-option v-for="item in statusOptions" :key="item" :label="item" :value="item" />
            </el-select>
            <el-date-picker
              v-model="listQuery.create_range"
              type="daterange"
              align="right"
              unlink-panels
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              size="mini"
              value-format="timestamp"
              :picker-options="pickerDiscoverRangeOptions"
            />
            <el-button v-waves class="filter-item" type="primary" size="mini" icon="el-icon-search" @click="handleFilter">
              Search
            </el-button>
          </div>
        </el-col>
      </el-row>
      <el-row class="tables-filter" style="margin: 10px" size="mini">
        <el-col :span="24">
          <el-checkbox v-model="showSysCode" class="filter-item" size="mini" @change="showSysCode = !showSysCode">
            系统编码
          </el-checkbox>
          <el-checkbox v-model="showBusiness" class="filter-item" size="mini" @change="showBusiness = !showBusiness">
            业务部门
          </el-checkbox>
          <el-checkbox v-model="showOwner" class="filter-item" size="mini" @change="showOwner = !showOwner">
            负责人
          </el-checkbox>
          <el-checkbox v-model="showUpdateTime" class="filter-item" size="mini" @change="showUpdateTime = !showUpdateTime">
            更新时间
          </el-checkbox>
          <el-checkbox v-model="showHeaders" class="filter-item" size="mini" @change="showHeaders = !showHeaders">
            Headers
          </el-checkbox>
          <el-checkbox v-model="showContent" class="filter-item" size="mini" @change="showContent = !showContent">
            Content
          </el-checkbox>
        </el-col>
      </el-row>
    </div>

    <el-table
      ref="filterTable"
      v-loading="listLoading"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;"
      size="mini"
      @sort-change="sortChange"
    >
      <el-table-column label="URL" prop="ip" min-width="200" align="center">
        <template slot-scope="{row}">
          <span>{{ row.url }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Tag" min-width="80" align="center">
        <template slot-scope="{row}">
          <span>{{ row.tag }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Title" min-width="400" align="center">
        <template slot-scope="{row}">
          <span>{{ row.title }}</span>
        </template>
      </el-table-column>
      <el-table-column v-if="showSysCode === true" label="SysCode" min-width="150px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.assets.sys_code }}</span>
        </template>
      </el-table-column>
      <el-table-column v-if="showBusiness === true" label="Business" min-width="150px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.assets.business }}</span>
        </template>
      </el-table-column>
      <el-table-column v-if="showOwner === true" label="Owner" min-width="150px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.assets.owner }}</span>
        </template>
      </el-table-column>
      <el-table-column v-if="showHeaders === true" label="Headers" min-width="300" align="center">
        <template slot-scope="{row}">
          <ul>
            <li v-for="(value, key) in row.headers" :key="key" style="text-align: left; margin: 0; padding: 0">
              <span> {{ key }}:</span>
              <span style="color: blue">{{ value }}</span>
            </li>
          </ul>
        </template>
      </el-table-column>
      <el-table-column v-if="showContent === true" label="Content" min-width="300" align="center">
        <template slot-scope="{row}">
          <span>{{ row.content }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Code" min-width="60" align="center">
        <template slot-scope="{row}">
          <span>{{ row.code }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Status" min-width="120" align="center">
        <template slot-scope="{row}">
          <span>{{ row.status }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Message" min-width="120" align="center">
        <template slot-scope="{row}">
          <span>{{ row.message }}</span>
        </template>
      </el-table-column>
      <el-table-column label="CreateTime" min-width="150" align="center">
        <template slot-scope="{row}">
          <span>{{ row.create_time | handleTime('{y}-{m}-{d} {h}:{i}') }}</span>
        </template>
      </el-table-column>
      <el-table-column v-if="showUpdateTime === true" label="UpdateTime" min-width="150" align="center">
        <template slot-scope="{row}">
          <span>{{ row.timestamp | handleTime('{y}-{m}-{d} {h}:{i}') }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="工单状态"
        align="center"
        width="200"
        class-name="small-padding fixed-width"
        :filters="[{ text: 'REPORTED', value: 'REPORTED' }, { text: 'UNREPORTED', value: 'UNREPORTED' }]"
        :filter-method="filterStatus"
      >
        <template slot-scope="{row}">
          <el-tag :type="row.ticket_info.status | statusFilter">
            <span class="link-type">{{ row.ticket_info.status }}</span>
          </el-tag>
          <el-tag>{{ row.ticket_info.source }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="Actions" align="center" min-width="200" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <el-button v-if="row.ticket_info.status !== 'reported'" size="mini" type="warning" icon="el-icon-circle-check" @click="handleUpdateTicket(row)">
            加白
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

    <el-dialog title="工单详情" :visible.sync="dialogTicketFormVisible" min-width="35%">
      <el-form ref="dataTicketForm" :rules="rulesTicketForm" :model="tempTicket" label-position="left" label-width="auto">
        <el-form-item label="url" prop="ip">
          <el-input v-model="tempTicket.url" disabled />
        </el-form-item>
        <el-form-item label="ticket_id" prop="ticket_id">
          <el-input v-model="tempTicket.ticket_id" />
        </el-form-item>
        <el-form-item label="owner" prop="owner">
          <el-input v-model="tempTicket.owner" />
        </el-form-item>
        <el-form-item label="Source" prop="source">
          <el-select v-model="tempTicket.source" class="filter-item" placeholder="Please select">
            <el-option v-for="item in typeTicketOptions" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="Date" prop="create_time">
          <el-date-picker
            v-model="tempTicket.create_time"
            type="datetime"
            placeholder="选择日期时间"
            value-format="timestamp"
          />
        </el-form-item>
        <el-form-item label="Status" prop="status">
          <el-select v-model="tempTicket.status" class="filter-item" placeholder="Please select">
            <el-option v-for="item in ticketStatusOptions" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="Remark" prop="remark">
          <el-input v-model="tempTicket.remark" :autosize="{ minRows: 2, maxRows: 4}" type="textarea" placeholder="Please input" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogTicketFormVisible = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="updateTicketData()">
          Confirm
        </el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>
import { fetchWebList } from '@/api/web'
import { updateTicket } from '@/api/ticket'
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination

export default {
  name: 'PortIndex',
  components: { Pagination },
  directives: { waves },
  filters: {
    statusFilter(status) {
      const statusMap = {
        REPORTED: 'success',
        UNREPORTED: 'danger'
      }
      return statusMap[status]
    },
    handleTime(timestamp) {
      return parseTime(timestamp)
    }
  },
  data() {
    return {
      list: null,
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        url: undefined,
        code: undefined,
        status: undefined,
        tag: 'Web',
        create_range: undefined
      },
      codeOptions: [],
      statusOptions: [],
      tagOptions: [],
      showOwner: false,
      showBusiness: false,
      showSysCode: false,
      showHeaders: false,
      showContent: false,
      showUpdateTime: false,
      tempTicket: {
        url: undefined,
        ticket_id: undefined,
        owner: '',
        remark: '',
        create_time: undefined,
        source: '',
        status: undefined
      },
      typeTicketOptions: ['ByHandle', 'ECP', 'ITSM', 'OTHER'],
      rulesTicketForm: {
        ticket_id: [{ required: true, message: 'type is required', trigger: 'change' }],
        create_time: [{ type: 'date', required: true, message: 'timestamp is required', trigger: 'blur' }],
        source: [{ required: true, message: 'source is required', trigger: 'blur' }],
        remark: [{ required: true, message: 'remark is required', trigger: 'blur' }],
        status: [{ required: true, message: 'status is required', trigger: 'blur' }]
      },
      dialogTicketFormVisible: false,
      ticketStatusOptions: ['REPORTED', 'UNREPORTED'],
      pickerDiscoverRangeOptions: {
        shortcuts: [{
          text: '最近一周',
          onClick(picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '最近一个月',
          onClick(picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '最近三个月',
          onClick(picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
            picker.$emit('pick', [start, end])
          }
        }]
      }
    }
  },
  created() {
    this.getList()
    this.optionsList()
  },
  methods: {
    getList() {
      this.listLoading = true
      fetchWebList(this.listQuery).then(response => {
        this.list = response.data.items
        this.total = response.data.total
      })
      this.listLoading = false
    },
    optionsList() {
      fetchWebList({ action: 'options' }).then(response => {
        this.codeOptions = response.data.code
        this.statusOptions = response.data.status
        this.tagOptions = response.data.tag
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    sortChange(data) {
      const { prop, order } = data
      if (prop === 'task_id') {
        this.sortByID(order)
      }
    },
    sortByID(order) {
      if (order === 'ascending') {
        this.listQuery.sort = '+id'
      } else {
        this.listQuery.sort = '-id'
      }
      this.handleFilter()
    },
    handleDelete(row, index) {
      this.$notify({
        title: 'Success',
        message: 'Delete Successfully',
        type: 'success',
        duration: 2000
      })
      this.list.splice(index, 1)
    },
    handleUpdateTicket(row) {
      this.tempTicket = Object.assign({}, row.ticket_info) // copy obj
      this.tempTicket.url = row.url
      this.dialogTicketFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataTicketForm'].clearValidate()
      })
    },
    updateTicketData() {
      this.$refs['dataTicketForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign(this.tempTicket)
          updateTicket(tempData).then(() => {
            this.dialogTicketFormVisible = false
            this.$notify({
              title: 'Success',
              message: 'Update Successfully',
              type: 'success',
              duration: 2000
            })
            this.getList()
          })
        }
      })
    },
    filterStatus(value, row) {
      return row.ticket_info.status === value
    }
  }
}
</script>

<style>
  .el-table .warning-row {
    background: oldlace;
  }

  .el-table .success-row {
    background: #f0f9eb;
  }
</style>
