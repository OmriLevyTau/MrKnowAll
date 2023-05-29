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


    const createUser = (email, password) => {
        return createUserWithEmailAndPassword(auth, email, password);
      };
    
    const signIn = (email, password) =>  {
    return signInWithEmailAndPassword(auth, email, password)
    };

    const signInWithGoogle = () => {
      return signInWithPopup(auth, GoogleProvider)
      .then((result) => {
        console.log(result);
      })
      .catch((error) => {
        console.log(error);
      })
    };
    
    const logout = () => {
        return signOut(auth)
    };
    
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
        <UserContext.Provider value={{user, logout, signIn, signInWithGoogle, createUser}}>
            {props.children}
        </UserContext.Provider>

    )
}

export default AppContext;