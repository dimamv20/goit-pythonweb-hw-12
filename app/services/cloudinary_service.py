import cloudinary
import cloudinary.uploader
from dotenv import dotenv_values

config = dotenv_values(".env")

cloudinary.config(
    cloud_name=config["CLOUDINARY_CLOUD_NAME"],
    api_key=config["CLOUDINARY_API_KEY"],
    api_secret=config["CLOUDINARY_API_SECRET"],
    secure=True
)

def upload_avatar(file_path: str):
    response = cloudinary.uploader.upload(file_path, folder="avatars")
    return response.get("secure_url")
