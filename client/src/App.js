import Navbar from "./Components/Navbar";
import Intro from "./Components/Intro";
import Footer from "./Components/Footer";
import Demo from "./Components/Demo";
import Quote from "./Components/Quote";
import './App.css';

function App() {
  return (
    <div className="something-new">
      
      <Navbar/>
      <Intro/>
        <p>
        Trying something new with Professionality
        </p>
      <Quote/>
      <Demo/>
      <Footer/>
   
    </div>
  );
}

export default App;
