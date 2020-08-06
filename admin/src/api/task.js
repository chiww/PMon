import request from '@/utils/request'

export function fetchList(query) {
  return request({
    url: '/admin/tasks',
    method: 'get',
    params: query
  })
}

export function fetchResult(query) {
  return request({
    url: '/admin/task/result',
    method: 'get',
    params: query
  })
}

