import request from '@/utils/request'

export function fetchIPAssets(params) {
  return request({
    url: '/admin/ipassets',
    method: 'get',
    params
  })
}

export function modifyIPAssets(data) {
  return request({
    url: '/admin/ipassets',
    method: 'post',
    data
  })
}

export function deleteIPAssets(data) {
  return request({
    url: '/admin/ipassets',
    method: 'delete',
    data
  })
}
