import React from 'react'
import solidOne from "../Assets/1-solid.svg"
import solidTwo from "../Assets/2-solid.svg"
import Demo from "./Demo.js";

import "./Demo.css";
import '../App.css';


import solidThree from "../Assets/3-solid.svg"

export default function Tutorial() {
  return (
    <div className="tutorial">
        <h2>How do I get started?</h2>

        <div className="instruction-and-demo">

        <div className="instruction-list">

        <div className="instruction-set">
        <img src={solidOne}style={{aspectRatio: 50/50}} width="30px" alt="numberOne" className="number"></img>
        <p className="instruction">Upload an image :)</p>
        </div>


        <div className="instruction-set">        
        <img src={solidTwo}style={{aspectRatio: 50/50}} width="30px" alt="numberOne" className="number"></img>
        <p className="instruction">Upload an image :)</p>
        </div>

        <div className="instruction-set">      
          <img src={solidThree}style={{aspectRatio: 50/50}} width="30px" alt="numberOne" className="number"></img>
          <p className="instruction">Upload an image :)</p>

        </div>
        </div>
        <div className="demo-list">
        <Demo/>
        </div>

        </div>


        


    
    </div>
  )
}
