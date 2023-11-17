import argparse
import datetime
import os
import re
import sys
import unicodedata
from urllib.request import urlretrieve

from openai import OpenAI

def make_slug(text):
  text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
  text = re.sub(r'[^\w\s-]', '', text).strip().lower()
  return re.sub(r'[-\s]+', '-', text)

def make_filename(text, size):
  slug = make_slug(text)
  timestamp = datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y-%m-%d-%H.%I.%S")
  return f"{slug}_{size}_{timestamp}.png"

if "OPENAI_API_KEY" not in os.environ:
  print("Please set OPENAI_API_KEY env variable")
  sys.exit(1)

base_dir = "images"
 
if not os.path.exists(base_dir):
  os.makedirs(base_dir)

parser = argparse.ArgumentParser(prog="gen_image")
parser.add_argument('prompt', help="Prompt")
parser.add_argument('-s', '--size', default="1024x1024", choices=['256x256', '512x512', '1024x1024', '1024x1792', '1792x1024'], help="Image size")
parser.add_argument('-m', '--model', default="dall-e-3", help="Model to use")
args = parser.parse_args()

client = OpenAI()

print("- Generating image")
response = client.images.generate(
  model="dall-e-3",
  prompt=args.prompt,
  size=args.size,
  quality="standard",
  n=1,
)

image_url = response.data[0].url
filename = os.path.join(base_dir, make_filename(args.prompt, args.size))

print("- Downloading image")
urlretrieve(image_url, filename)

print(f"Saved to: {filename}")
