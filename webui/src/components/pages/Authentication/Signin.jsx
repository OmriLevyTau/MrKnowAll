import React, { useState, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { UserContext } from '../AppContent/AppContext';
import { Form, Input, Button, Image } from 'antd';
import image from "../../../images/mustach3.png"
 


const Signin = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const {signIn} = useContext(UserContext);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('')
    try {
      await signIn(email, password)
      navigate('/home')
    } catch (e) {
      setError(e.message)
      alert(e.message)
    }
  };

  return (
    <div style={{ display: "flex", flexDirection:"column"}} >
      <div class="split left"/>        
      
      <div class="split right" style={{width: "50%",  flexDirection:"column"}}>
            <div >
              <h1 >Sign in to your account</h1>
              <p style={{alignContent:"center"}}>
                Don't have an account yet?{' '}
                <Link to='/signup' className='underline'>
                  Sign up.
                </Link>
              </p>
            </div>

            <Form
              name="basic"
              labelCol={{ span: 4, }}
              wrapperCol={{ span: 13, }}
              style={{ maxWidth: 600,}}
              initialValues={{ remember: true, }}
              autoComplete="off"
            >
              <Form.Item
                  label="email"
                  name="email"
                  rules={[
                      {
                      required: true,
                      message: 'Please input your email!',
                      },
                  ]}
                  >
                  <Input onChange={(e) => setEmail(e.target.value)} type='email'/>
              </Form.Item>

              <Form.Item
                  label="Password"
                  name="password"
                  rules={[
                      {
                      required: true,
                      message: 'Please input your password!',
                      },
                  ]}
                >
                <Input.Password onChange={(e) => setPassword(e.target.value)} type='password' />
              </Form.Item>

              <Form.Item
              wrapperCol={{
                  offset: 8,
                  span: 16,
              }}
              >
              <Button type='primary' htmlType="submit" onClick={handleSubmit}>
                  Sign in
              </Button>
              </Form.Item>
            </Form>

          </div>
        </div>
  );
};

export default Signin;