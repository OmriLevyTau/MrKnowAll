import React, {useContext} from 'react';
import { useNavigate } from 'react-router-dom';
import { UserContext } from '../AppContent/AppContext';

const Account = () => {
    const { user, logout} = useContext(UserContext);

    const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/signin');
      // ??? need to reset user state ???
    } catch (e) {
      alert(e.message);
    }
  };

  return (
    <div >
      <h1>Account</h1>
      <p>User Email: {user && user.email}</p>

      <button onClick={handleLogout}>
        Logout
      </button>
    </div>
  );
};

export default Account;