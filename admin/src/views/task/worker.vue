<template>
  <div class="app-container">
    <div class="filter-container" style="margin-bottom: 10px">
      <el-input v-model="listQuery.task_id" placeholder="任务ID" clearable size="mini" style="width: 180px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-input v-model="listQuery.address" placeholder="目标地址" clearable size="mini" style="width: 180px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-select v-model="listQuery.node" placeholder="节点名" clearable size="mini" style="width: 90px" class="filter-item">
        <el-option v-for="item in nodeOptions" :key="item" :label="item" :value="item" />
      </el-select>
      <el-select v-model="listQuery.state" placeholder="任务状态" clearable size="mini" class="filter-item" style="width: 120px">
        <el-option v-for="item in stateOptions" :key="item" :label="item" :value="item" />
      </el-select>
      <el-select v-model="listQuery.tag" placeholder="任务标签" clearable size="mini" class="filter-item" style="width: 120px">
        <el-option v-for="item in tagOptions" :key="item" :label="item" :value="item" />
      </el-select>
      <el-date-picker
        v-model="listQuery.start_range"
        type="daterange"
        align="right"
        unlink-panels
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        size="mini"
        value-format="timestamp"
        :picker-options="pickerStartRangeOptions"
      />
      <el-button v-waves class="filter-item" type="primary" size="mini" icon="el-icon-search" @click="handleFilter">
        Search
      </el-button>
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;"
      :default-sort="{prop: 'date_start', order: 'descending'}"
      size="mini"
    >
      <!--      @sort-change="sortChange"-->
      <el-table-column label="任务名称" prop="name" sortable min-width="350px" align="center">
        <template slot-scope="scope">
          <span class="link-type">{{ scope.row.param.name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="任务工具" prop="tool" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.param.tool }}</span>
        </template>
      </el-table-column>
      <el-table-column label="任务目标" prop="target" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.param.address }}</span>
        </template>
      </el-table-column>
      <el-table-column label="任务参数" prop="options" min-width="250" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.param.options }}</span>
        </template>
      </el-table-column>

      <el-table-column label="任务标签" min-width="100px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.param.tag }}</span>
        </template>
      </el-table-column>
      <el-table-column label="开始时间" prop="started" sortable min-width="210px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.started | handleTime }}</span>
        </template>
      </el-table-column>
      <el-table-column label="结束时间" prop="succeeded" sortable min-width="210px" align="center">
        <template slot-scope="scope">
          <span v-if="scope.row.state === 'SUCCESS' ">{{ scope.row.succeeded | handleTime }}</span>
        </template>
      </el-table-column>
      <el-table-column label="节点名称" min-width="100px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.node.name }}</span>
        </template>
      </el-table-column>

      <el-table-column label="任务状态" class-name="status-col" align="center" min-width="120">
        <template slot-scope="scope">
          <el-tag :type="scope.row.state | statusFilter" @click="openStatusMessage(scope.row)">
            {{ scope.row.state }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="Actions" align="center" min-width="200" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button v-if="scope.row.state!=='SUCCESS'" size="mini" disabled type="success" icon="el-icon-video-pause" @click="handlePause(scope.row)">
            暂停
          </el-button>
          <el-button v-if="scope.row.state!=='SUCCESS'" size="mini" disabled icon="el-icon-delete" @click="handleStop(scope.row)">
            终止
          </el-button>
          <el-button v-if="scope.row.state==='SUCCESS'" size="mini" type="success" icon="el-icon-info" @click="handleFetchResult(scope.row)">
            详情
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

    <el-dialog :visible.sync="dialogResultVisible" title="任务执行结果">
      <el-table v-if="portResultTable.includes(resultTag)" ref="filterResult" :data="resultData" border fit highlight-current-row size="mini">
        <el-table-column label="IPAddress" prop="address" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.address }}</span>
          </template>
        </el-table-column>
        <el-table-column v-if="resultTag === 'HOST_DISC'" label="Status" prop="status" align="center" :filters="[{text: 'up', value: 'up'}, {text: 'down', value: 'down'}]" :filter-method="filterResultHandler">
          <template slot-scope="scope">
            <span>{{ scope.row.status }}</span>
          </template>
        </el-table-column>
        <el-table-column v-if="['PORT_DISC','PORT_CHEK', 'PORT_RISK'].indexOf(resultTag) >= 0" label="Open" prop="open" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.open.join(",") }}</span>
          </template>
        </el-table-column>
        <el-table-column v-if="['PORT_DISC','PORT_CHEK', 'PORT_RISK'].indexOf(resultTag) >= 0" label="Close" prop="close" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.close.join(",") }}</span>
          </template>
        </el-table-column>
        <el-table-column v-if="resultTag === 'PORT_INFO'" label="Service" prop="service" align="center" min-width="450px">
          <template slot-scope="scope">
            <ul v-for="item in scope.row.service" :key="item">
              <li v-for="(value, key) in item" :key="key" style="text-align: left; margin: 0; padding: 0">
                <span> {{ key }}:</span> <br v-if="key === 'servicefp'">
                <span v-if="key === 'update_time'" style="color: blue"> {{ value | handleTime('{y}-{m}-{d} {h}:{i}') }}</span>
                <span v-else style="color: blue">{{ value }}</span>
              </li>
            </ul>
          </template>
        </el-table-column>
      </el-table>

      <el-table v-if="webcheckResultTable.includes(resultTag)" ref="filterResult" :data="resultData" border fit highlight-current-row size="mini">
        <el-table-column label="URL" prop="url" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.url }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Status" prop="status" align="center" :filters="[{text: 'ACCESSIBLE', value: 'ACCESSIBLE'}, {text: 'INACCESSIBLE', value: 'INACCESSIBLE'}]" :filter-method="filterResultHandler">
          <template slot-scope="scope">
            <span>{{ scope.row.status }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Code" prop="open" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.code }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Headers" prop="close" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.headers }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Title" prop="close" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.title }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Tag" prop="close" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.tag }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Update" prop="close" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.timestamp | handleTime('{y}-{m}-{d} {h}:{i}') }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Message" prop="close" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.message }}</span>
          </template>
        </el-table-column>
      </el-table>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogResultVisible = false">Confirm</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { fetchList } from '@/api/task'
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination

export default {
  name: 'ComplexTable',
  components: { Pagination },
  directives: { waves },
  filters: {
    statusFilter(status) {
      const statusMap = {
        SUCCESS: 'success',
        STARTED: 'info',
        ISSUED: 'info',
        FAILURE: 'danger',
        PENDING: 'info'
      }
      return statusMap[status]
    },
    handleTime(timestamp) {
      return parseTime(timestamp)
    }
  },
  data() {
    return {
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        state: undefined,
        tag: undefined,
        task_id: undefined,
        task_name: undefined,
        node: undefined,
        start_range: undefined,
        address: undefined,
        sort: '+date_start'
      },
      resultQuery: {
        status: 'up'
      },
      resultData: [],
      resultTag: '',
      portResultTable: ['HOST_DISC', 'PORT_DISC', 'PORT_CHEK', 'PORT_INFO', 'PORT_RISK'],
      webcheckResultTable: ['WEB_CHECK'],
      stateOptions: [],
      tagOptions: [],
      dialogResultVisible: false,
      nodeOptions: [],
      downloadLoading: false,
      pickerStartRangeOptions: {
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
      fetchList(this.listQuery).then(response => {
        this.list = response.data.items
        this.total = response.data.total
      })
      this.listLoading = false
    },
    optionsList() {
      fetchList({ action: 'options' }).then(response => {
        this.tagOptions = response.data.tag
        this.stateOptions = response.data.state
        this.nodeOptions = response.data.business
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
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
    handleFetchResult(row) {
      this.resultData = row.result
      this.resultTag = row.param.tag
      this.dialogResultVisible = true
    },
    filterResultHandler(value, row, column) {
      const property = column['property']
      return row[property] === value
    },
    handlePause(row) {
      this.$notify({
        title: 'Success',
        message: '暂停任务 Successfully',
        type: 'success',
        duration: 2000
      })
    },
    handleStop(row) {
      this.$notify({
        title: 'Success',
        message: '终止任务 Successfully',
        type: 'success',
        duration: 2000
      })
    },
    openStatusMessage(row) {
      this.$alert(row.message, row.state, {
        confirmButtonText: '确定'
      })
    }
  }
}
</script>
