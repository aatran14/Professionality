import React from 'react';
import { Link, BrowserRouter } from 'react-router-dom';

function Navbar() {
  return (
    <BrowserRouter>
    <nav class="navbar">
    <div class="navbar-left">
      <a href="#demo" class="navbar-brand">Professionality</a>
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
