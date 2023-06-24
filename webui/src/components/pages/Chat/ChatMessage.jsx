import { Avatar, Card } from "antd";
import GenericModal from "../../common/Modal/GenericModal";
import { useState } from "react";
import ChatAnswerContext from "./ChatAnswerContext";
import chatIcon from "../../../images/mr-know-all-icon.jpg"
 

 /**
  * content: {
  *   "message": "message goes here" (not null), 
  *   "ref": null | [ref1,...], 
  *   "metadata": null | {
  *     "query_content": data.query_content, 
  *     "context": data.context 
  *   }
  * }
  */

function ChatMessage(props) {
  const { chatgpt, content } = props;
  const [open, setOpen] = useState(false)

  const onCancel = () => {
    setOpen(false);
  }

  const context =  content.metadata && content.metadata.context ? content.metadata.context : null
  
  
  let contextModal =
    <GenericModal
      open={open} 
      setOpen={setOpen}
      loading={false}
      setStatus={null}
      onCancel={onCancel}
      modalButtonText="Show context"
      modalTitle={"chatGPT's answer is based on the following context from your documents."}
      modalContent={<ChatAnswerContext context={context}/>}
      buttonType={"default"}
      buttonSize={"medium"}                   
  />
  

  const avatar = chatgpt ? chatIcon : "https://xsgames.co/randomusers/avatar.php?g=pixel&key=1";
  const back = chatgpt ? "#FDF1F3" : "white";

  return (
    <Card
    bodyStyle={{ width:"100%" }}
    style={{
        width: "100%",
        display:"flex", 
        flexDirection:"row", 
        wordWrap:"anywhere",
        marginBottom:"10px",
        boxShadow: "1px 1px 1px 1px #F9F7F7",
        fontFamily:"Nunito, sans-serif",
        backgroundColor: back
    }}
  >
    <div style={{ display:"flex", flexDirection:"column", width:"100%"}}>
      <div style={{ display:"flex", flexDirection:"row", width:"100%"}}>
        <div style={{width:'25px', marginRight: '20px'}}>
          <Avatar src={avatar}  />
        </div>
        <div style={{ display:"flex", flexDirection:"column", overflowWrap: "anywhere" , fontFamily:'sans-serif', fontSize:'16px'}} >
          <p>{content.message}</p>
          {chatgpt && content.metadata && content.metadata.context ? <br/> : null}
        </div>
      </div>
      <div className="ai-context-modal" style={{ display: "flex", justifyContent:"space-between", alignItems:"end", width:"100%" }}>
        <div></div>
        {chatgpt && content.metadata && content.metadata.context ? contextModal : null}
      </div>
    </div>
  </Card>
  );
}

export default ChatMessage;
