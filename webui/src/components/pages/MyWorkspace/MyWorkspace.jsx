import { useContext } from "react";
import SideMenu from "../../common/Menu/SideMenu";
import FileTable from "../../common/Table/Table";
import { UserContext } from "../AppContent/AppContext";

function MyWorkspace() {

  const { user } = useContext(UserContext);
  
  return (
    <>
      <div
        style={{
          display: "flex",
          flexDirection: "row",
          background: "white",
          height: "100%",
          width: "flex-grow",
        }}
      >
        <SideMenu />
        <div
          style={{
            flexGrow: 1,
            width: "100%",
            height: "100%",
            borderLeft: "15px white solid",
            overflowY: "visible",
          }}
        >
          <div
            style={{
              alignItems: "center", 
              fontFamily:"Nunito, sans-serif",
              fontSize: "180%",
            }}
          >
            {/* <h1>{user && user.email.split("@")[0]}-workspace</h1> */}
            <h1 style={{textAlign:"center" , width:"97%", fontSize:"200%", fontWeight:800, marginBottom:"1%"}}>my workspace</h1>
          </div>
          <FileTable></FileTable>
        </div>
      </div>
    </>
  );
}

export default MyWorkspace;
