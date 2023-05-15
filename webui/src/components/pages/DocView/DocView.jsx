import { Navigate, useNavigate, useParams } from "react-router-dom";
import { Button } from "antd";
import backArrow from "../../../images/back-arrow.png"

function DocView() {

    let {fileName} = useParams();
    const navigate = useNavigate()
    
    let file = null;
    try {
        file = require("./"+fileName+".pdf");
    } catch (e) {
        alert("File does not exist! " + e.message);
        return <Navigate to='/my-workspace' replace={true} />;
    }
    
    return (
        <div className="doc-view" style={{overflow:"hidden"}}>
            <div className="doc-actions" style={{display:"flex",flexDirection:"row",backgroundColor:"rgb(50,50,50)",height:"7vh" }}>
                <div style={{position:"absolute",left:"40%",paddingTop:"1%"}}>
                    <font size="+1" style={{color:"white"}} >{fileName}</font>
                </div>
                <Button color="rgb(50,50,50)" onClick={()=>navigate("/my-workspace")} style={{left:"87%", top:"20%"}}> 
                <img src={backArrow} style={{height:"100%",width:"100%"}}/>
                </Button>
            </div>
            <object  data={file+ "#zoom=140&scrollbar=0&toolbar=0&navpanes=0" } style={{width:"100vw",height:"100vh"}}/> 
        </div>
    );
}

export default DocView;