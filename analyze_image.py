import argparse
import os
import sys

from openai import OpenAI

if "OPENAI_API_KEY" not in os.environ:
    print("Please set OPENAI_API_KEY env variable")
    sys.exit(1)

client = OpenAI()

parser = argparse.ArgumentParser(prog="gen_image")
parser.add_argument('-u', '--url', required=True, help="Image URL")
parser.add_argument('-p', '--prompt', default="What's in this image?", help="Prompt")
parser.add_argument('-m', '--model', default="gpt-4-vision-preview", help="Model to use")
args = parser.parse_args()

response = client.chat.completions.create(
    model=args.model,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": args.prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": args.url,
                    },
                },
            ],
        }
    ],
    max_tokens=300,
)

print(response.choices[0])
