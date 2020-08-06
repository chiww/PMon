import Mock from 'mockjs'

const NameList = []
const count = 100

for (let i = 0; i < count; i++) {
  NameList.push(Mock.mock({
    name: '@first'
  }))
}
NameList.push({ name: 'mock-Pan' })

export default [

  // task list
  {
    url: '/monitor-admin/task/list',
    type: 'get',
    response: _ => {
      return {
        code: 20000,
        data: {
          total: 20,
          'items|20': [{
            task_id: '@guid()',
            task_name: 'task' + '@name()',
            // start_time: +Mock.Random.date('T'),
            // end_time: +Mock.Random.date('T'),
            start_time: '@datetime',
            end_time: '@datetime',
            node_name: '@name()',
            // price: '@float(1000, 15000, 0, 2)',
            'status|1': ['SUCCESS', 'STARTED', 'FAILED', 'PENDING']
          }]
        }
      }
    }
  },

  {
    url: '/monitor-admin/task/result',
    type: 'get',
    response: _ => {
      return {
        code: 20000,
        data: {
          resultData: [
            { ip: '@ip()', result: '1024' },
            { ip: '@ip()', result: '8080' },
            { ip: '@ip()', result: '22' },
            { ip: '@ip()', result: '5566' }
          ]
        }
      }
    }
  }
]
