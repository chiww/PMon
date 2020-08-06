import request from '@/utils/request'

export function getList(params) {
  return request({
    url: '/admin/table/list',
    method: 'get',
    params
  })
}
