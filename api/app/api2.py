from fastapi import FastAPI, Response, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from torch import autocast
import torch
import requests
from PIL import Image
from io import BytesIO
from diffusers import StableDiffusionImg2ImgPipeline
from auth_token import auth_token
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

device = "cuda"
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "nitrosocke/Ghibli-Diffusion", torch_dtype=torch.float16, use_auth_token=auth_token
).to(device)

@app.post("/")
def generate(init_image: UploadFile, mask_image: UploadFile):
    init_bytes = init_image.file.read()
    init_pil_image = Image.open(BytesIO(init_bytes))
    prompt = "ghibli style, a fantasy landscape with castles"
    generator = torch.Generator(device=device).manual_seed(1024)
    image = pipe(prompt=prompt, image=init_pil_image, strength=0.75, guidance_scale=7.5, generator=generator).images[0]

    return {"Hello": "World"}