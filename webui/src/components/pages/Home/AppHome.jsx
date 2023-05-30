import { Button, Collapse } from "antd";
import HomeCard from "../../common/Card/HomeCard";
import mustach from "../../../images/mustach-home2.png"
import { CloudUploadOutlined, QuestionAnswerOutlined, QuestionMarkSharp } from "@mui/icons-material";

import { useNavigate } from "react-router-dom";
import { useContext } from "react";
import { UserContext } from "../AppContent/AppContext";
import TopMenu from "../../common/Menu/TopMenu";
import ChatInput from "../Chat/ChatInput";
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
            <TopMenu/>
            <div style={{ justifyContent:"space-evenly", width:"100%", display:"flex", flexDirection:"column", alignItems:"center", }} >
                <div style={{ display:"flex", flexDirection:"row", background:"black", height:"50%" }}>
                    <div style={{background:"black", marginRight:"2%"}}>
                        <img src={ mustach} alt="mustach" width="100%" />
                    </div>
                    <div  style={{ display:"flex", flexDirection:"column", width:"100%", height:"100%", justifyContent:"flex-start", marginRight:"3%", marginTop:"10%"}} >
                        <div style={{ textAlign:"left", wordWrap:"break-word", color:"white" }} >
                            <h1 style={{ fontSize: `max(24px, 2.75vw)`,   fontFamily: "Nunito, sans-serif", fontWeight:"bold"}} >Mr. Know All <br /> your new AI powered assitant.</h1>
                        </div>
                        <div style={{ textAlign:"left", wordWrap:"break-word", color:"white", marginTop:"2%" }} >
                            <p style={{ fontSize: `max(18px, 1.5vw)`,  fontFamily: "Nunito, sans-serif"}} >A tailor made chatGPT assitant, based on your data - and for your purpose.</p>
                        </div>
                    </div>
                </div>
                <div className="new-home-layout" style={{backgroundColor:'black', width:"100%", marginTop:'0%'}}>
                    <div className="new-home-header-search" style={{marginBottom:"0%", marginTop:"0%", display:"flex", flexDirection:"column", alignItems:"center"}}>                    
                        <h2 className = "new-home-header-title" style={{color:'white',  fontFamily: "Nunito, sans-serif"}} >Ask me anything.. about your data!</h2>
                        <ChatInput width={"55%"} />
                    </div>
                </div>
                <div className="image" style={{width:"50%", marginBottom:"3%", display:"flex", flexDirection:"row", marginTop:"2%", justifyItems:"center"}}>
                    <HomeCard
                        title="Search"
                        content="Search content related to the subjects you are interested in, or that can help you."
                        icon="fa fa-search fa-3x"
                    />
                    <HomeCard  
                        title="Chat"
                        content="Ask what you want to know, we will give you best answer we can."
                        icon="fa fa-comments fa-3x"
                    />
                    <HomeCard  
                        title="Upload"
                        content="Upload your files, that you will be able to use and filter in the future."
                        icon="fa fa-cloud-upload fa-3x"
                    />
                </div>
                <div className="home-page-content" style={{width:"80%", alignItems:"center", display:"flex", flexDirection:"column"}}>
                     <div style={{ textAlign:"center", wordWrap:"break-word", color:"black", width:"80%",
                        letterSpacing:"1px", fontSize:`max(20px, 1.5vw)`, fontWeight:"450", marginBottom:"3%" }} >
                        
                    </div>
                    
                </div>
                
            </div>

            
        </div>
    )

};

export default Landing;