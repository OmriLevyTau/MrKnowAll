import { Avatar, Card } from "antd";

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
      <Avatar src={"https://xsgames.co/randomusers/avatar.php?g=pixel&key="+avatar} style={{marginRight:"10px"}} />
      <div style={{ display:"flex", flexDirection:"row", overflowWrap: "anywhere" }} >
        {content}
      </div>
    </div>
  </Card>
  );
}

export default ChatMessage;
