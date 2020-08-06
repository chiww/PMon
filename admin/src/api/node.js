import request from '@/utils/request'

export function fetchNode(params) {
  return request({
    url: '/admin/node',
    method: 'get',
    params
  })
}

export function modifyNode(data) {
  return request({
    url: '/admin/node',
    method: 'post',
    data
  })
}

export function deleteNode(data) {
  return request({
    url: '/admin/node',
    method: 'delete',
    data
  })
}

