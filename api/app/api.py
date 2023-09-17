from fastapi import FastAPI, Response, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from torch import autocast
import torch
from io import BytesIO
from auth_token import auth_token
from pydantic import BaseModel
from PIL import Image
from diffusers import StableDiffusionControlNetInpaintPipeline, StableDiffusionImg2ImgPipeline, ControlNetModel, DDIMScheduler
import numpy as np
import torch


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

device = "cuda" if torch.cuda.is_available() else "cpu"
generator = torch.Generator(device=device)

controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/control_v11p_sd15_inpaint", torch_dtype=torch.float16, use_auth_token=auth_token
)
pipe = StableDiffusionControlNetInpaintPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5", controlnet=controlnet, torch_dtype=torch.float16, use_safetensor=True,use_auth_token=auth_token
)
pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)

@app.post("/editImage")
def generate(init_image: UploadFile, mask_image: UploadFile):
    init_bytes = init_image.file.read()
    mask_bytes = mask_image.file.read()

    init_image = Image.open(BytesIO(init_bytes)).resize((512, 512))
    mask_image = Image.open(BytesIO(mask_bytes)).resize((512, 512))

    def make_inpaint_condition(image, image_mask):
        image = np.array(image.convert("RGB")).astype(np.float32) / 255.0
        image_mask = np.array(image_mask.convert("L")).astype(np.float32) / 255.0

        print(image.shape[0:1], image_mask.shape[0:1])
        assert image.shape[0:1] == image_mask.shape[0:1], "image and image_mask must have the same image size"
        image[image_mask > 0.5] = -1.0  # set as masked pixel
        image = np.expand_dims(image, 0).transpose(0, 3, 1, 2)
        image = torch.from_numpy(image)
        return image

    control_image = make_inpaint_condition(init_image, mask_image)
        

    image = pipe(
        "a handsome man with ray-ban sunglasses",
        num_inference_steps=20,
        generator=generator,
        guidance_scale=9.0,
        eta=5.0,
        image=init_image,
        mask_image=mask_image,
        control_image=control_image,
    ).images[0]

    image.save("SHOUTPUT.png")

    """
    SD = imgToImg()
    with autocast(device):
        # Pass the information into the function
        res = SD.editImage(init_pil, mask_pil, prompt)
    
    # convert res to base64
    buffer = BytesIO()
    res.save(buffer, format="PNG")
    imgstr = base64.b64encode(buffer.getvalue())
    """
    
    # Return the image
    # return Response(content=imgstr, media_type="image/png")
    return {"hello":"world"}


        

