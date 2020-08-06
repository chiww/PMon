import request from '@/utils/request'

export function fetchPortList(query) {
  return request({
    url: '/admin/ports',
    method: 'get',
    params: query
  })
}
