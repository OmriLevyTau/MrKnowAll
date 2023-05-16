import TopMenu from "../../common/Menu/TopMenu";
import imageAbout from "../../../images/workflow-ask.png"
import { Button } from "antd";
import { useNavigate } from "react-router-dom";


function About(){

    const navigate = useNavigate();
    
    const onClick = (item) => {
        navigate(`/home`)
    };
    
    return (
        <div className="generic-page-holder">
            <TopMenu />
            <div class="responsive-container-block bigContainer">
                <div class="responsive-container-block Container bottomContainer">
                    <img class="mainImg" src={imageAbout}/>
                    <div class="allText bottomText">
                    <p class="text-blk headingText">
                        Our Vision
                    </p>
                    <p class="text-blk subHeadingText">
                        you probably ask yourself how can we help you. good question!
                    </p>
                    <p class="text-blk description">
                        In today's reality, organizations need to manage and restore huge amounts of data. But, the current tools are not enough, and this is why we are here.
                        <br/><br/>
                        Mr. Know All allows you to upload your data and store it.
                        Once uploaded, you can immediately access an AI assistant that can answer your questions - based on your data. 
                        <br/><br/> 
                        behind the scenes, we break your document into sentences, embed each one into a vector using a dedicated pipeline, 
                        and store them in a vector database that is best suited for semantic search."
                        <br/><br/> 
                        when you ask a question, We retrieve the most relevant data from the vector database and inject it into ChatGPT along with your question. 
                        Then, we prompt the system to generate the best answer based on your data, and you get it - the best answer based on your data!
                    </p>
                    <Button type="primary" key="submit" size="large" style={{marginBottom:"4%" ,marginLeft:"2%"}} onClick={onClick}>Let us begin!</Button>
                    </div>
                </div>
            </div>    
                        
        </div>
    )
}

export default About;


