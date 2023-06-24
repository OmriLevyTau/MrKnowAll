import { Collapse, List } from "antd";

const { Panel } = Collapse;

function ChatAnswerContext(props){
    const {context} = props;

    return (
        <div>
            <p>
                This context was provided to chatGPT alongside your question.
            </p>
            <List
                size="small"
                bordered={false}
                dataSource={Object.entries(context)}
                renderItem={(item, index) => 
                    <List.Item>
                        <Collapse style={{width:'100%'}}>
                            <Panel header={item[0]}> 
                                {item[1]} 
                            </Panel>  
                        </Collapse>
                    </List.Item>
               }
            />
    </div>
    );

}

export default ChatAnswerContext;