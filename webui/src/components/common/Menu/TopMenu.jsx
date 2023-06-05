import { Button, Menu, Image } from "antd";
import { useNavigate } from "react-router-dom";
import { pages } from "./MenuUtils";
import { useContext, useState } from "react";
import { UserContext } from "../../pages/AppContent/AppContext";
import logo from "../../../images/hat.png"


function TopMenu(){

    const navigate = useNavigate();
    const [open, setOpen] = useState(false);
    const [loading, setLoading] = useState(false);
    const { logout } = useContext(UserContext);

    const onMenuClick = (item) => {
        navigate(`/${item.key}`)
    };

    const handleSubmit = (data) => {
        alert("Submitted: " + data);
        setOpen(false);
    };

    const handleLogout = async () => {
        try {
          await logout();
          navigate('/signin');
          console.log('You are logged out')
        } catch (e) {
          console.log(e.message);
        }
      };


    const onCancel = () => {setOpen(false)};

    return (
        <div style={{ display:'flex', flexDirection:'row',  alignItems: 'center' , padding: "2px", justifyContent:"space-between", marginRight:"20px", }}>
            <div  style={{ display:'flex', flexDirection:'row',  alignItems: 'center' , padding: "2px", width:"100%"}}>
                <div className="page-menu-logo" onClick={()=>navigate('/home')} >
                <Image width={40} height = {40} src={logo} preview={false} style={{}}/>
                    {/* <span style={{ fontWeight: 'bold' , fontSize: "30px", display:"flex"}}>Mr. Know All</span>  */}
                </div>
                <div style={{ display:'flex', flexDirection:'row',  alignItems: 'center' , padding: "0px", justifyContent:"space-between"}}>
                    <Menu 
                        className="menu-options"
                        onClick={onMenuClick}
                        mode="horizontal"
                        disabledOverflow
                        selectedKeys={[]}
                        items={pages}
                        style={{
                            fontFamily:"Nunito, sans-serif",
                            fontSize:"18px",
                        }}                       
                    />    
                </div>
            </div>   
            <Button type="primary" onClick={handleLogout} >Logout</Button>
        </div>
    )

}

export default TopMenu;