import React, {useContext} from 'react';
import { useNavigate } from 'react-router-dom';
import { UserContext } from '../AppContent/AppContext';
import useFileTableStore from '../MyWorkspace/fileStore';
import { useQueryClient } from '@tanstack/react-query';
import useChatStore from '../Chat/chatStore';


const Account = () => {
    const { user, logout} = useContext(UserContext);
    const {setAllFiles} = useFileTableStore();
    const {clearChatStore} = useChatStore();
    const queryClient = useQueryClient()


    const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await logout();
      // clear cache when done
      queryClient.clear();
      setAllFiles([]);
      clearChatStore();
      navigate('/signin');
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