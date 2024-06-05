from diffusers import StableDiffusionPipeline, DiffusionPipeline
import torch

def load_model():
    model_id = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = pipe.to("cuda")
    return pipe

def model_inference(prompt="a photo of an astronaut riding a horse on mars"):
    pipe = load_model()
    image = pipe(prompt, num_inference_steps=10).images[0]  
    # image.save("astronaut_rides_horse.png")
    return image

if __name__ == "__main__":
    model_inference()