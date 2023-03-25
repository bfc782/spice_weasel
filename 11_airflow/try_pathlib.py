# %%
import pathlib
import os
import requests
import json
import requests
import requests.exceptions as requests_exceptions
# %%
print(os.getcwd())
# %%

pathlib.Path("/tmp/images").mkdir(parents=True, exist_ok=True)


# %%
with open("/tmp/launches.json") as f:
    launches = json.load(f)
    image_urls = [launch["image"] for launch in launches["results"]]
    for image_url in image_urls:
        try:
            response = requests.get(image_url)
            image_filename = image_url.split("/")[-1]
            target_file = f"/tmp/images/{image_filename}"
            with open(target_file, "wb+") as f:
                f.write(response.content)
            print(f"Downloaded {image_url} to {target_file}")
        except requests_exceptions.MissingSchema:
            print(f"{image_url} appears to be an invalid URL.")
        except requests_exceptions.ConnectionError:
            print(f"Could not connect to {image_url}.")
# %%
