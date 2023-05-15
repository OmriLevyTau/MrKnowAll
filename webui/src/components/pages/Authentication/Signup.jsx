import React, { useState , useContext} from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Form, Input, Button } from 'antd';
import { UserContext } from '../AppContent/AppContext';

const Signup = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('')
  const { createUser} = useContext(UserContext);
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await createUser(email, password);
      navigate('/home')
    } catch (e) {
      setError(e.message);
      alert(e.message);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection:"column" }}>
      <div class="split left"/>        
      <div class="split right" style={{width: "50%",  flexDirection:"column"}}>
        <div>
          <h1 >Sign up for a free account</h1>
          <p>
            Already have an account yet?{' '}
            <Link to='/signin' className='underline'>
              Sign in.
            </Link>
          </p>
        </div>
      
        <Form
          name="basic"
          labelCol={{ span: 4, }}
          wrapperCol={{  span: 13, }}
          style={{ maxWidth: 600,  }}
          initialValues={{ remember: true, }}
          autoComplete="off"
          onSubmit={handleSubmit}
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
                <Input onChange={(e) => setEmail(e.target.value)} />
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
            <Input.Password onChange={(e) => setPassword(e.target.value)}  />
            </Form.Item>

        <Form.Item
        wrapperCol={{ offset: 8, span: 16, }}
        >
        <Button type='primary' htmlType="submit" onClick={handleSubmit}>
            Sign up
        </Button>
        </Form.Item>
      </Form>
      </div>
    </div>

  );
};

export default Signup;