import React from 'react'
import chat_land from "../../../images/chat_land.png"
import upload_file_land from "../../../images/upload_file_land.PNG"
import ask_land from "../../../images/ask_land.gif"

function Product({title, description, imageName, reverse}) {
    if (!reverse){
      if(imageName == "upload_file_land"){
        return(
          <div className="landing-product" style={{ display:"flex", flexDirection:"row", marginTop:"4%" }}>
            <div className="product-description" style={{display:"flex", flexDirection:"column", justifyContent:"flex-start", marginRight:"0%" }} >
              <h3 style={{fontSize: `max(20px, 1.8vw)`}} >{title}</h3>
              <p style={{fontSize: `max(16px, 1.2vw)`}} >{description}</p>
            </div>
            <div className="product-imgae"  style={{display:"flex", justifyContent:"end", width:"100%"}} >
              <img src={ upload_file_land } alt="workflow"  style={{ height:"80%", width:"80%", aspectRatio:"auto" }} />
            </div>        
          </div>
        )
      }
      else{
        if(imageName == "chat_land"){
          return(
            <div className="landing-product" style={{ display:"flex", flexDirection:"row", marginTop:"3%" }}>
              <div className="product-description" style={{display:"flex", flexDirection:"column", justifyContent:"flex-start", marginRight:"0px" }} >
                <h3 style={{fontSize: `max(20px, 1.8vw)`}} >{title}</h3>
                <p style={{fontSize: `max(16px, 1.2vw)`}} >{description}</p>
              </div>
              <div className="product-imgae"  style={{display:"flex", justifyContent:"center", width:"50%"}} >
                <img src={ chat_land } alt="workflow"  style={{ height:"70%", width:"70%", aspectRatio:"auto"}} />
              </div>        
            </div>
          )
        }
      }
      
    }
  return (
      <div className="landing-product" style={{ display:"flex", flexDirection:"row", marginTop:"3%" }}>
        <div className="product-imgae"  style={{display:"flex", justifyContent:"start", marginRight:"1.5%",}} >
          <img src={ ask_land}  alt="workflow" style={{ height:"80%", width:"80%", aspectRatio:"auto" }} />
        </div>
        <div className="product-description" style={{display:"flex", flexDirection:"column", justifyContent:"flex-start", width:"80%" }} >
          <h3 style={{fontSize: `max(20px, 1.8vw)`}} >{title}</h3>
          <p style={{fontSize: `max(16px, 1.2vw)`}} >{description}</p>
        </div>       
    </div>
  )
}

export default Product;