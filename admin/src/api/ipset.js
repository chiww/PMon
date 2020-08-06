import request from '@/utils/request'

export function fetchIPSet(params) {
  return request({
    url: '/admin/ipset',
    method: 'get',
    params
  })
}

export function modifyIPSet(data) {
  return request({
    url: '/admin/ipset',
    method: 'post',
    data
  })
}
