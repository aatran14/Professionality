import React, { useState, useRef, useEffect } from 'react';
import { ReactSketchCanvas } from "react-sketch-canvas";

const styles = {
  border: "0.0625rem solid #9c9c9c",
  borderRadius: "0.25rem",
};

const Demo = () => {
  const [eraseState, setEraseState] = useState(false);
  const [backgroundImage, setBackgroundImage] = useState('https://drive.google.com/uc?export=view&id=1Oe9t_PvKt7n89jscypuzrRb5hm_vS_ic');
  
  const canvas = useRef(null);
//   const img = new Image();
//   img.src = backgroundImage;
//   console.log(img.height, img.width);
//   var realHeight = img.height + "px"
//   var realWidth = img.width + "px"

  var [realWidth, setrealWidth] = useState("");
  var [realHeight, setrealHeight] = useState("");

  useEffect(() => {
    const img = new Image();
    img.src = backgroundImage;
    console.log(img.height, img.width);
    img.onload = () => {
        console.log(img.height, img.width);
        const width = img.width;
        const height = img.height;
        setrealHeight(img.height + "px");
        setrealWidth(img.width + "px");
      };
    
    }, []);

    useEffect(() => {
        setBackgroundImage("https://drive.google.com/uc?export=view&id=1Oe9t_PvKt7n89jscypuzrRb5hm_vS_ic");
        
    }, [realHeight, realWidth]);


  useEffect(() => {
    if(eraseState === true){
        canvas.current.eraseMode(eraseState); 
    }
  }, [eraseState]);

  useEffect(() => {
    if (backgroundImage === "") {
    canvas.current.exportImage("png")
          .then(dataURL => {
            // Create a temporary download link
            console.log(dataURL);
            const downloadLink = document.createElement("a");
            downloadLink.href = dataURL;
            downloadLink.download = "lolll.png";

            // Trigger a click event on the download link
            downloadLink.click();
            })
            .catch(error => {
                console.error(error);
            });
        }
  }, [backgroundImage]);

//   function handleImageHeight(){
//     const img = new Image();
//     img.src = backgroundImage;
//     console.log(img.height, img.width);
//     return (img.height + "px");
   
//   }
//   function handleImageWidth(){
//     const img = new Image();
//     img.src = backgroundImage;
//     console.log(img.height, img.width);
//     return (img.width + "px");
   
//   }
  
    if (!realWidth || !realHeight) {
    return null; // Render nothing until realWidth and realHeight are set
  }

  return (
    <div>
      <ReactSketchCanvas
        ref={canvas}
        strokeWidth={20}
        strokeColor="black"
        canvasColor="white"
        width= {realWidth}
        height= {realHeight}
        backgroundImage={backgroundImage}
        exportWithBackgroundImage = {false}
      />
      <button
        onClick={() => {
            // console.log(realHeight, realWidth);
          setEraseState(true);// Set eraseState to true
        }}
      >
        Eraser
      </button>
      <button
        onClick={() => {
          setEraseState(false);// Set eraseState to true
        }}
      >
        Draw
      </button>
      <button
        onClick={() => {
            canvas.current.clearCanvas();// Set eraseState to true
        }}
      >
        Clear All
      </button>
      <button
        onClick={() => {
            setBackgroundImage("");// Set eraseState to true
        }}
      >
        Done
      </button>
    </div>
    
  );
};


export default Demo;
