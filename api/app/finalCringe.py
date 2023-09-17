from diffusers import StableDiffusionControlNetInpaintPipeline, ControlNetModel, DDIMScheduler
from diffusers.utils import load_image
import numpy as np
import torch
from auth_token import auth_token


device = "cuda" if torch.cuda.is_available() else "cpu"
#Initial image
init_image = load_image("C:/Users/julie/OneDrive/Desktop/jeff.png").resize((512, 512)) # converts into a PIL image

#Mask image
mask_image = load_image("C:/Users/julie/OneDrive/Desktop/jeffmask.png").resize((512, 512))

generator = torch.Generator(device=device).manual_seed(1)

#Combining the two images
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

#Setting up the models
controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/control_v11p_sd15_inpaint", torch_dtype=torch.float16, auth_token=auth_token
)
pipe = StableDiffusionControlNetInpaintPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5", controlnet=controlnet, torch_dtype=torch.float16, use_safetensor=True, auth_token=auth_token
)

#speed up diffusion process with faster scheduler and memory optimization
pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)

pipe.enable_model_cpu_offload()

#generate image
image = pipe(
    "a man wearing a suit, fully clothed",
    num_inference_steps=20,
    generator=generator,
    guidance_scale=9.0,
    eta=1.0,
    image=init_image,
    mask_image=mask_image,
    control_image=control_image,
).images[0]

image.save("SHOUTPUT.png")