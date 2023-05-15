import React, {useContext} from 'react';
import { Navigate } from 'react-router-dom';
import { UserContext } from './AppContext';

const ProtectedRoute = ({ children }) => {
  const {user} = useContext(UserContext);

  if (!user) {
    return <Navigate to='/signin' replace={true} />;
  }
  return children;
};

export default ProtectedRoute;