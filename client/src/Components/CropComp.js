import React, { useRef, useState } from 'react';
import Cropper from 'react-cropper';
import 'cropperjs/dist/cropper.css';
import '../App.css';


function ImageCropper() {
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
      cropperRef.current.getCroppedCanvas({ width: 800, height: 800 }).toBlob((blob) => {
        const croppedImageURL = URL.createObjectURL(blob);
        setCroppedImage(croppedImageURL);
      });
    }
  };

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
      {croppedImage && (
        <div className="my-cropped-image">
          <h2>Cropped Image:</h2>
          <img src={croppedImage}style={{aspectRatio: 50/50}} width="50px" alt="Cropped"></img>

        </div>
      )}
    </div>
  );
}

export default ImageCropper;
