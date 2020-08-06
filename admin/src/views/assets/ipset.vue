<template>
  <div class="app-container">
    <div class="filter-container" style="margin-bottom: 10px">
      <el-row class="tables-search" style="width: 100%">
        <el-col :span="24">
          <div>
            <el-input v-model="listQuery.ip" placeholder="IP" style="width: 150px;" class="filter-item" size="mini" @keyup.enter.native="handleFilter" />
            <el-input v-model="listQuery.host" placeholder="Host" style="width: 150px;" class="filter-item" size="mini" @keyup.enter.native="handleFilter" />
            <el-select v-model="listQuery.range" placeholder="网段" clearable style="width: 140px" size="mini" class="filter-item">
              <el-option v-for="item in rangeOptions" :key="item" :label="item" :value="item" />
            </el-select>
            <el-select v-model="listQuery.sys_code" placeholder="系统编码" clearable style="width: 140px" size="mini" class="filter-item">
              <el-option v-for="item in syscodeOptions" :key="item" :label="item" :value="item" />
            </el-select>
            <el-select v-model="listQuery.owner" placeholder="负责人" clearable style="width: 140px" size="mini" class="filter-item">
              <el-option v-for="item in ownerOptions" :key="item" :label="item" :value="item" />
            </el-select>
            <el-select v-model="listQuery.status" placeholder="状态" clearable style="width: 140px" size="mini" class="filter-item">
              <el-option v-for="item in statusOptions" :key="item" :label="item" :value="item" />
            </el-select>
            <el-date-picker
              v-model="listQuery.discover_range"
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
            <el-button class="filter-item" type="primary" size="mini" icon="el-icon-search" @click="handleFilter">
              Search
            </el-button>
          </div>
        </el-col>
      </el-row>
    </div>

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
      <el-table-column label="IP" align="center">
        <template slot-scope="scope">
          {{ scope.row.ip }}
        </template>
      </el-table-column>
      <el-table-column label="Range" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.range }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Host" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.assets.host }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Owner" align="center">
        <template slot-scope="scope">
          {{ scope.row.assets.owner }}
        </template>
      </el-table-column>
      <el-table-column label="SysCode" align="center">
        <template slot-scope="scope">
          {{ scope.row.assets.sys_code }}
        </template>
      </el-table-column>
      <el-table-column label="Business" align="center">
        <template slot-scope="scope">
          {{ scope.row.assets.business }}
        </template>
      </el-table-column>
      <el-table-column label="Discover" align="center">
        <template slot-scope="scope">
          {{ scope.row.discover_time | handleTime('{y}-{m}-{d} {h}:{i}') }}
        </template>
      </el-table-column>
      <el-table-column label="Update" align="center">
        <template slot-scope="scope">
          {{ scope.row.update_time | handleTime('{y}-{m}-{d} {h}:{i}') }}
        </template>
      </el-table-column>
      <el-table-column label="FailedTimes" align="center">
        <template slot-scope="scope">
          {{ scope.row.failed_times }}
        </template>
      </el-table-column>
      <el-table-column class-name="status-col" label="Status" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.status | statusFilter">{{ scope.row.status }}</el-tag>
        </template>
      </el-table-column>
      <!--      <el-table-column label="Actions" align="center" width="210" class-name="small-padding fixed-width">-->
      <!--        <template slot-scope="{row,$index}">-->
      <!--          <el-button size="mini" type="danger" @click="handleDelete(row,$index)">删除</el-button>-->
      <!--        </template>-->
      <!--      </el-table-column>-->
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

  </div>
</template>

<script>
import { fetchIPSet } from '@/api/ipset'
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination

export default {
  components: { Pagination },
  filters: {
    statusFilter(status) {
      const statusMap = {
        DOWN: 'success',
        UP: 'danger'
      }
      return statusMap[status]
    },
    handleTime(timestamp) {
      return parseTime(timestamp)
    }
  },
  data() {
    return {
      total: 0,
      list: null,
      listLoading: true,
      statusOptions: [],
      ownerOptions: [],
      syscodeOptions: [],
      rangeOptions: [],
      listQuery: {
        page: 1,
        limit: 20,
        ip: undefined,
        owner: undefined,
        host: undefined,
        sys_code: undefined,
        business: undefined,
        status: undefined,
        discover_range: undefined
      },
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
    this.getOptions()
  },
  methods: {
    getList() {
      this.listLoading = true
      fetchIPSet(this.listQuery).then(response => {
        this.list = response.data.items
        this.total = response.data.total
      })
      this.listLoading = false
    },
    getOptions() {
      this.listLoading = true
      fetchIPSet({ action: 'options' }).then(response => {
        this.statusOptions = response.data.status
        this.ownerOptions = response.data.owner
        this.syscodeOptions = response.data.sys_code
        this.rangeOptions = response.data.range
      })
      this.listLoading = false
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
    }
  }
}
</script>
