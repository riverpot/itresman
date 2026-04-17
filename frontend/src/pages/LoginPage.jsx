import { useState } from 'react'
import { Form, Input, Button, Card, message, Typography } from 'antd'
import { UserOutlined, LockOutlined } from '@ant-design/icons'
import { login } from '../api/auth'

const { Title, Text } = Typography

export default function LoginPage({ onLoginSuccess, onGoRegister }) {
  const [loading, setLoading] = useState(false)

  const onFinish = async (values) => {
    setLoading(true)
    try {
      const res = await login(values)
      localStorage.setItem('access_token', res.data.access_token)
      message.success('登录成功')
      onLoginSuccess?.()
    } catch (err) {
      const status = err.response?.status
      if (status === 401) message.error('用户名或密码错误')
      else if (status === 403) message.error('账户已禁用，请联系管理员')
      else message.error('登录失败，请稍后重试')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={styles.center}>
      <Card style={styles.card}>
        <Title level={3} style={{ textAlign: 'center' }}>用户登录</Title>
        <Form layout="vertical" onFinish={onFinish} autoComplete="off">
          <Form.Item name="username" label="用户名 / 邮箱"
            rules={[{ required: true, message: '请输入用户名或邮箱' }]}>
            <Input prefix={<UserOutlined />} placeholder="用户名或邮箱" />
          </Form.Item>
          <Form.Item name="password" label="密码"
            rules={[{ required: true, message: '请输入密码' }]}>
            <Input.Password prefix={<LockOutlined />} placeholder="密码" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" block loading={loading}>登录</Button>
          </Form.Item>
          <Text>没有账号？<Button type="link" onClick={onGoRegister} style={{ padding: 0 }}>立即注册</Button></Text>
        </Form>
      </Card>
    </div>
  )
}

const styles = {
  center: { minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#f0f2f5' },
  card: { width: 400, borderRadius: 8, boxShadow: '0 2px 12px rgba(0,0,0,0.1)' },
}
