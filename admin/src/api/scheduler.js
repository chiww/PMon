// eslint-disable-next-line no-unused-vars
import axios from 'axios'
import { Message } from 'element-ui'
import store from '@/store'
import { getToken } from '@/utils/auth'

// create an axios instance
const request = axios.create({
  baseURL: process.env.VUE_APP_BASE_API, // url = base url + request url
  // withCredentials: true, // send cookies when cross-domain requests
  timeout: 5000 // request timeout
})

// request interceptor
request.interceptors.request.use(
  config => {
    // do something before request is sent

    if (store.getters.token) {
      // let each request carry token
      // ['X-Token'] is a custom headers key
      // please modify it according to the actual situation
      config.headers['X-Token'] = getToken()
    }
    return config
  },
  error => {
    // do something with request error
    console.log(error) // for debug
    return Promise.reject(error)
  }
)

// response interceptor
request.interceptors.response.use(
  /**
   * If you want to get http information such as headers or status
   * Please return  response => response
   */

  /**
   * Determine the request status by custom code
   * Here is just an example
   * You can also judge the status by HTTP Status Code
   */
  response => {
    const res = response.data
    // if the custom code is not 20000, it is judged as an error.
    if (response.status !== 200) {
      Message({
        message: res.message || 'Error',
        type: 'error',
        duration: 5 * 1000
      })
      return Promise.reject(new Error(res.message || 'Error'))
    } else {
      return res
    }
  },
  error => {
    console.log('err>>' + error) // for debug
    Message({
      message: error.message,
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

// self.api_prefix = '/scheduler'
// self._add_url_route('get_scheduler_info', '', api.get_scheduler_info, 'GET')
export function schedulerInfo(params) {
  return request({
    url: '/scheduler',
    method: 'get',
    params
  })
}

// self._add_url_route('add_job', '/jobs', api.add_job, 'POST')
export function addJob(params) {
  return request({
    url: '/scheduler/jobs',
    method: 'post',
    params
  })
}

// self._add_url_route('get_job', '/jobs/<job_id>', api.get_job, 'GET')
export function getJob(params) {
  return request({
    url: '/scheduler/jobs/' + params.id,
    method: 'get',
    params
  })
}

// self._add_url_route('get_jobs', '/jobs', api.get_jobs, 'GET')
export function getJobs(params) {
  return request({
    url: '/scheduler/jobs',
    method: 'get',
    params
  })
}

// self._add_url_route('delete_job', '/jobs/<job_id>', api.delete_job, 'DELETE')
export function deleteJob(params) {
  return request({
    url: '/scheduler/jobs/' + params.id,
    method: 'delete'
  })
}

// self._add_url_route('update_job', '/jobs/<job_id>', api.update_job, 'PATCH')
export function updateJob(params) {
  return request({
    url: '/scheduler/jobs/' + params.id,
    method: 'patch',
    params
  })
}

// self._add_url_route('pause_job', '/jobs/<job_id>/pause', api.pause_job, 'POST')
export function pauseJob(params) {
  return request({
    url: '/scheduler/jobs/' + params.id + '/pause',
    method: 'post',
    params
  })
}

// self._add_url_route('resume_job', '/jobs/<job_id>/resume', api.resume_job, 'POST')
export function resumeJob(params) {
  return request({
    url: '/scheduler/jobs/' + params.id + '/resume',
    method: 'post',
    params
  })
}

// self._add_url_route('run_job', '/jobs/<job_id>/run', api.run_job, 'POST')
export function runJob(params) {
  return request({
    url: '/scheduler/jobs/' + params.id + '/run',
    method: 'post'
  })
}

export function loadJob(data) {
  return request({
    url: '/scheduler/jobs/' + data.uuid + '/load',
    method: 'post',
    data
  })
}

export function unloadJob(data) {
  return request({
    url: '/scheduler/jobs/' + data.uuid + '/unload',
    method: 'post',
    data
  })
}

export function loadJobs(params) {
  return request({
    url: '/scheduler/jobs/loads',
    method: 'get'
  })
}

export function removeJobs(params) {
  return request({
    url: '/scheduler/jobs/remove',
    method: 'get'
  })
}

export function shutdown(data) {
  return request({
    url: '/scheduler/shutdown',
    method: 'get',
    data
  })
}

export function start(data) {
  return request({
    url: '/scheduler/start',
    method: 'get',
    data
  })
}

