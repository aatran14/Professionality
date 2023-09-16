import React from 'react';
import ElonMusk from "../Assets/ElonMusk.jpg";

export default function Quote() {
  return (
    <div className="Quote-Image-Container">
    
    <div className="quote">
    <p className="words">
    "Enabling underrepresented communities is one of the most interesting challenges in the world.
    I want to help people who change the world change the world."</p>
    <p className="author">
    - Andy Tran Co-Founder
    </p>
    </div>


    <div className="sample-image">
    <img src={ElonMusk}stle={{aspectRatio: 50/50}} width="350px" alt="Elon Musk" className="elon-musk"></img>
    
    
    

    </div>
   

  

   
    
    
    </div>
  )
}
