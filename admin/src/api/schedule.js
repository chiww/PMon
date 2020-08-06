import request from '@/utils/request'

export function fetchTrigger(params) {
  return request({
    url: '/admin/schedule/trigger',
    method: 'get',
    params
  })
}

export function modifyTrigger(data) {
  return request({
    url: '/admin/schedule/trigger',
    method: 'post',
    data
  })
}

export function deleteTrigger(data) {
  return request({
    url: '/admin/schedule/trigger',
    method: 'delete',
    data
  })
}

export function fetchJob(params) {
  return request({
    url: '/admin/schedule/job',
    method: 'get',
    params
  })
}

export function modifyJob(data) {
  return request({
    url: '/admin/schedule/job',
    method: 'post',
    data
  })
}

export function deleteJob(data) {
  return request({
    url: '/admin/schedule/job',
    method: 'delete',
    data
  })
}

export function fetchTask(params) {
  return request({
    url: '/admin/schedule/task',
    method: 'get',
    params
  })
}

export function modifyTask(data) {
  return request({
    url: '/admin/schedule/task',
    method: 'post',
    data
  })
}

export function deleteTask(data) {
  return request({
    url: '/admin/schedule/task',
    method: 'delete',
    data
  })
}

export function fetchSchedule(params) {
  return request({
    url: '/admin/schedule/schedule',
    method: 'get',
    params
  })
}

export function modifySchedule(data) {
  return request({
    url: '/admin/schedule/schedule',
    method: 'post',
    data
  })
}

export function deleteSchedule(data) {
  return request({
    url: '/admin/schedule/schedule',
    method: 'delete',
    data
  })
}

export function fetchNode(params) {
  return request({
    url: '/admin/schedule/nodes',
    method: 'get',
    params
  })
}

export function modifyNode(data) {
  return request({
    url: '/admin/schedule/nodes',
    method: 'post',
    data
  })
}

export function deleteNode(data) {
  return request({
    url: '/admin/schedule/nodes',
    method: 'delete',
    data
  })
}

