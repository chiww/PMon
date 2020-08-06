import request from '@/utils/request'

export function updateTicket(data) {
  return request({
    url: '/admin/ticket',
    method: 'post',
    data
  })
}
