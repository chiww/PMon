import request from '@/utils/request'

export function fetchWebList(query) {
  return request({
    url: '/admin/web',
    method: 'get',
    params: query
  })
}

export function updateWebTicket(data) {
  return request({
    url: '/admin/ticket',
    method: 'post',
    data
  })
}
