import { SendOutlined } from "@mui/icons-material";
import { Button, Modal, Select, Space } from "antd";
import { useContext, useState } from "react";
import { UserContext } from "../AppContent/AppContext";
import { useLocation, useNavigate } from "react-router-dom";
import TextArea from "antd/es/input/TextArea";
import { query } from "../../../services/Api";
import { LoadingOutlined } from "@ant-design/icons";
import useFileStore from "../MyWorkspace/fileStore";
import {OPENAI_ERROR, SERVER_ERROR, STATUS_OK} from "../Constants";
import useChatStore from "./chatStore";


function ChatInput(props) {
  const location = useLocation();
  const navigate = useNavigate();
  const {addMsgToStore, removeLastMsgFromStore} = useChatStore();
  const { files, addFileToStore, removeFileFromStore } = useFileStore(); 
  const { user , token} = useContext(UserContext);
  const [msg, setMsg] = useState("");
  const [waitingChatGpt, setWaitingChatGpt] = useState(false)
  const { width, withAdvancedFiltering } = props;
  const [selectedFilesFiltering, setSelectedFilesFiltering] = useState([])


  // Helpers and configs
  // ======================================================
  const noFilesModal = () => {
    Modal.confirm({
      title: "Mr. Know All gives you the opportunity to ask questions about your data. You should upload your files before you ask questions, so we will be able to give you answers based on them.  So, Please, upload files to your workspace, and help us help you.",        okText: "Upload",
      onOk: () => {
        navigate("/my-workspace");
      },
      style:{textAlign:"fit-content"}
    });
    setMsg("");
  }

  const onAddFileFiltering = (e) =>{
    setSelectedFilesFiltering(prev => e);
  }

  // Send a message on chat
  // ======================================================

  const sendMsg = async () => {
    // Some basic validations.
    
    if (msg === "") {return;}
    if (files.length < 1) {noFilesModal();return;} 
    else if (location.pathname !== "chat") {navigate("/chat");}

    // Update chatLog with user's message
    setWaitingChatGpt(true);
    addMsgToStore({ chatgpt: false, content: {"message": msg, "ref": null, "metadata": null}});
    setMsg("");
    addMsgToStore({chatgpt: true,content: {"message": <LoadingOutlined style={{ color: "black" }} /> , "ref": null, "metadata": null}})

    const userQuery = {
      "user_id": user.email,
      "query_id": files.length,
      "query_content": msg.trim(),
    }

    if (selectedFilesFiltering && selectedFilesFiltering.length > 0){
      userQuery["advanced_filtering"] = {"document_id": {"$in": selectedFilesFiltering}}
    }

    // make an api call to the backend
    let chatResponse = await query(userQuery, token);
   
    let chatGptResponse = {chatgpt: true,content: SERVER_ERROR}; // default.
    // check if error occured while communicating with the server
    if (chatResponse.status!==200 && chatResponse.status!==204){
      chatGptResponse = {chatgpt: true, content: {"message": SERVER_ERROR, "ref": null, "metadata": null}};
    }
    // Otherwise, communicating with the backend was successfull. It does *not* mean
    // communicating with the AI assistant was successfuul. 
    else if ( chatResponse.data.response.status != STATUS_OK){
      chatGptResponse = {chatgpt: true,content: {"message": SERVER_ERROR, "ref": null, "metadata": null}};
    }
    // Happy flow
    else {
      let responseData = chatResponse.data
      let content = {
        "message": responseData.response.content, 
        "ref": responseData.references, 
        "metadata": {"query_content": responseData.query_content, "context": responseData.context }
      }
      console.log(content);
      chatGptResponse = {chatgpt: true, content: content};
    }
    removeLastMsgFromStore();
    addMsgToStore(chatGptResponse);
    setWaitingChatGpt(false);
  };

  const Selection =       
  <Select 
    mode="multiple" 
    allowClear 
    options={files.map(item => ({value: item.name, label: item.name}))} 
    style={{ width: '20%' }} 
    placeholder="Filter files"
    onChange={onAddFileFiltering}
    maxTagCount={1}
    maxTagTextLength={12}
    disabled={waitingChatGpt}
  />

  return (
    <div className="chat-input-holder" style={{ width: width, marginBottom: "30px",display: "flex",flexDirection: "row",}}>
      <div className="text-area-container" style={{ position: "relative", width: "100%"}}>
        <TextArea
          autoSize={{ minRows: 1, maxRows: 2 }}
          /* onPressEnter={sendMsg} */
          onChange={(e) => setMsg(e.target.value)}
          value={msg}
          placeholder="Ask anything!" 
          style={{
            boxSizing: "border-box",
            fontFamily: "Nunito, sans-serif",
            boxShadow: "1px 1px 1px 1px #F9F7F7",
            position: "absolute",
            fontSize: "100%",
            fontWeight: "50%",            
          }}
        />
        <Button onClick={sendMsg} style={{display: "flex",float: "right",}} disabled={waitingChatGpt} >
          <SendOutlined style={{height:"100%" ,fontSize:"18px", borderColor:"1px transparent"}}/>
        </Button>
      </div>
      { withAdvancedFiltering ? Selection : null}
    </div>

  );
}

export default ChatInput;
