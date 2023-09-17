import React from 'react';
import ElonMusk from "../Assets/ElonMusk.jpg";
import QuoteCarousel from "./QuoteCarousel.js";

export default function Quote() {
  return (
    <div className="Quote-Image-Container">
    <div className="quote">
    <QuoteCarousel/>
    
    </div>
    <div className="sample-image">
    <img src={ElonMusk}style={{aspectRatio: 50/50}} width="300px" alt="Elon Musk" className="elon-musk"></img>
   
    </div>
    
    </div>
    
  )
}
