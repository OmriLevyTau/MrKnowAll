import { Button, Image, Menu, Modal } from "antd";
import { useNavigate } from "react-router-dom";
import { pages } from "./MenuUtils";
import logo from "../../../images/hat.png"
import useChatStore from "../../pages/Chat/chatStore";
import { deleteChatHistory } from "../../../services/Api";
import { useContext } from "react";
import { UserContext } from "../../pages/AppContent/AppContext";
import { DeleteOutlined } from "@mui/icons-material";
import GenericModal from "../Modal/GenericModal";


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

    const onNewHere = () => {
        Modal.warn({
            title: "Hi! I'm Mr. Know all, and I'm here to help.",
            content: <div style={{ wordBreak:"break-word", width:"100%" }}>
                Here are some tips to find your way here:<br/><br/>
                <h5>1. Upload your files</h5>
                <ul>
                    <li>
                    It may take a few seconds to minutes. You can read about the process in the About section.<br/><br/>
                    </li>
                </ul>
                <h5>2. Don't ask to ask. just ask.</h5>
                <ul>
                    <li><b>Don't:</b><i> "Hi, how are you? Recently I got interested in history and became quite an expert,
                        but I can't find the answer to a question I have. Maybe you can help me...<br/> Do you know when WW2 started?"</i></li>
                    <li style={{ marginTop:"2px" }} ><b>Do:</b> <i>"When did WW2 start?"</i></li>
                </ul>
            </div>
        })
    }
    

    return (
    <div className="side-menu" style={{ backgroundColor: "black", width: "200px", display: "flex", flexDirection: "column" }}>
        <div className="page-menu-logo" onClick={() => navigate('/home')} style={{ marginLeft: "0%", marginTop: "5%", display: "flex", flexDirection: "row", justifyItems: "center" }}>
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
                flex: 1, // Expand the menu to take remaining space
            }}
            disabledOverflow={true}
            inlineCollapsed={false}
        />
        <div style={{ alignSelf: "center", marginBottom: "28%" }}> {/* Align to bottom and adjust marginBottom */}
            <Button type="primary" onClick={onNewHere} style={{ display:"flex", 
                flexDirection:"row", marginBottom:"20%", width:"100%", justifyContent:"center" }}>
                <p>New here?</p>
            </Button>
            <Button type="default" onClick={onClearChat} style={{ display:"flex", flexDirection:"row", width:"100%" }}>
                <DeleteOutlined style={{ alignSelf:"center" }} />
                <p>Clear chat</p>
            </Button>
        </div>
    </div> 
    )
};

export default SideMenu;

