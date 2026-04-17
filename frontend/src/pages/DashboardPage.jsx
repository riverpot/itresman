import { useState } from 'react'
import { Layout, Menu, Button, message, theme } from 'antd'
import { PoweroffOutlined } from '@ant-design/icons'
import { logout } from '../api/auth'

const { Header, Content, Sider } = Layout

export default function DashboardPage({ onLogout }) {
  const [collapsed, setCollapsed] = useState(false)
  const { token } = theme.useToken()

  const handleLogout = async () => {
    try {
      await logout()
    } catch {
      // 即使接口失败也清除本地 token
    }
    localStorage.removeItem('access_token')
    message.success('已退出登录')
    onLogout?.()
  }

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider collapsible collapsed={collapsed} onCollapse={setCollapsed}>
        <div style={{ height: 32, margin: 16, background: 'rgba(255,255,255,0.1)', borderRadius: 4, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', fontWeight: 'bold', fontSize: collapsed ? 12 : 14 }}>
          {collapsed ? 'IT' : 'IT 资源管理'}
        </div>
        <Menu theme="dark" defaultSelectedKeys={['dashboard']} mode="inline" items={[
          { key: 'dashboard', label: '控制台' },
          { key: 'vms', label: '虚拟机管理' },
          { key: 'disks', label: '云硬盘管理' },
          { key: 'network', label: '虚拟网络' },
        ]} />
      </Sider>
      <Layout>
        <Header style={{ background: token.colorBgContainer, padding: '0 24px', display: 'flex', alignItems: 'center', justifyContent: 'flex-end' }}>
          <Button icon={<PoweroffOutlined />} onClick={handleLogout}>退出登录</Button>
        </Header>
        <Content style={{ margin: 24 }}>
          <div style={{ padding: 24, minHeight: 360, background: token.colorBgContainer, borderRadius: 8 }}>
            <h2>欢迎使用企业IT资源管理系统</h2>
            <p>请从左侧菜单选择功能模块。</p>
          </div>
        </Content>
      </Layout>
    </Layout>
  )
}
