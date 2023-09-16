import React, { useState, useRef, useEffect } from 'react';
import { ReactSketchCanvas } from "react-sketch-canvas";
import Cropper from 'react-cropper';
import 'cropperjs/dist/cropper.css';

const styles = {
  border: "0.0625rem solid #9c9c9c",
  borderRadius: "0.25rem",
};

const Demo = () => {
  const [eraseState, setEraseState] = useState(false);
  const [backgroundImage, setBackgroundImage] = useState("");

  const [initial, setInitial] = useState(true);
  const [imageSrc, setImageSrc] = useState('');
  const [croppedImage, setCroppedImage] = useState(null);
  const cropperRef = useRef(null);

  // Function to handle file input change
  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (file) {
      const imageURL = URL.createObjectURL(file);
      setImageSrc(imageURL);
    }
  };

  // Function to handle cropping
  const handleCrop = () => {
    if (cropperRef.current) {
      cropperRef.current.getCroppedCanvas({ width: 700, height: 700 }).toBlob((blob) => {
        const croppedImageURL = URL.createObjectURL(blob);
        setCroppedImage(croppedImageURL);
        setrealHeight(croppedImageURL.width);
        setrealWidth(croppedImageURL.height);
      });
    }
  };
  
  const canvas = useRef(null);
//   const img = new Image();
//   img.src = backgroundImage;
//   console.log(img.height, img.width);
//   var realHeight = img.height + "px"
//   var realWidth = img.width + "px"

  var [realWidth, setrealWidth] = useState("");
  var [realHeight, setrealHeight] = useState("");

  useEffect(() => {
    if (backgroundImage !== "") {
        const img = new Image();
        img.src = backgroundImage;

        img.onload = () => {
        const width = img.width;
        const height = img.height;


        // Set the canvas width and height based on the image dimensions
        setrealWidth(width);
        setrealHeight(height);
        };
    }
  }, [backgroundImage]);

    // useEffect(() => {
    //     setBackgroundImage();
        
    // }, [realHeight, realWidth]);

    useEffect(() => {
        setBackgroundImage(croppedImage);
      }, [realHeight, realWidth]);


  useEffect(() => {
    if(eraseState === true){
        canvas.current.eraseMode(eraseState); 
    }
  }, [eraseState]);

//   useEffect(() => {
//     console.log("HELP");
    // if (backgroundImage === "" && !initial) {
        
    // canvas.current.exportImage("png")
    //       .then(dataURL => {
    //         // Create a temporary download link
    //         console.log(dataURL);
    //         const downloadLink = document.createElement("a");
    //         downloadLink.href = dataURL;
    //         downloadLink.download = "lolll.png";

    //         // Trigger a click event on the download link
    //         downloadLink.click();
    //         })
    //         .catch(error => {
    //             console.error(error);
    //         });
    //     }
//     if (backgroundImage === ""){
//         const img = new Image();
//         img.src = backgroundImage;
//         console.log(img.height, img.width);
//         img.onload = () => {
//             console.log(img.height, img.width);
//             setrealHeight(img.height + "px");
//             setrealWidth(img.width + "px");
//         };
//  }
//   }, [backgroundImage]);

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

  if(!croppedImage){
    return (
        <div>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      {imageSrc && (
        <div>
          <Cropper
            src={imageSrc}
            style={{ maxHeight: '400px', width: '100%' }}
            initialAspectRatio={1}
            guides={true}
            viewMode={2}
            responsive={true}
            ref={cropperRef}
            onInitialized={(instance) => {
              cropperRef.current = instance;
            }}
          />
          <button onClick={handleCrop}>Crop Image</button>
        </div>
      )}
      
    </div>
    )
  }

  return (
    <div>
    {
        backgroundImage === "" ? (
            <ReactSketchCanvas
                ref={canvas}
                strokeWidth={20}
                strokeColor="black"
                canvasColor="white"
                width= {realWidth}
                height= {realHeight}
                backgroundImage={croppedImage}
                exportWithBackgroundImage = {false}
            />
        ):(
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
        )
    }
        <div>
          <h2>Cropped Image:</h2>
          <img src={croppedImage} alt="Cropped" />
          <h2>NON Image:</h2>
          <img src={backgroundImage} alt="Cropped" />
        </div>
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
            setBackgroundImage("");
            canvas.current.exportImage("png")
          .then(dataURL => {
            // Create a temporary download link
            // console.log(dataURL);
            // const downloadLink = document.createElement("a");
            // downloadLink.href = dataURL;
            // downloadLink.download = "lolll.png";

            // // Trigger a click event on the download link
            // downloadLink.click();
            // After downloading, modify the image
            const image = new Image();
            image.src = dataURL;

            image.onload = () => {
            const canvas = document.createElement("canvas");
            const ctx = canvas.getContext("2d");
            canvas.width = image.width;
            canvas.height = image.height;
            ctx.drawImage(image, 0, 0);

            const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
            const data = imageData.data;

            // Loop through pixels and change transparent pixels to white
            for (let i = 0; i < data.length; i += 4) {
                const alpha = data[i + 3]; // Alpha channel value (0 to 255)
                if (alpha === 0) {
                // If the pixel is transparent (alpha = 0), set it to white
                data[i] = 255; // R (red)
                data[i + 1] = 255; // G (green)
                data[i + 2] = 255; // B (blue)
                data[i + 3] = 255; // Alpha (fully opaque)
                }
            }

            // Put the modified image data back on the canvas
            ctx.putImageData(imageData, 0, 0);

            // Export the modified image as a new download link
            const modifiedDataURL = canvas.toDataURL("image/png");
            const modifiedDownloadLink = document.createElement("a");
            modifiedDownloadLink.href = modifiedDataURL;
            modifiedDownloadLink.download = "real.png";
            modifiedDownloadLink.click();
            };

            })
            .catch(error => {
                console.error(error);
            });// Set eraseState to true
        }}
      >
        Done
      </button>
    </div>
    
  );
};


export default Demo;
