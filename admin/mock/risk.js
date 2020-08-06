import Mock from 'mockjs'

const portList = [
  { ip: '', host: '', port: '80', owner: 'Anna.Wang', business: 'BU-A', discover_time: 1464117240475, ticket_info: { id: '1234567890', status: 'reported', owner: 'william.chen', remark: 'xxx', timestamp: 1464117240475, type: 'ECP' }}
]
export default [

  {
    url: '/monitor-admin/risk/port/list',
    type: 'get',
    response: _ => {
      return {
        code: 20000,
        data: {
          total: 20,
          'items|20': [{
            ip: '@ip()',
            host: '@ip()',
            port: '@integer(1, 65535)',
            owner: '@name()',
            sys_code: '@guid()',
            business: '@name()',
            discover_time: Mock.Random.date('T'),
            update_time: Mock.Random.date('T'),
            ticket_info: {
              'status|1': ['reported', 'unreported'],
              id: '@id()',
              owner: '@name()',
              remark: Mock.Random.csentence(20, 30),
              timestamp: Mock.Random.date('T'),
              'source|1': ['ByHandle', 'ECP', 'ITSM', 'OTHER']
            }
          }]
        }
      }
    }
  },

  {
    url: '/monitor-admin/risk/port/ticket/update',
    type: 'post',
    response: _ => {
      return {
        code: 20000,
        data: 'success'
      }
    }
  },

  {
    url: '/monitor-admin/risk/service',
    type: 'get',
    response: _ => {
      return {
        code: 20000,
        data: {
          total: 20,
          'items|20': [{
            ip: '@ip()',
            host: '@ip()',
            service: '@integer(1, 65535)',
            owner: '@name()',
            sys_code: '@guid()',
            discover_time: +Mock.Random.date('T'),
            update_time: +Mock.Random.date('T'),
            ticket_info: {
              ticket_id: '@id()',
              owner: '@name()',
              remark: Mock.Random.csentence(20, 30)
            }
          }]
        }
      }
    }
  },
  {
    url: '/monitor-admin/risk/vuln',
    type: 'get',
    response: _ => {
      return {
        code: 20000,
        data: {
          total: 20,
          'items|20': [{
            ip: '@ip()',
            host: '@ip()',
            port: '@integer(1, 65535)',
            owner: '@name()',
            sys_code: '@guid()',
            discover_time: +Mock.Random.date('T'),
            update_time: +Mock.Random.date('T'),
            ticket_info: {
              ticket_id: '@id()',
              owner: '@name()',
              remark: Mock.Random.csentence(20, 30)
            }
          }]
        }
      }
    }
  }
]
