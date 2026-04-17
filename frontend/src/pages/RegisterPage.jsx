import { useState } from 'react'
import { Form, Input, Button, Card, message, Typography } from 'antd'
import { UserOutlined, LockOutlined, MailOutlined } from '@ant-design/icons'
import { register } from '../api/auth'

const { Title, Text } = Typography

export default function RegisterPage({ onGoLogin }) {
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)

  const onFinish = async (values) => {
    setLoading(true)
    try {
      await register(values)
      setSuccess(true)
      message.success('注册成功，请登录')
    } catch (err) {
      const code = err.response?.data?.code
      if (code === 'ERR_CONFLICT') {
        message.error(err.response.data.message)
      } else {
        message.error('注册失败，请检查输入')
      }
    } finally {
      setLoading(false)
    }
  }

  if (success) {
    return (
      <div style={styles.center}>
        <Card style={styles.card}>
          <Title level={3} style={{ textAlign: 'center' }}>注册成功 🎉</Title>
          <Button type="primary" block onClick={onGoLogin}>前往登录</Button>
        </Card>
      </div>
    )
  }

  return (
    <div style={styles.center}>
      <Card style={styles.card}>
        <Title level={3} style={{ textAlign: 'center' }}>用户注册</Title>
        <Form layout="vertical" onFinish={onFinish} autoComplete="off">
          <Form.Item name="username" label="用户名"
            rules={[
              { required: true, message: '请输入用户名' },
              { min: 3, max: 32, message: '用户名长度 3~32 个字符' },
            ]}>
            <Input prefix={<UserOutlined />} placeholder="用户名" />
          </Form.Item>
          <Form.Item name="email" label="邮箱"
            rules={[{ required: true, message: '请输入邮箱' }, { type: 'email', message: '邮箱格式不正确' }]}>
            <Input prefix={<MailOutlined />} placeholder="邮箱" />
          </Form.Item>
          <Form.Item name="password" label="密码"
            rules={[{ required: true, message: '请输入密码' }, { min: 8, message: '密码至少 8 位' }]}>
            <Input.Password prefix={<LockOutlined />} placeholder="密码" />
          </Form.Item>
          <Form.Item name="confirm_password" label="确认密码"
            dependencies={['password']}
            rules={[
              { required: true, message: '请确认密码' },
              ({ getFieldValue }) => ({
                validator(_, v) {
                  if (!v || getFieldValue('password') === v) return Promise.resolve()
                  return Promise.reject(new Error('两次密码不一致'))
                },
              }),
            ]}>
            <Input.Password prefix={<LockOutlined />} placeholder="确认密码" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" block loading={loading}>注册</Button>
          </Form.Item>
          <Text>已有账号？<Button type="link" onClick={onGoLogin} style={{ padding: 0 }}>立即登录</Button></Text>
        </Form>
      </Card>
    </div>
  )
}

const styles = {
  center: { minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#f0f2f5' },
  card: { width: 400, borderRadius: 8, boxShadow: '0 2px 12px rgba(0,0,0,0.1)' },
}
