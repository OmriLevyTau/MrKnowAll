import { Button, Menu, Image } from "antd";
import { useNavigate } from "react-router-dom";
import { landingPages, pages } from "./MenuUtils";
import logo from "../../../images/hat.png"


function LandingTopMenu(){

    const navigate = useNavigate();

    const onMenuClick = (item) => {
        navigate(`/${item.key}`)
    };


    return (
        <div style={{ display:'flex', flexDirection:'row',  alignItems: 'center' , padding: "2px", justifyContent:"space-between", marginRight:"20px", }}>
            <div  style={{ display:'flex', flexDirection:'row',  alignItems: 'center' , padding: "2px", width:"100%"}}>
                <div className="page-menu-logo" onClick={()=>navigate('/')} >
                <Image width={40} height = {40} src={logo} preview={false} style={{}}/>
                </div>
                <div style={{ display:'flex', flexDirection:'row',  alignItems: 'center' , padding: "0px", justifyContent:"space-between"}}>
                    <Menu 
                        className="menu-options"
                        onClick={onMenuClick}
                        mode="horizontal"
                        disabledOverflow
                        selectedKeys={[]}
                        items={landingPages}
                        style={{
                            fontFamily:"Nunito, sans-serif",
                            fontSize:"18px",
                        }}                       
                    />    
                </div>
            </div>   
            <Button type="primary" onClick={() => navigate('/signin')} >Sign in</Button>
        </div>
    )

}

export default LandingTopMenu;