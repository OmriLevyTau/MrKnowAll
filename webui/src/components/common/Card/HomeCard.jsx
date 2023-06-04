import { Image, Card } from "antd"; 

function HomeCard(props){
    
    const {title, content, icon} = props;

    return(
            <div className="service-box">
                <div className="service-icon yellow" style={{marginLeft:"auto", marginRight:"auto"}}>
                    <div className="front-content">
                        <i className={icon}></i>
                        <h3>{title}</h3>
                    </div>
                </div>
                <div className="service-content" style={{marginLeft:"auto", marginRight:"auto"}}>
                    <h3>{title}</h3>
                    <p>{content}</p>
                </div>
            </div>
    )
    
}

export default HomeCard;
