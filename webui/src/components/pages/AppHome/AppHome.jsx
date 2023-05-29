import { Button, Image, Space } from "antd";
import GenericCard from "../../common/Card/GenericCard"
import ChatInput from "../Chat/ChatInput";
import TopMenu from "../../common/Menu/TopMenu";
import HomeCard from "../../common/Card/HomeCard";

function AppHome(){

    return(
        <div className="generic-page-holder">
            <TopMenu />
            <div className="home-layout">
                <div className="home-header">
                
                    <div className="home-header-search" style={{marginBottom:"0%", marginTop:"10%", display:"flex", flexDirection:"column", alignItems:"center"}}>                    
                        <h2 className = "home-header-title" >What do you want to know?</h2>
                        <ChatInput width={"50%"} />
                        
                    </div>
                    {/*}
                    <div className = "home-header-checkbox">
                        <label><input type="checkbox" /> Do you want to search online? </label >
                    </div>   
                    */}               
                    <div className="home-header-description" />                        
                </div>
                <div className="home-page-content" style={{ justifyItems:"center"}} >
                    <div className="cards-row" style={{width:"40%", marginLeft:"auto", marginRight:"auto", maxHeight:"250%", marginTop:"2%"}}>
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
                    {/* <div className="image" style={{display:"flex", marginBottom:"2%", }}> */}       
                </div>
            </div>
        </div>
    )

};

export default AppHome;

/*
<Image.PreviewGroup>
    <div className="site-card-wrapper" style={{display:"flex", flexDirection:"row"}}>
        <Space direction="horizontal" size="middle" style={{ display: 'flex' }} >

            <GenericCard 
                title="Explore"
                imageName={image2}
                content="Search content related to the subjects you are interested in, or that can help you."
            />
    
            <GenericCard 
                title="Know"
                imageName={image1}
                content="Ask what you want to know, we will give you best answer we can."
            />
    
            <GenericCard 
                title="Upload"
                imageName={image3}
                content="Upload your files, that you will be able to use and filter in the future."
            />
        
        </Space>
    </div>
</Image.PreviewGroup>
*/
