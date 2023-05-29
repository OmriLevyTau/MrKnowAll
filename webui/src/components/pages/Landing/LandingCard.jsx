import { Card } from 'antd'
import React from 'react'

function LandingCard({content, title, icon}) {
  return (
    <Card
        hoverable
        title={title}
        headStyle={{background:"#F9F7F7", fontSize:`max(18px, 1vw)`}}
        bordered={false} 
        style={{ width:300, margin:"2%" ,textAlign:"center", justifyContent: 'center', whiteSpace: "pre-line" , display: "flex", flexDirection: "column", fontSize:`max(18px, 0.5vw)`}}>
            {icon}
            <br />
            <br />
            <p>{content}</p>
    </Card>
  )
}

export default LandingCard