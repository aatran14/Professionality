from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
import numpy as np
from torch import autocast
import torch
import requests
from PIL import Image
from io import BytesIO
from diffusers import StableDiffusionControlNetInpaintPipeline, ControlNetModel, DDIMScheduler
from auth_token import auth_token
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,
    filename='app.log'
)


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'C:/Users/julie/OneDrive/Desktop/ShellHacks23/Professionality/api/app/uploads'  # Folder where uploaded images will be stored
app.config['ALLOWED_EXTENSIONS'] = {'png'}  # Set allowed file extensions

#device = "cuda" if torch.cuda.is_available() else "cpu"
device = "cpu"
generator = torch.Generator(device=device)

controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/control_v11p_sd15_inpaint", torch_dtype=torch.float32, use_auth_token=auth_token
)
pipe = StableDiffusionControlNetInpaintPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5", controlnet=controlnet, torch_dtype=torch.float32,use_auth_token=auth_token
)
pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)

@app.route('/editImage', methods=['POST'])
def edit_image():
    # Check if init image is in the request
    if 'init_image' not in request.files:
        return 'no init image'
    if 'mask_image' not in request.files:
        return 'no mask image'

    logger = logging.getLogger('app')

    init_image = Image.open(request.files['init_image']).resize((512, 512))
    mask_image = Image.open(request.files['mask_image']).resize((512, 512))

    def make_inpaint_condition(image, image_mask):
        print("Temppppp")
        image = np.array(image.convert("RGB")).astype(np.float32) / 255.0
        image_mask = np.array(image_mask.convert("L")).astype(np.float32) / 255.0

        print(image.shape[0:1], image_mask.shape[0:1])
        logger.log(logging.DEBUG, "Img Shape: " + str(image.shape[0:1]))
        assert image.shape[0:1] == image_mask.shape[0:1], "image and image_mask must have the same image size"
        image[image_mask > 0.5] = -1.0  # set as masked pixel
        image = np.expand_dims(image, 0).transpose(0, 3, 1, 2)
        image = torch.from_numpy(image)
        return image

    logger.log(logging.DEBUG, "Before inpainting")
    control_image = make_inpaint_condition(init_image, mask_image)
    logger.log(logging.DEBUG, "After inpainting")

    pipe.enable_model_cpu_offload()

    image = pipe(
        "a handsome man with ray-ban sunglasses",
        num_inference_steps=10,
        generator=generator,
        guidance_scale=9.0,
        eta=1.0,
        image=init_image,
        mask_image=mask_image,
        control_image=control_image,
    ).images[0]

    image.save("SHOUTPUT.png")

    return jsonify({"message": "Yay it is done!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
