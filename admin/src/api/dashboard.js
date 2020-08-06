import request from '@/utils/request'

export function fetchDashboard(params) {
  return request({
    url: '/admin/dashboard',
    method: 'get',
    params
  })
}

export function fetchPanelCount(params) {
  return request({
    url: '/admin/panel_count',
    method: 'get',
    params
  })
}

export function fetchHisLine(params) {
  return request({
    url: '/admin/his_line',
    method: 'get',
    params
  })
}

export function fetchRiskBar(params) {
  return request({
    url: '/admin/risk_bar',
    method: 'get',
    params
  })
}

export function fetchReportPie(params) {
  return request({
    url: '/admin/report_pie',
    method: 'get',
    params
  })
}

export function fetchUnreportedPie(params) {
  return request({
    url: '/admin/unreported_pie',
    method: 'get',
    params
  })
}
