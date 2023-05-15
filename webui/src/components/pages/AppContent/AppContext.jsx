import { createContext, useState, useEffect } from "react";
import {
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword,
    signOut,
    onAuthStateChanged,
  } from 'firebase/auth';
  import { auth } from '../Authentication/Firebase'
  


export const UserContext = createContext();

function AppContext(props){
    const [user, setUser] = useState({});


    const createUser = (email, password) => {
        return createUserWithEmailAndPassword(auth, email, password);
      };
    
       const signIn = (email, password) =>  {
        return signInWithEmailAndPassword(auth, email, password)
       }
    
      const logout = () => {
          return signOut(auth)
      }
    
      useEffect(() => {
        const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
          if (currentUser){
            setUser(currentUser);
          } else{
            setUser("")
          }
          console.log(user)
        });
        return () => unsubscribe();        
      }, []);

    // get user data from backend for initial display.
    
    return (
        <UserContext.Provider value={{user, logout, signIn, createUser}}>
            {props.children}
        </UserContext.Provider>

    )
}

export default AppContext;