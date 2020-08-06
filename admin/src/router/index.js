import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },

  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '首页', icon: 'mdashboard' }
    }]
  },
  //
  {
    path: '/risk',
    component: Layout,
    redirect: '/risk/port',
    name: 'Risk',
    meta: {
      title: '风险面板',
      icon: 'risk'
    },
    children: [
      {
        path: 'port',
        component: () => import('@/views/risk/port'),
        name: 'port',
        meta: { title: '端口服务' }
      },
      {
        path: 'service',
        component: () => import('@/views/risk/web'),
        name: 'service',
        meta: { title: '高危后台' }
      }
    ]
  },
  {
    path: '/assets',
    component: Layout,
    redirect: '/assets/ipassets',
    name: 'Assets',
    meta: {
      title: '资产管理',
      icon: 'assets'
    },
    children: [
      {
        path: 'ipassets',
        component: () => import('@/views/assets/ipassets'),
        name: 'ipassets',
        meta: { title: 'IP资产' }
      },
      {
        path: 'ipset',
        component: () => import('@/views/assets/ipset'),
        name: 'ipset',
        meta: { title: 'IP存活' }
      }
    ]
  },
  {
    path: '/task',
    component: Layout,
    redirect: '/task/worker',
    name: 'Task',
    meta: {
      title: '任务面板',
      icon: 'task'
    },
    children: [
      {
        path: 'worker',
        component: () => import('@/views/task/worker'),
        meta: { title: '节点任务' }
      },
      {
        path: 'scheduler',
        component: () => import('@/views/task/scheduler'),
        name: 'scheduler',
        meta: { title: '后台任务' }
      },
      {
        path: 'schedule',
        component: () => import('@/views/task/schedule'),
        name: 'schedule',
        meta: { title: '任务配置' }
      }
    ]
  },
  {
    path: '/settings',
    component: Layout,
    redirect: '/settings/system',
    name: 'Settings',
    meta: {
      title: '配置面板',
      icon: 'settings'
    },
    children: [
      {
        path: 'system',
        component: () => import('@/views/settings/system'),
        name: 'system',
        meta: { title: '系统配置' }
      },
      {
        path: 'node',
        component: () => import('@/views/settings/node'),
        name: 'node',
        meta: { title: '节点配置' }
      }
    ]
  },
  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
