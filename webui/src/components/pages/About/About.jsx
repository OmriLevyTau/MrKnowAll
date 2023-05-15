import TopMenu from "../../common/Menu/TopMenu";
import imageAbout from "../../../images/about.jpg"
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
                        We want to allow every employee get all the best answers for every question he has, based on the materials of the organization, and his specifically.
                        We are here to give you the option to ask questions, and get the answers you are looking for. 
                        And what if the organization doesn't have the answer?  we also provide the option to search online, using chatGPT! 
                    </p>
                    <Button type="primary" key="submit" size="large" style={{marginBottom:"4%" ,marginLeft:"2%"}} onClick={onClick}>Let us begin!</Button>
                    </div>
                </div>
            </div>    
                        
        </div>
    )
}

export default About;


