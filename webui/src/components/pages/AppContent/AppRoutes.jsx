import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import AppContext from "./AppContext";
import MyWorkspace from "../MyWorkspace/MyWorkspace";
import DocView from "../DocView/DocView";
import About from "../About/About";
import Chat from "../Chat/Chat";
import Signin from "../Authentication/Signin";
import Signup from "../Authentication/Signup";
import Account from "../Authentication/Account";
import ProtectedRoute from "./ProtectedRoute";
import ChatContext from "./ChatContext";
import Landing from "../Landing/Landing";
import AppHome from "../Home/AppHome";

function AppRoutes(){
    return(
        <AppContext>
            <ChatContext>
                <BrowserRouter>
                    <Routes>
                        <Route path='/home' element={<ProtectedRoute><AppHome /> </ProtectedRoute>}></Route>
                        <Route path='/about' element={<ProtectedRoute><About /> </ProtectedRoute> }></Route>
                        <Route path='/my-workspace' element={<ProtectedRoute><MyWorkspace /> </ProtectedRoute>}></Route>
                        <Route path='/doc-view/:fileName' element={<ProtectedRoute><DocView /></ProtectedRoute>}></Route> 
                        <Route path='/chat' element={<ProtectedRoute><Chat /> </ProtectedRoute>}></Route> 
                        <Route path='/' element={<Landing />}></Route>
                        <Route path='/signin' element={<Signin />}></Route>
                        <Route path='/signup' element={<Signup />}></Route>
                        <Route path='/account' element={<ProtectedRoute><Account /> </ProtectedRoute>}></Route>
                    </Routes>            
                </BrowserRouter> 
            </ChatContext>           
        </AppContext>
    )
}

export default AppRoutes;