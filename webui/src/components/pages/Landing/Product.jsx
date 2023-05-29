import React from 'react'
import step1_signup from "../../../images/step1_signup.jpg"
import step2_upload from "../../../images/step2_upload.jpg"
import step3_chat from "../../../images/step3_chat.jpg"

function Product({title, description, imageName, reverse}) {
    if (!reverse){
      if(imageName == "step1_signup"){
        return(
          <div className="landing-product" style={{ display:"flex", flexDirection:"row", marginTop:"7%" }}>
            <div className="product-description" style={{display:"flex", flexDirection:"column", justifyContent:"flex-start", marginRight:"0%" }} >
              <h3 style={{fontSize: `max(20px, 1.8vw)`}} >{title}</h3>
              <p style={{fontSize: `max(16px, 1.2vw)`}} >{description}</p>
            </div>
            <div className="product-imgae"  style={{display:"flex", justifyContent:"end", width:"160%"}} >
              <img src={ step1_signup } alt="workflow"  style={{ height:"98%", width:"98%", aspectRatio:"auto" }} />
            </div>        
          </div>
        )
      }
      else{
        if(imageName == "step3_chat"){
          return(
            <div className="landing-product" style={{ display:"flex", flexDirection:"row", marginTop:"7%" }}>
              <div className="product-description" style={{display:"flex", flexDirection:"column", justifyContent:"flex-start", marginRight:"0%" }} >
                <h3 style={{fontSize: `max(20px, 1.8vw)`}} >{title}</h3>
                <p style={{fontSize: `max(16px, 1.2vw)`}} >{description}</p>
              </div>
              <div className="product-imgae"  style={{display:"flex", justifyContent:"end", width:"160%"}} >
                <img src={ step3_chat } alt="workflow"  style={{ height:"98%", width:"98%", aspectRatio:"auto" }} />
              </div>        
            </div>
          )
        }
      }
      
    }
  return (
      <div className="landing-product" style={{ display:"flex", flexDirection:"row", marginTop:"7%" }}>
        <div className="product-imgae"  style={{display:"flex", justifyContent:"start", marginRight:"3%",}} >
          <img src={ step2_upload}  alt="workflow" style={{ height:"98%", width:"98%", aspectRatio:"auto" }} />
        </div>
        <div className="product-description" style={{display:"flex", flexDirection:"column", justifyContent:"flex-start", width:"140%" }} >
          <h3 style={{fontSize: `max(20px, 1.8vw)`}} >{title}</h3>
          <p style={{fontSize: `max(16px, 1.2vw)`}} >{description}</p>
        </div>       
    </div>
  )
}

export default Product;