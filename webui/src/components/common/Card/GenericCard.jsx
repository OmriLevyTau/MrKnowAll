import { Image, Card } from "antd"; 

function GenericCard(props){
    
    const {title, imageName, content, width} = props;

    return(
        <Card
            hoverable
            title={title} 
            headStyle={{background:"#F9F7F7"}}
            bordered={false} 
            style={{width:230, textAlign:"center", justifyContent: 'center', whiteSpace: "pre-line" , display: "flex", flexDirection: "column"}}>
            <Image className="icons" width={70} height = {70} src={imageName} preview={false} />
            <br />
            {content}
        </Card>
    )
    
}

export default GenericCard;
