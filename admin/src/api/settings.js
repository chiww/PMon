import request from '@/utils/request'

export function fetchSettings(params) {
  return request({
    url: '/admin/settings',
    method: 'get',
    params
  })
}

export function updateSettings(data) {
  return request({
    url: '/admin/settings',
    method: 'post',
    data
  })
}
