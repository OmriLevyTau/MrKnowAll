import { Avatar, Card } from "antd";
import GenericModal from "../../common/Modal/GenericModal";
import { useState } from "react";
import ChatAnswerContext from "./ChatAnswerContext";

 

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
  />
  

  const avatar = chatgpt ? "1" : "2";
  const back = chatgpt ? "#FDF1F3" : "white";

  return (
    <Card
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
    <div style={{ display:"flex", flexDirection:"row", }}>
      <div style={{width:'25px', marginRight: '20px'}}>
        <Avatar src={"https://xsgames.co/randomusers/avatar.php?g=pixel&key="+avatar}  />
      </div>
      <div style={{ display:"flex", flexDirection:"column", overflowWrap: "anywhere" , fontFamily:'sans-serif'}} >
        <p>{content.message}</p>
        <br/>
        <div className="ai-context-modal" style={{ display: "flex", justifyContent: "flex-end", alignContent: "start" }}>
        {chatgpt && content.metadata && content.metadata.context ? contextModal : null}
        </div>
      </div>
    </div>
  </Card>
  );
}

export default ChatMessage;
