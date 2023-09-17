from diffusers import StableDiffusionControlNetInpaintPipeline, ControlNetModel, DDIMScheduler
from diffusers.utils import load_image
import numpy as np
import torch
from io import BytesIO
import base64
from PIL import Image
import logging

class imgToImg:
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='app.log',
        filemode='w'
    )


    def editImage(self, init_image, mask_image, prompt): # takes input base64 representation for the images
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger = logging.getLogger(__name__)

        # Convert init image to PIL and resize
        #init_image = load_image("C:/Users/julie/OneDrive/Desktop/jeff.png").resize((512, 512)) # converts into a PIL image
        
        """
        try:
            init_image = Image.open(BytesIO(base64.b64decode(init_image)))
        except Exception as e:
            logger.error("Process failed while opening image", e.args[0])

        try:
            init_image.resize((512, 512))
        except Exception as e:
            logger.error("Process failed during image resizing", e.args[0])
        """
        logger.log(logging.DEBUG, str(type(init_image)))
        logger.log(logging.DEBUG, str(type(mask_image)))
        init_image.resize((512, 512))
        mask_image.resize((512, 512))

        # Conver mask image to PIL and resize
        #mask_image = load_image("C:/Users/julie/OneDrive/Desktop/jeffmask.png").resize((512, 512))
        
        """
        try:
            mask_image = Image.open(BytesIO(base64.b64decode(mask_image)))
        except Exception as e:
            logger.error("Process failed while opening mask image", e.args[0])

        try:
            mask_image.resize((512, 512))
        except Exception as e:
            logger.error("Process failed during mask image resizing", e.args[0])
        """

        generator = torch.Generator(device=device)

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

        try:
            control_image = make_inpaint_condition(init_image, mask_image)
        except Exception as e:
            logger.log(logging.DEBUG, "combination failed")

        #Setting up the models
        controlnet = ControlNetModel.from_pretrained(
            "lllyasviel/control_v11p_sd15_inpaint", torch_dtype=torch.float16
        )
        pipe = StableDiffusionControlNetInpaintPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5", controlnet=controlnet, torch_dtype=torch.float16, use_safetensor=True
        )

        #speed up diffusion process with faster scheduler and memory optimization
        pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)

        pipe.enable_model_cpu_offload()

        #generate image
        
        image = pipe(
            prompt=prompt,
            num_inference_steps=20,
            generator=generator,
            guidance_scale=9.0,
            eta=1.0,
            image=init_image,
            mask_image=mask_image,
            control_image=control_image,
        ).images[0]

        return image # returns a PIL image

"""  
tempA = ""
tempB = ""
a = ""
b = "iVBORw0KGgoAAAANSUhEUgAAAZkAAAHlCAMAAAAQm3FGAAAAAXNSR0IB2cksfwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAvRQTFRF////6Ojo2NjY/f396+vrqKiofn5+UlJSQkJCJiYmKSkpSUlJU1NTkZGRz8/P/Pz8/v7+nZ2dX19fHx8fERERAwMDAQEBAAAABwcHGhoaSkpKkpKS1tbW+Pj49vb25eXl6urqmpqaPDw8DAwMCAgIOzs7UVFRUFBQRUVFQUFBOTk5T09PcnJy6enp9/f30tLSS0tLFBQUHh4eTk5O9PT0zMzMcXFxFRUVAgICGRkZeHh44ODg7u7u39/f+/v7xsbGenp6IiIiBAQEVlZW19fXkJCQYmJiNTU1MDAwTExMJSUlsrKy7+/vs7OzSEhICQkJLy8vaGhorKysq6urMTEx7e3tv7+/cHBwd3d3VVVVqampr6+v3t7e7OzsJycnCwsLFhYWKCgobm5utbW1ubm5EBAQHBwc4eHhZ2dn8fHxhISEIyMjo6Oj1NTUYWFhBgYGLCwseXl5wcHBY2NjBQUFtra2jo6Oc3Nz8PDwDw8PVFRU4uLib29vICAgiIiI5+fnt7e3gYGBQ0ND4+Pj2dnZLi4upaWlvb29QEBAEhISwsLCGxsbuLi4+fn5W1tbCgoKaWlp8/PzsLCwREREjY2NhYWFiYmJISEhx8fHw8PDnp6eKioqExMTioqKKysr5OTky8vLoKCgWlpaDg4OhoaGrq6uHR0ddXV1ODg48vLyxMTEGBgYOjo629vbfHx8xcXFFxcXu7u7V1dXXl5eDQ0NNzc3RkZG1dXVnJycoqKi3Nzc+vr6MzMzyMjIwMDA5ubmbGxs9fX1XFxcdnZ2vLy80NDQoaGhPz8/p6en3d3df39/urq6WFhYpKSki4uL0dHRmJiYysrKgoKCmZmZWVlZ2tragICAJCQkdHR0e3t7MjIyZmZmvr6+09PTm5ubpqamsbGxR0dHPj4+zs7ObW1tlJSUlpaWqqqqh4eHj4+Pzc3NXV1dZGRka2trfX19TU1NjIyMycnJLS0tampqPT09tLS0YGBgg4ODNDQ0n5+fl5eXra2tuvsRZgAAC2JJREFUeJzt3Xl4VNUZx3FICBpEiIW5N6iBiJFFBEzEMpAQZWRTlBhWRQIRjFFZAhqtiBgElB1soYUoCohFY0RUAi64FIQibnWpUq2ptlrUotLWttr2n06CtcyQkNy595y3587381eeh3l4zm/eZ2bOPWuTJoBKTRMSEqTbgEiJzRKSmh93fHKLE1qe2Kq1dGvwvZSTftCmbcCyw6zUdiefcmpaWlr7Dh06pEk3LM6ln9bxdPtIGe3O6NS5S9czu52V1F26cXGsR8+zM+36ZJ3Ts5d0A+PVuT/sbdVbGNsO9umbLd3EOJPTr1+/Jrnnnd8/cIy61Ahd0Eq6rXEkZcDAQYOHXHjc8Rc1UJYagY5D01unSDc5Plx8ybB2jSjJ9/IuzR/Oz40OI0YGnRSm5nPT9oKkUdLN9r2U0UMc1qVWmzHpudJN97n2l4ViqYydd/nYK4YPHZfDEIEqBeNjKoxtWxMKM9tcOXGSdADfuqooxsp85+qBxdIRfCm34Bp3hbHtjK6nXcuImtfSrht/rEf+RsqbnD+FJxxPTZ1W4r4uYZY1YfqM6xOl4/hHjxtKPSlMrdDV+Tfy/OmNxJsyvCtMjRY/upnPjRfaj/TgNyZCyeCTrpVO5Qet8jwuTNjMW2YxNOBW2q3eFybcGZh9W450MrOVzbl9gorKhL/S5s6TDmew1vMnXq2mLjXuuFM6n7kWLHQ68O/IohHSAU212PNeWZQlS6UjmmnZcsWFCX+hnSsd0kSJY1eoLoxt3fVj6ZgGSr9UeWFsO2ucdEzz/GSl8u+ysNAq6ZyGSUn76WQNdQnrJh3VMNf+bJGewtirWSDgyIlLNBXGnknvzIk1HXUVxg6VS4c1yhgPp8oaELxEOqxJ1mj69a8RuFs6rUmax7boLyYlc6TTmuQefYWx17Kbo9Fa3+vxvP8x3Scd1yDrOmssTGlf6bgGWb9WY2XG95SOa5CbUvUVZu0G6bQmuV/HSOZhGx9Il05rkli3Yzg3YQxLmxz4ucvtGI23qe/F0mFNsuxBTV9mgYdGFEiHNUrFGXoKY3VawI4NRx6erqcyK+ZIJzXNgko9lXlks3RS0yzQ85xpPSod1DhbFC6XPcJjj0sHNc6s2ToKE3yCDTROdR+sozK9k6Rzmidnq47KVOVvkQ5qnMSJOipjB7ZdL53UOKsaOlTOI9uflE5qmhGaKpOX3086qmGe0jXXvPpplmc6coW2ibPlz0hnNcvQ0xt+T72x9mkObHBi/SZdlSm9i4kzJwq66qqMvXCHdFijpM3QVplnn5MOa5bnFR3NcLTC86SzmmWeo1OZ3chgTZMjL8R0/G8sgr9gZ7MTZffrqow9mOXmTqScr60yeauWSac1ypwWuioTfGKndFij7NylaVAz3G9myZkjZdp6Z+NHS2c1S+6LurYD9tktndUwe+6Iege9Oa+Zyrj3y6gB55lU5v9Eh5aR76CC42drPctCDafGRs5squqs7a2QDmqc4sKId1DRcZqh/PbSQY1TrGURbeFLzJ05VZylozJd9knnNE93LSM0L0vHNFCxjsoE2UPjXPFqDZXJu1k6poGKdWzWCCyQjmmghMbczezaKdIxDbRZy6ozdtE4t1lHD6BkqnRMA+3bpaEyWSzQiMFZGhaeb+Oshhi8omEQYAlX1Megxy6llwLVsl5lgUYMylcrr4wdek06pYkqXtdwaFPvX0nHNNHmc9RXxi7cIx3TRLt1jNAUNpWOaaDc5uo7AbY9jO1Nzr2gZSrgDXZrOjdIxzLajCQeOB0brmWf8z0soHFs3Epl5QhaYcHaH7I8+mfOna/siiArFAxZdu0jU8ab0jENtKWNosIESwNWKKOodu1nFsNnzvU4W+VAwOH/23pLOqWJEt9W/0iTzO6mWKxXfn9T2xvpNMei4tcKv84sK1A1l/s0YzRc1QYN2+5972u7BzDhHKt31J15njlLOpzRmu1VVpmM+dLhjJb7rrLeWfAq6XBmK9+vqjJ2tx7S4YzW/TJVG5ttq9M86XRGm3+5usGzvVwP4EZ5N2XPNNa9PGa60fMWZWdqjMyRDme2hOmqPjXJ66SzGe43iioTeI/Nze4kqVgQEMzIepQbNV1arKDnXPrennSWzbjVs8r7ylgXdJCO5QPZKm4M7H+3dCwfyH5fQWXsGxidcW3nb1VUZi53A7n3lIpFNO9TGffWqRg8G0ZlPPCcghm0G9gG4IFeH6z0un82eYp0KJ+ofn2lp/efWJ3TpSP5xqmeHhSY9zvpPP7xoaenNyz6SDqPf1zj6WKNdq9I5/GNam9P1qoslg7kF+t/7+36pv7dpRP5xNLjPa2Lbd/DdKYn1qz0ei3AyBekM/lCgfdXbP2B80298PF4zyvzCdsAvPBHzzdrFN0pnckXyjp6XRhrK3fQe+GA10c2WM/ynOmFCs8nm9//lBkAL0zJaPi9bpSaYzNCJYuSJy6VjuQTF7qvSeqm1ZsuWnhCfvPPXv78tfU8ynhjX7L7D8vcffPnz2eBmccWu//9D30mHcKXbnQ/lFnFtRkqvOt+J8AmHvgVSOzkujB21zTpFH607kzXhbHy2SejwDr3V5+njmU/hgLvuF9o1uJP0iF8abPrZWbWQTbKqnCu68VMVUOlM/jTm64r04Jj/5R4zvUQwBdsYVIiZ5HLwqzYIB3Bp3q5nZ3JYs2fGq2nuazMMFbJKHK3u6VmwRdbSyfwqzXuugClUziQSZEEd6ecrv1AOoBvVbsbONvP+iVVqnu7qsyXLC1XpTrTTWFCX0m337/GFUa81Q5nOCt3S7ffv6r7RLzVeUccqdWIFQIrOcVUmajKVB1q+98/UzsOaehMOuvP0s33serI9Walb5w0cmbtX1dOS/jwoQYqs/8v0s33sYq/Rn4Krtsxa+DBR4Yc+iLp5iZNXslfkhoIWvV9rVmdWZuhzo4uke/2CeGC9MrOzj48t1+84O2+M5p//bfedRYnxKSZQjvyI7tjk7Oj/n3Zsh1NepXvqmtf2n0DZNocH3IPRA5pFo2u82Wj/n77PzptjTw0wOq2THNj48ukyCHNwDf1vG5HevozkZvTg7dpbWjcmRq1GaBz/S9NWBL5M/OAvlbGo1EHIytTNK7el34euQkq44DGZsajtyL7XVby873qfmFO1E3PmWP1NjTufLQxqsuVeWudZ2Cm3Bm1O71dte6mxpnsyVGVsUu+XVzH5fGjuka97FBT/Y2NKzsPRlfGtjduLT/qdf+M+siUvsVEs2L/iv46Cwv2f708YV6zZs0KCgra176qenbUS5aUCbfb/55pcXRlwn3ijZXT7xi57ZG9r/Y9sOWdSV9VRk3dWIPq+MaDp3KbNzBfVjKhKM+Kfs3Ml9g2o9zjsew8Hybd6njQbIbz05oqP5RudVyYtdzpzQDBlvU8jsJba04OOFubUcmN2ZokfFnkpDCBvu2lWxw3Cj7d7+COwOkMzGh03tZGLz5vyy1mWuVMuq9xHYHg14yYafZx/qJGdARKDz0p3dD4s3P9tw3vdGr5sHQz41LTazKP+bEJtPlmqnQb41TF2O2P1VuXksnTFnMds5gBbzy4cHry/syNVRmppcH/DWWWztz+IF9ksnLKysqmtir/4N8bTvv8k+3bZvfJmr16yNaXd8+SbhgijNuzZ09xcfEo6XYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgDv0HB1kie8HlqdUAAAAASUVORK5CYII="
c = "boy wearing a suit"
SD = imgToImg()
print(SD.editImage(a, b, c))
"""
SD = imgToImg()
init_image = Image.open("C:/Users/julie/OneDrive/Desktop/jeff.png")
mask_image = Image.open("C:/Users/julie/OneDrive/Desktop/jeffmask.png")
generatedImage = SD.editImage(init_image, mask_image, "Young boy wearing a tie")
generatedImage.save("MaJefe.png")