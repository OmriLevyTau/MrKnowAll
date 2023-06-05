import { Image, Menu } from "antd";
import { useNavigate } from "react-router-dom";
import { pages } from "./MenuUtils";
import back from "../../../images/mustach3_menu.png"
import logo from "../../../images/hat.png"

function SideMenu(){
    const navigate = useNavigate();
    
    const onMenuClick = (item) => {
        navigate(`/${item.key}`)
    };

    
    const onMouseOver = (e) => {
        e.target.style.color = "#e1b2ba";
        setTimeout(() => {
            e.target.style.color = "white";
          }, 10);
    };
    

    return (
        <div 
            className="side-menu"
            style={{justifyContent:"space-between", backgroundColor:"black", width:"14%"}}
            >
            <div >
                <div className="page-menu-logo" onClick={()=>navigate('/home')} style={{marginLeft:"0%", marginTop:"5%", flexDirection:"row", justifyItems:"center"}} >
                    <Image width={70} height = {70} src={logo} preview={false} style={{marginLeft:"20%"}}/>
                    {/* <span style={{ fontWeight: 'bold', fontSize: "200%", color:"white"}}>Mr. Know All</span>  */}
                </div>
                <Menu 
                    className="side-menu" 
                    mode="inline" 
                    onClick={onMenuClick} 
                    onMouseOver={onMouseOver}
                    items={pages} 
                    style={{
                        color:"white",
                        background: 'rgba(204, 204, 204, 0.0)',
                        fontSize:"120%",
                        marginTop:"10%",
                        fontFamily:"Nunito, sans-serif",
                        marginRight:"5%"
                    }} 
                    disabledOverflow={true}
                    inlineCollapsed={false}
                />
            </div>
        </div>        
    )
};

export default SideMenu;

