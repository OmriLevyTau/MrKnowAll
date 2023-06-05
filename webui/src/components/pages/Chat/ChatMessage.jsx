import { Avatar, Card } from "antd";

 

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
        {chatgpt && content.ref ? "Based-on: " + content.ref : null}        
      </div>
    </div>
  </Card>
  );
}

export default ChatMessage;
