import { Image, Card } from "antd"; 

function HomeCard(props){
    
    const {title, content, icon} = props;

    return(
            <div class="service-box">
                <div class="service-icon yellow" style={{marginLeft:"auto", marginRight:"auto"}}>
                    <div class="front-content">
                        <i class={icon}></i>
                        <h3>{title}</h3>
                    </div>
                </div>
                <div class="service-content" style={{marginLeft:"auto", marginRight:"auto"}}>
                    <h3>{title}</h3>
                    <p>{content}</p>
                </div>
            </div>
    )
    
}

export default HomeCard;
