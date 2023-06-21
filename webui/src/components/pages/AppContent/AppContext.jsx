import { createContext, useState, useEffect } from "react";
import {
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword,
    signOut,
    onAuthStateChanged,
    GoogleAuthProvider,
    signInWithPopup,
  } from 'firebase/auth';
  import { auth } from '../Authentication/Firebase'
  
export const GoogleProvider = new GoogleAuthProvider();

export const UserContext = createContext();

function AppContext(props){
    const [user, setUser] = useState({});
    const [token, setToken] = useState("");

    const createUser = (email, password) => {
        return createUserWithEmailAndPassword(auth, email, password);
      };
    
    const signIn = (email, password) =>  {
    return signInWithEmailAndPassword(auth, email, password)
    };

    const signInWithGoogle = async () => {
      try {
        const result = await signInWithPopup(auth, GoogleProvider);
      } catch (error) {
        alert(error);
      }
    };
    
    const logout = () => {
        return signOut(auth)
    };
    
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      
      const getToken = async (currentUser) => {
        const token = await currentUser.getIdToken();
        setToken(token);
      };
     
      
      if (currentUser) {
          getToken(currentUser);
          setUser(currentUser);
      } else {
        setUser("");
      }
    });
    return () => unsubscribe();
  }, []);

  // get user data from backend for initial display.

  return (
    <UserContext.Provider
      value={{ user, logout, signIn, signInWithGoogle, createUser, token, }} // Include the token and tokenReady in the context value
    >
      {props.children}
    </UserContext.Provider>
  );
}

export default AppContext;