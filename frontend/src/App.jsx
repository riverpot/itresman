import { useState } from 'react'
import { ConfigProvider, App as AntApp } from 'antd'
import zhCN from 'antd/locale/zh_CN'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'

function AppContent() {
  const [page, setPage] = useState(
    localStorage.getItem('access_token') ? 'dashboard' : 'login'
  )

  if (page === 'register') {
    return <RegisterPage onGoLogin={() => setPage('login')} />
  }
  if (page === 'dashboard') {
    return <DashboardPage onLogout={() => setPage('login')} />
  }
  return (
    <LoginPage
      onLoginSuccess={() => setPage('dashboard')}
      onGoRegister={() => setPage('register')}
    />
  )
}

export default function App() {
  return (
    <ConfigProvider locale={zhCN}>
      <AntApp>
        <AppContent />
      </AntApp>
    </ConfigProvider>
  )
}
