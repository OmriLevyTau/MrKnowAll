import { SendOutlined } from "@mui/icons-material";
import { Button, Modal } from "antd";
import { useContext, useState } from "react";
import { UserContext } from "../AppContent/AppContext";
import { useLocation, useNavigate } from "react-router-dom";
import { ChatLogContext } from "../AppContent/ChatContext";
import TextArea from "antd/es/input/TextArea";
import { query } from "../../../services/Api";
import useFileStore from "../MyWorkspace/store";
import {OPENAI_ERROR, SERVER_ERROR, STATUS_OK} from "../Constants";


function ChatInput(props) {
  const location = useLocation();
  const navigate = useNavigate();
  const { setChatLog, } = useContext(ChatLogContext);
  const { files, addFileToStore, removeFileFromStore } = useFileStore(); 
  const { user } = useContext(UserContext);
  const [msg, setMsg] = useState("");
  const [waitingChatGpt, setWaitingChatGpt] = useState(false);
  const { width } = props;

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

  // Send a message on chat
  // ======================================================

  const sendMsg = async () => {
    // Some basic validations.
    if (msg === "") {return;}
    if (files.length < 1) {noFilesModal();return;} 
    else if (location.pathname !== "chat") {navigate("/chat");}

    // Update chatLog with user's message
    setWaitingChatGpt(true);
    setChatLog((prevChat) => [...prevChat, { chatgpt: false, content: {"message": msg, "ref": null, "metadata": null} }]);
    setMsg("");

    // make an api call to the backend
    let chatResponse = await query({
      "user_id": user.email,
      "query_id": files.length,
      "query_content": msg
    });
   
    let chatGptResponse = {chatgpt: true,content: SERVER_ERROR}; // default.
    // check if error occured while communicating with the server
    if (chatResponse.status!==200 && chatResponse.status!==204){
      chatGptResponse = {chatgpt: true, content: {"message": SERVER_ERROR, "ref": null, "metadata": null}};
      console.log(chatResponse.data)
    }
    // Otherwise, communicating with the backend was successfull. It does *not* mean
    // communicating with the AI assitant was successfuul. 
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
      chatGptResponse = {chatgpt: true,content: content};
    }
    setChatLog((prevChat) => [...prevChat, chatGptResponse]);
    setWaitingChatGpt(false);
  };

  return (
    <div
      className="chat-input-holder"
      style={{
        width: width,
        paddingBottom: "2%",
        display: "flex",
        flexDirection: "row",
      }}
    >
      <div
        className="text-area-container"
        style={{ position: "relative", width: "100%"}}
        
      >
        <TextArea
          autoSize={{ minRows: 1, maxRows: 4 }}
          /* onPressEnter={sendMsg} */
          onChange={(e) => setMsg(e.target.value)}
          value={msg}
          placeholder="Ask me anything, and get answers based on your data!" 
          style={{
            boxSizing: "border-box",
            fontFamily: "Nunito, sans-serif",
            boxShadow: "1px 1px 1px 1px #F9F7F7",
            position: "absolute",
            fontSize: "100%",
            fontWeight: "50%",
            
          }}
        />
        <Button
          onClick={sendMsg}
          
          style={{
            display: "flex",
            float: "right",
          }}
          disabled={waitingChatGpt}
        >
          <SendOutlined style={{height:"100%" ,fontSize:"18px", borderColor:"1px transparent"}}/>
        </Button>
      </div>
    </div>
  );
}

export default ChatInput;
