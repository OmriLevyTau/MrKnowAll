import { createContext, useState, useEffect } from "react";
import {
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword,
    signOut,
    onAuthStateChanged,
    GoogleAuthProvider,
    signInWithPopup,
    setPersistence,
    browserSessionPersistence
  } from 'firebase/auth';
  import { auth } from '../Authentication/Firebase'
import useFileTableStore from "../MyWorkspace/fileStore";
import useChatStore from "../Chat/chatStore";
import { useQueryClient } from "@tanstack/react-query";
import { deleteChatHistory } from "../../../services/Api";
  
export const GoogleProvider = new GoogleAuthProvider();

export const UserContext = createContext();

function AppContext(props){
    const [user, setUser] = useState({});
    const [token, setToken] = useState("");
    const {setAllFiles} = useFileTableStore();
    const {clearChatStore} = useChatStore();
    const queryClient = useQueryClient()
  

    const clearCache = () => {
      // clear browser cache
      queryClient.clear();
      setAllFiles([]);
      clearChatStore();
      // clear chat history db
      deleteChatHistory(user.email, token);
    }

    const createUser = (email, password) => {
        clearCache();
        return createUserWithEmailAndPassword(auth, email, password);
      };
    
    const signIn = (email, password) =>  {
      clearCache();
      return signInWithEmailAndPassword(auth, email, password)
    };

    const signInWithGoogle = async () => {
      try {
        clearCache();
        const result = await signInWithPopup(auth, GoogleProvider);
      } catch (error) {
        alert(error);
      }
    };
    
    const logout = () => {
      clearCache();
      return signOut(auth)
    };
    
    useEffect(() => {
      const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
        const getToken = async (currentUser) => {
          const token = await currentUser.getIdToken(true);
          setToken(token);
        };
    
        if (currentUser) {
          getToken(currentUser);
          setUser(currentUser);
        } else {
          setUser("");
        }
      });
    
      // Set session-based persistence
      setPersistence(auth, browserSessionPersistence)
        .then(() => {
          // Persistence set successfully
        })
        .catch((error) => {
          console.log(error);
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