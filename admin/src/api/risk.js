import request from '@/utils/request'

export function fetchPortList(query) {
  return request({
    url: '/admin/risk/port/list',
    method: 'get',
    params: query
  })
}

export function updatePortTicket(data) {
  return request({
    url: '/admin/risk/port/ticket/update',
    method: 'post',
    data
  })
}

export function fetchService(query) {
  return request({
    url: '/admin/risk/service',
    method: 'get',
    params: query
  })
}

export function fetchVuln(query) {
  return request({
    url: '/admin/risk/vuln',
    method: 'get',
    params: query
  })
}
