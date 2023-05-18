import { SendOutlined, UploadOutlined } from "@mui/icons-material";
import { Button, Input, Modal, Upload } from "antd";
import { useContext, useState } from "react";
import { UserContext } from "../AppContent/AppContext";
import { useLocation, useNavigate } from "react-router-dom";
import { ChatLogContext } from "../AppContent/ChatContext";
import TextArea from "antd/es/input/TextArea";
import { msgResponseDict } from "./ChatDemoUtils";

function ChatInput(props) {
  const location = useLocation();
  const navigate = useNavigate();
  const { setChatLog, dataSource, setDataSource } = useContext(ChatLogContext);
  const { user } = useContext(UserContext);
  const [msg, setMsg] = useState("");
  const [msgCounter,setMsgCounter] = useState(0);
  const [waitingChatGpt, setWaitingChatGpt] = useState(false);
  const { width } = props;

  // an helper function to make delay in response
  // for testing purposes
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const messageResponder = (counter)=>{
    if (counter<2){
      return msgResponseDict[counter]
    }
    else{
      return "ChatGPT generic Answer: " + Math.random() + " " + user.email
    }
  }

  const sendMsg = async () => {
    if (msg === "") {
      return;
    }
    if (dataSource.length === 0) {
      Modal.confirm({
        title: "Mr. Know All gives you the opportunity to ask questions about your data. You should upload your files before you ask questions, so we will be able to give you answers based on them.  So, Please, upload files to your workspace, and help us help you.",        okText: "Upload",

        onOk: () => {
          navigate("/my-workspace");
        },
        style:{textAlign:"fit-content"}
      });
    } else if (location.pathname !== "chat") {
      navigate("/chat");
    }
    if (dataSource.length > 0) {
      setWaitingChatGpt(true);
      setChatLog((prevChat) => [...prevChat, { chatgpt: false, content: msg }]);
      setMsg("");
      // make an api call to the backend
      // get chatGPT answer, update the log
      await sleep(2000);
      let chatGptResponse = {
        chatgpt: true,
        content: messageResponder(msgCounter)
      };
      setMsgCounter(prev => (prev+1))
      setChatLog((prevChat) => [...prevChat, chatGptResponse]);
      setWaitingChatGpt(false);
    }
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
