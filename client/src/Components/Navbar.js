import React from 'react';
import { Link, BrowserRouter } from 'react-router-dom';
import WB from "../Assets/WB.svg";


function Navbar() {
  return (
    <BrowserRouter>
    <nav class="navbar">
    <div class="navbar-left">
    <img src={WB}style={{aspectRatio: 50/50}} width="70px" alt="Elon Musk" className="navbar-left-logo"></img>

      <a href="#demo" class="navbar-left-brand">ProFresh</a>
    </div>
    <div class="navbar-right">
      <button class="navbar-button">Meet the team</button>
      <button class="navbar-button">Get Started</button>
    </div>
  </nav>
    </BrowserRouter>
  );
}

export default Navbar;
