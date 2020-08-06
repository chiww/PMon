<template>
  <div class="app-container">
    <el-table
      v-loading="listLoading"
      :data="triggers"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
      style="width: 100%"
      size="mini"
    >
      <el-table-column label="UUID" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.uuid }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Name" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Trigger" align="center" width="100">
        <template slot-scope="scope">
          {{ scope.row.trigger }}
        </template>
      </el-table-column>
      <el-table-column label="Detail" align="center" width="150">
        <template slot-scope="scope">
          <ul v-for="(value, key) in scope.row" :key="key" style="text-align: left; margin: 0; padding: 0">
            <li v-if="['uuid', 'name', 'remark', 'trigger', 'misfire_grace_time', 'coalesce', 'max_instances', 'next_run_time', 'replace_existing'].indexOf(key) === -1">
              <span> {{ key }}:</span>
              <span v-if="['start_date', 'end_date', 'run_date'].indexOf(key) >= 0" style="color: blue">{{ value * 1000 | handleTime('{y}-{m}-{d} {h}:{i}') }}</span>
              <span v-else style="color: blue">{{ value }}</span>
            </li>
          </ul>
        </template>
      </el-table-column>
      <el-table-column label="Setting" align="center" width="150">
        <template slot-scope="scope">
          <ul v-for="(value, key) in scope.row" :key="key" style="text-align: left; margin: 0; padding: 0">
            <li v-if="['misfire_grace_time', 'coalesce', 'max_instances', 'next_run_time', 'replace_existing'].indexOf(key) >= 0">
              <span> {{ key }}:</span>
              <span style="color: blue">{{ value }}</span>
            </li>
          </ul>
        </template>
      </el-table-column>
      <el-table-column label="Remark" align="center">
        <template slot-scope="scope">
          {{ scope.row.remark }}
        </template>
      </el-table-column>
      <el-table-column label="Actions" align="center" width="300" class-name="small-padding fixed-width">
        <template slot="header">
          <el-button class="filter-item" size="mini" type="primary" icon="el-icon-circle-plus-outline" @click="handleTriggerCreate">
            新增
          </el-button>
        </template>
        <template slot-scope="{row,$index}">
          <el-button type="primary" size="mini" icon="el-icon-edit-outline" @click="handleTriggerUpdate(row)">编辑</el-button>
          <el-button type="danger" size="mini" icon="el-icon-delete" @click="handleTriggerDelete(row,$index)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogTriggerFormVisible" width="35%">
      <el-form ref="dataForm" :model="triggerItems" label-position="left" label-width="auto">
        <el-form-item label="trigger">
          <el-select v-model="triggerItems.trigger" size="mini" class="filter-item" placeholder="Please select">
            <el-option v-for="item in ['interval', 'date', 'cron']" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="uuid">
          <el-input v-model="triggerItems.uuid" :autosize="{ minRows: 1, maxRows: 1}" disabled type="textarea" placeholder="后台生成" />
        </el-form-item>
        <el-form-item label="name">
          <el-input v-model="triggerItems.name" :autosize="{ minRows: 1, maxRows: 1}" type="textarea" placeholder="Please input" />
        </el-form-item>
        <div v-if="triggerItems.trigger === 'interval'">
          <el-form-item label="seconds">
            <el-input v-model="triggerItems.seconds" :autosize="{ minRows: 1, maxRows: 1}" type="textarea" placeholder="Please input" />
          </el-form-item>
          <el-form-item label="minutes">
            <el-input v-model="triggerItems.minutes" :autosize="{ minRows: 1, maxRows: 1}" type="textarea" placeholder="Please input" />
          </el-form-item>
          <el-form-item label="hours">
            <el-input v-model="triggerItems.hours" :autosize="{ minRows: 1, maxRows: 1}" type="textarea" placeholder="Please input" />
          </el-form-item>
          <el-form-item label="days">
            <el-input v-model="triggerItems.days" :autosize="{ minRows: 1, maxRows: 1}" type="textarea" placeholder="Please input" />
          </el-form-item>
          <el-form-item label="weeks">
            <el-input v-model="triggerItems.weeks" :autosize="{ minRows: 1, maxRows: 1}" type="textarea" placeholder="Please input" />
          </el-form-item>
        </div>
        <div v-if="triggerItems.trigger === 'date'">
          <el-form-item label="run_date">
            <el-date-picker
              v-model="triggerItems.run_date"
              type="datetime"
              size="mini"
              placeholder="选择日期时间"
              value-format="timestamp"
            />
          </el-form-item>
        </div>
        <div v-if="triggerItems.trigger === 'cron'">
          <el-form-item label="second">
            <el-input v-model="triggerItems.second" :autosize="{ minRows: 1, maxRows: 1}" type="textarea" placeholder="Please input" />
          </el-form-item>
          <el-form-item label="minute">
            <el-input v-model="triggerItems.minute" :autosize="{ minRows: 1, maxRows: 1}" type="textarea" placeholder="Please input" />
          </el-form-item>
          <el-form-item label="hour">
            <el-input v-model="triggerItems.hour" :autosize="{ minRows: 1, maxRows: 1}" type="textarea" placeholder="Please input" />
          </el-form-item>
          <el-form-item label="day">
            <el-input v-model="triggerItems.day" :autosize="{ minRows: 1, maxRows: 1}" type="textarea" placeholder="Please input" />
          </el-form-item>
          <el-form-item label="week">
            <el-input v-model="triggerItems.week" :autosize="{ minRows: 1, maxRows: 1}" type="textarea" placeholder="Please input" />
          </el-form-item>
          <el-form-item label="month">
            <el-input v-model="triggerItems.month" :autosize="{ minRows: 1, maxRows: 1}" type="textarea" placeholder="Please input" />
          </el-form-item>
          <el-form-item label="year">
            <el-input v-model="triggerItems.year" :autosize="{ minRows: 1, maxRows: 1}" type="textarea" placeholder="Please input" />
          </el-form-item>
          <el-form-item label="day_of_week">
            <el-input v-model="triggerItems.day_of_week" :autosize="{ minRows: 1, maxRows: 1}" type="textarea" placeholder="Please input" />
          </el-form-item>
        </div>
        <div v-if="triggerItems.trigger !== 'date'">
          <!--          <el-form-item label="start_date">-->
          <!--            <el-input v-model="triggerItems.start_date" :autosize="{ minRows: 1, maxRows: 1}" type="textarea" placeholder="Please input" />-->
          <!--          </el-form-item>-->
          <!--          <el-form-item label="end_date">-->
          <!--            <el-input v-model="triggerItems.end_date" :autosize="{ minRows: 1, maxRows: 1}" type="textarea" placeholder="Please input" />-->
          <!--          </el-form-item>-->
          <el-form-item label="start_end">
            <el-date-picker
              v-model="triggerItems.start_end"
              type="datetimerange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              size="mini"
              value-format="timestamp"
            />
          </el-form-item>
        </div>
        <el-form-item label="remark">
          <el-input v-model="triggerItems.remark" :autosize="{ minRows: 1, maxRows: 4}" type="textarea" placeholder="Please input" />
        </el-form-item>
        <el-form-item label="misfire_grace_time">
          <el-input v-model="triggerItems.misfire_grace_time" :autosize="{ minRows: 1, maxRows: 1}" type="textarea" placeholder="除非清楚该选项含义，否则请保持默认！" />
        </el-form-item>
        <el-form-item label="coalesce">
          <el-input v-model="triggerItems.coalesce" :autosize="{ minRows: 1, maxRows: 1}" type="textarea" placeholder="除非清楚该选项含义，否则请保持默认！" />
        </el-form-item>
        <el-form-item label="max_instances">
          <el-input v-model="triggerItems.max_instances" :autosize="{ minRows: 1, maxRows: 1}" type="textarea" placeholder="除非清楚该选项含义，否则请保持默认！" />
        </el-form-item>
        <el-form-item label="next_run_time">
          <el-input v-model="triggerItems.next_run_time" :autosize="{ minRows: 1, maxRows: 1}" type="textarea" placeholder="除非清楚该选项含义，否则请保持默认！" />
        </el-form-item>
        <el-form-item label="replace_existing">
          <el-input v-model="triggerItems.replace_existing" :autosize="{ minRows: 1, maxRows: 1}" type="textarea" placeholder="除非清楚该选项含义，否则请保持默认！" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogTriggerFormVisible = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createTriggerData():updateTriggerData()">
          Confirm
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { fetchTrigger, modifyTrigger, deleteTrigger } from '@/api/schedule'
import { parseTime } from '@/utils'

export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        true: 'success',
        false: 'danger'
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
      triggers: [],
      listLoading: true,
      triggerItems: {
        uuid: '',
        trigger: 'interval',
        name: '',
        misfire_grace_time: undefined,
        coalesce: undefined,
        max_instances: 1,
        next_run_time: undefined,
        replace_existing: undefined,
        // interval
        seconds: undefined,
        minutes: undefined,
        hours: undefined,
        days: undefined,
        weeks: undefined,
        start_date: undefined,
        end_date: undefined,
        timezone: 'Asia/Shanghai',
        start_end: [],
        // date
        run_date: undefined,
        // cron
        second: undefined,
        minute: undefined,
        hour: undefined,
        day: undefined,
        week: undefined,
        month: undefined,
        year: undefined,
        day_of_week: undefined,
        remark: ''
      },
      // intervalItems: {
      //   seconds: undefined,
      //   minutes: undefined,
      //   hours: undefined,
      //   days: undefined,
      //   weeks: undefined,
      //   start_date: undefined,
      //   end_date: undefined
      // },
      // cronItems: {
      //   second: undefined,
      //   minute: undefined,
      //   hour: undefined,
      //   day: undefined,
      //   week: undefined,
      //   month: undefined,
      //   year: undefined,
      //   day_of_week: undefined,
      //   start_date: undefined,
      //   end_date: undefined
      // },
      // dateItems: {
      //   run_date: undefined
      // },
      dialogTriggerFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Edit',
        create: 'Create'
      }
    }
  },
  created() {
    this.getTriggerList()
  },
  methods: {
    getTriggerList() {
      this.listLoading = true
      fetchTrigger().then(response => {
        this.triggers = response.data.items
        this.total = response.data.length
      })
      this.listLoading = false
    },
    resetItems() {
      this.triggerItems = {
        uuid: '',
        trigger: 'interval',
        name: '',
        misfire_grace_time: undefined,
        coalesce: undefined,
        max_instances: 1,
        next_run_time: undefined,
        replace_existing: undefined,
        // interval
        seconds: undefined,
        minutes: undefined,
        hours: undefined,
        days: undefined,
        weeks: undefined,
        start_date: undefined,
        end_date: undefined,
        start_end: [],
        timezone: 'Asia/Shanghai',
        // date
        run_date: undefined,
        // cron
        second: undefined,
        minute: undefined,
        hour: undefined,
        day: undefined,
        week: undefined,
        month: undefined,
        year: undefined,
        day_of_week: undefined,
        remark: ''
      }
    },
    handleTriggerCreate() {
      this.resetItems()
      this.dialogStatus = 'create'
      this.dialogTriggerFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createTriggerData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          modifyTrigger(this.triggerItems).then(() => {
            this.triggers.push(this.triggerItems)
            this.dialogTriggerFormVisible = false
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
    handleTriggerUpdate(row) {
      this.triggerItems = Object.assign({}, row) // copy obj
      this.triggerItems['start_end'] = [this.triggerItems['start_date'] * 1000, this.triggerItems['end_date'] * 1000]
      if (this.triggerItems['run_date'] !== undefined) {
        this.triggerItems['run_date'] = this.triggerItems['run_date'] * 1000
      }
      this.dialogStatus = 'update'
      this.dialogTriggerFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateTriggerData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.triggerItems)
          modifyTrigger(tempData).then(() => {
            const index = this.triggers.findIndex(v => v.uuid === tempData.uuid)
            this.triggers.splice(index, 1, this.triggerItems)
            this.dialogTriggerFormVisible = false
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
    handleTriggerDelete(row, index) {
      deleteTrigger(row).then(() => {
        this.$notify({
          title: 'Success',
          message: 'Delete Successfully',
          type: 'success',
          duration: 2000
        })
        this.triggers.splice(index, 1)
      })
    }
  }
}
</script>

