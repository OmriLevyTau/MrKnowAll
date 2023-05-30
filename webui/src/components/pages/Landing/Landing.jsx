import { Button, Collapse } from "antd";
import mustach from "../../../images/mustach3.png"
import LandingCard from "./LandingCard";
import  Product  from "./Product";
import { CloudUploadOutlined, QuestionAnswerOutlined, QuestionMarkSharp } from "@mui/icons-material";
import LandingTopMenu from "../../common/Menu/LandingTopMenu";

import { useNavigate } from "react-router-dom";
import { useContext } from "react";
import { UserContext } from "../AppContent/AppContext";
const { Panel } = Collapse;

function Landing(){
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
            <LandingTopMenu />
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
                    <LandingCard 
                        title="Upload"
                        content="Upload your files"
                        icon={<CloudUploadOutlined style={{fontSize:`max(18px, 4vw)`}} />}
                    />
                    <LandingCard 
                        title="Ask"
                        content="Ask anything "
                        icon={<QuestionMarkSharp style={{fontSize:`max(18px, 4vw)`}} />}
                    />
                    <LandingCard 
                        title="Chat"
                        content="Chat with your new AI assitant"
                        icon={<QuestionAnswerOutlined style={{fontSize:`max(18px, 4vw)`}} />}
                    />
                </div>
                <div className="home-page-content" style={{width:"80%", alignItems:"center", display:"flex", flexDirection:"column"}}>
                    <h2 style={{textAlign:"center", fontSize: `max(24px, 3vw)`, marginBottom: '4%'}}>TLDR - who is Mr. Know All?</h2>
                     <div style={{ textAlign:"center", wordWrap:"break-word", color:"black", width:"80%",
                        letterSpacing:"1px", fontSize:`max(20px, 1.5vw)`, fontWeight:"450", marginBottom:"3%" }} >
                        <p>
                            Aren't you tired of wasting time, searching for a specific sentence, in a specific line,<br></br> in a specific folder, too many times a day? <br></br> <br></br>
                            Instead of wasting so much efforts and time, wouldn't you prefer to ask someone a question, and get an answer, based solely on yor data and files? <br></br> <br></br>
                            This is exactly what Mr. Know All is here for! <br></br>
                            We know, pretty awesome. <br></br> <br></br>
                            Mr. Know All allows you to upload your data and store it. <br/><br/>
                            Once uploaded, you can immediately access an AI assistant that can answer your questions - based on your data. <br/><br/> 
                            
                        </p>
                    </div>
                    <h2 style={{textAlign:"center", fontSize: `max(24px, 3vw)`}}>How can you work with Mr. Know All?</h2>
                    <div className="landing-products-holder" style={{ display:"flex", flexDirection:"column", width:"100%", alignItems:"center", marginBottom:"10%", justifyContent:"space-between" }}>
                        
                        <div>
                            <Product 
                                title="Upload files or documents"
                                description="We are excited to introduce a feature that empowers you to effortlessly upload the files you'd like to receive valuable responses on. To take advantage of this functionality, simply navigate to `My Workspace` and conveniently locate the designated upload button. Feel free to upload any files that pique your interest, as these are the very files our system will provide comprehensive answers and insights on."
                                imageName="upload_file_land"
                                reverse={false} />
                        </div>
                        <div>
                            <Product 
                                title="Ask a question" 
                                description="After you uploaded your files, you may ask any questions you want. You will be sent to the chat page, and Mr. Know All will give you answers, based on the data which is located in the files you uploaded. you can chat with him, ask further questions, and enjoy. For further technicall details, go to the About page after you sign up or login."
                                imageName="ask_land" 
                                reverse={true} />
                        </div>
                        <div >
                            <Product 
                                title="Chat with AI assistant"
                                description=
                                "After uploading a file, you can ask questions about it. Once you receive a response to any of your questions, you can ask follow-up questions and engage in a chat with our AI assistant."
                                imageName="chat_land"
                                reverse={false}
                                 />
                        </div>
                    </div>
                </div>
                <div style={{ width:"60%", justifyContent:"center", alignItems:"center", display:"flex", marginBottom:"5%" }}>
                    <Button size="large" shape="round" type="primary" onClick={handleLetsStart} style={{width:"30%", height: "100%"}}>
                         Let's start!
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

export default Landing;