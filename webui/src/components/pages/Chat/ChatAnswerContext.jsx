import { Button, Collapse, List } from "antd";
import { useNavigate } from "react-router-dom";

const { Panel } = Collapse;

function ChatAnswerContext(props){
    const {context} = props;
    const navigate = useNavigate();


    const onClick = (doc_id) => {
        navigate("/doc-view/" + doc_id)
    }

    
    return (
        <div>
            <p>
                It is the most relevant data for your question, based on your documents.
            </p>
            <List
                size="small"
                bordered={false}
                dataSource={Object.entries(context)}
                renderItem={(item, index) => 
                    <List.Item>
                        <Collapse style={{width:'100%'}}>
                            <Panel header={item[0]}>
                                <div style={{ display:"flex", flexDirection:"column", width:"100%", height: "300px" }}> 
                                    <pre style={{ background:"inherit", width:"100%", overflowY:"scroll",
                                        overflowX: "hidden", whiteSpace: "pre-wrap", border:"none"}}>
                                        {item[1]}
                                    </pre>
                                    <div style={{ display: "flex", justifyContent:"end", alignItems:"end", width:"100%"  }} >
                                        <Button onClick={() => onClick(item[0])} >Jump to Source</Button>
                                    </div>
                                </div>
                            </Panel>
                        </Collapse>
                    </List.Item>
               }
            />
    </div>
    );

}

export default ChatAnswerContext;