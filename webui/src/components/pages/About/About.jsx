import { Button, Collapse } from "antd";
import ProductAbout from "./ProductAbout";
import mustach from "../../../images/mustach3.png"
import AboutCard from "./AboutCard";
import { CloudUploadOutlined, QuestionAnswerOutlined, QuestionMarkSharp } from "@mui/icons-material";
import TopMenu from "../../common/Menu/TopMenu";

import { useNavigate } from "react-router-dom";
import { useContext } from "react";
import { UserContext } from "../AppContent/AppContext";
const { Panel } = Collapse;

function About(){
    const navigate = useNavigate();
    const { user } = useContext(UserContext);

    const handleLetsStart = () => {
        if (!user){
            navigate('/signin')
        }
        navigate('/home')
    }


    return(
        <div className="generic-page-holder" >
            <TopMenu />
            <div style={{ justifyContent:"space-evenly", width:"100%", display:"flex", flexDirection:"column", alignItems:"center" }} >
                <div style={{ display:"flex", flexDirection:"row", background:"black", height:"100%" }}>
                    <div style={{background:"black", marginRight:"2%"}}>
                        <img src={ mustach} alt="mustach" width="130%" />
                    </div>
                    <div  style={{ display:"flex", flexDirection:"column", width:"100%", height:"100%", justifyContent:"flex-start", marginRight:"3%", marginTop:"10%" }} >
                        <div style={{ textAlign:"left", wordWrap:"break-word", color:"white" }} >
                            <h1 style={{ fontSize: `max(24px, 3vw)` }} >Meet Mr. Know All <br /> your new AI powered assitant.</h1>
                        </div>
                        <div style={{ textAlign:"left", wordWrap:"break-word", color:"white", marginTop:"2%" }} >
                            <p style={{ fontSize: `max(18px, 1.5vw)` }} >A tailor made chatGPT assitant, based on your data - and for your purpose.</p>
                        </div>
                     </div>
                </div>
                <div className="image" style={{width:"100%", marginBottom:"3%", display:"flex", flexDirection:"row", marginTop:"2%", justifyItems:"center"}}>
                    <AboutCard 
                        title="Upload"
                        content="Upload your files"
                        icon={<CloudUploadOutlined style={{fontSize:`max(18px, 4vw)`}} />}
                    />
                    <AboutCard 
                        title="Ask"
                        content="Ask anything "
                        icon={<QuestionMarkSharp style={{fontSize:`max(18px, 4vw)`}} />}
                    />
                    <AboutCard 
                        title="Chat"
                        content="Chat with your new AI assitant"
                        icon={<QuestionAnswerOutlined style={{fontSize:`max(18px, 4vw)`}} />}
                    />
                </div>
                <div className="home-page-content" style={{width:"80%", alignItems:"center", display:"flex", flexDirection:"column"}}>
                     <div style={{ textAlign:"center", wordWrap:"break-word", color:"black", width:"80%",
                        letterSpacing:"1px", fontSize:`max(20px, 1.5vw)`, fontWeight:"450", marginBottom:"3%" }} >
                        <p>
                            Mr. Know All allows you to upload your data and store it.
                            Once uploaded, you can immediately access an AI assistant that can answer your questions -
                            based on your data. <br/><br/> It's a chatGPT level AI assistant on the most recent data and without the need of training your own model.
                        </p>
                    </div>
                    <h2 style={{textAlign:"center", fontSize: `max(24px, 3vw)`}}>So, How this magic works?</h2>
                    <div className="landing-products-holder" style={{ display:"flex", flexDirection:"column", width:"100%", alignItems:"center", marginBottom:"10%", justifyContent:"space-between" }}>
                        <div >
                            <ProductAbout 
                                title="Upload data"
                                description="We break your documents into sentences, embed each one into a vector using a dedicated pipeline. 
                                Finally, we store them in a vector database that is best suited for semantic search."
                                imageName="img1"
                                reverse={false}
                                 />
                        </div>
                        <div>
                            <ProductAbout 
                                title="Ask a question" 
                                description="We retrieve the most relevant data from the vector database and inject it into ChatGPT along with your question. 
                                Then, we prompt the system to generate the best answer based on your data.
                                " 
                                imageName="img2" 
                                reverse={true} />
                        </div>
                    </div>
                </div>
                <div style={{ width:"60%", justifyContent:"center", alignItems:"center", display:"flex", marginBottom:"5%" }}>
                    <Button size="large" shape="round" type="primary" onClick={handleLetsStart} >
                         return to home page, and ask a question!
                    </Button>
                </div>
            </div>

            <div style={{ background:"rgba(236, 235, 235, 0.3)", paddingBottom: "3%", paddingTop:"1%", }}>
                <h2 style={{textAlign:"center", fontSize: "2vw"}}>Frequently Asked Questions</h2>
                <Collapse style={{ margin:"3%", alignContent:"center",  fontSize:`max(16px,0.9vw)` }}  >
                    <Panel style={{background:"rgba(201,199,199, 0.2) ", opacity:"0.95", marginBottom:"0.5%"}} header="Do you train a model just for me?" key="1">
                        <p>No,we extract the most relevant data for your question, using a similarity search over 
                            your data. Then, we redirect your qeustion to OpenAI's chatGPT 3.5 with the most relevant
                            data we found. Then chatGPT answers your question based on the data we provided to it.
                        </p>
                    </Panel>
                    <Panel style={{background:"rgba(201,199,199, 0.2) ", opacity:"0.95", marginBottom:"0.5%"}} header="What about privacy? What can I upload?" key="2">
                        <p>Upload anything you'd let chatGPT see.</p>
                    </Panel>
                    <Panel style={{background:"rgba(201,199,199, 0.2) ", opacity:"0.95", marginBottom:"0.5%"}} header="What kind of documents you support?" key="3">
                        <p> Currently doc, docx and pdf. </p>
                    </Panel>
                </Collapse>
            </div>
        </div>
    )

};

export default About;