import { Button, Image, Menu, Modal } from "antd";
import { useNavigate } from "react-router-dom";
import { pages } from "./MenuUtils";
import logo from "../../../images/hat.png"
import useChatStore from "../../pages/Chat/chatStore";
import { deleteChatHistory } from "../../../services/Api";
import { useContext } from "react";
import { UserContext } from "../../pages/AppContent/AppContext";

function SideMenu(props){
    const navigate = useNavigate();
    const {clearChatStore} = useChatStore();
    const {waitingChatGpt } = props;
    const { user, token } = useContext(UserContext);
    
    const onMenuClick = (item) => {
        navigate(`/${item.key}`)
    };


    const onClearChat = () => {
        Modal.confirm({
            title: "Are you sure you want to clear chat?",
            okText: "yes",
            cancelText: "No",
            okType: "danger",
            onOk: () => {
                if (waitingChatGpt){
                    alert("Cannot clear chat while waiting for response.")
                    return;
                }
                deleteChatHistory(user.email, token);
                clearChatStore();
            },
            });
    }
    

    return (
        
        <div className="side-menu" style={{ justifyContent: "space-between",alignItems:"center" ,backgroundColor: "black", width: "14%", display: "flex", flexDirection: "column" }}>
            <div>
                <div className="page-menu-logo" onClick={() => navigate('/home')} style={{ marginLeft: "0%", marginTop: "5%", flexDirection: "row", justifyItems: "center" }}>
                    <Image width={70} height={70} src={logo} preview={false} style={{ marginLeft: "20%" }} />
                </div>
                <Menu
                className="side-menu"
                mode="inline"
                onClick={onMenuClick}
                items={pages}
                style={{
                    color: "white",
                    background: 'rgba(204, 204, 204, 0.0)',
                    fontSize: "120%",
                    marginTop: "10%",
                    fontFamily: "Nunito, sans-serif",
                    marginRight: "5%"
                }}
                disabledOverflow={true}
                inlineCollapsed={false}
                />
            </div>
            <div style={{ marginBottom:"10%" }}>
                <Button type="primary" onClick={onClearChat} >Clear chat</Button>
            </div>
        </div>

        // <div 
        //     className="side-menu"
        //     style={{justifyContent:"space-between", backgroundColor:"black", width:"14%", display: "flex", flexDirection: "column"}}
        //     >
        //     <div >
        //         <div className="page-menu-logo" onClick={()=>navigate('/home')} style={{marginLeft:"0%", marginTop:"5%", flexDirection:"row", justifyItems:"center"}} >
        //             <Image width={70} height = {70} src={logo} preview={false} style={{marginLeft:"20%"}}/>
        //             {/* <span style={{ fontWeight: 'bold', fontSize: "200%", color:"white"}}>Mr. Know All</span>  */}
        //         </div>
        //         <Menu 
        //             className="side-menu" 
        //             mode="inline" 
        //             onClick={onMenuClick} 
        //             onMouseOver={onMouseOver}
        //             items={pages} 
        //             style={{
        //                 color:"white",
        //                 background: 'rgba(204, 204, 204, 0.0)',
        //                 fontSize:"120%",
        //                 marginTop:"10%",
        //                 fontFamily:"Nunito, sans-serif",
        //                 marginRight:"5%"
        //             }} 
        //             disabledOverflow={true}
        //             inlineCollapsed={false}
        //         />
        //         <Button type="primary" >Clear chat</Button>
        //     </div>
        // </div>        
    )
};

export default SideMenu;

