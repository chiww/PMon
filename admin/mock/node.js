import Mock from 'mockjs'

const data = Mock.mock({
  'items|30': [{
    id: '@id',
    name: '@name()',
    'status|1': ['enable', 'disable'],
    ip: '@ip()',
    'scope|1-1': ['192.168.0.0/16', '10.0.0.0/8', '172.16.0.0/12'],
    remark: '@name()'
  }]
})

export default [
  {
    url: '/monitor-admin/node/list',
    type: 'get',
    response: config => {
      const items = data.items
      return {
        code: 20000,
        data: {
          total: items.length,
          items: items
        }
      }
    }
  },
  {
    url: '/monitor-admin/node/create',
    type: 'post',
    response: _ => {
      return {
        code: 20000,
        data: 'success'
      }
    }
  },

  {
    url: '/monitor-admin/node/update',
    type: 'post',
    response: _ => {
      return {
        code: 20000,
        data: 'success'
      }
    }
  }
]
