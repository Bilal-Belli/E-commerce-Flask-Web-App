import cloudinary
import cloudinary.uploader

# Set up Cloudinary configuration
cloudinary.config(
    cloud_name = 'dxqcqtzo2',
    api_key = '333815531534449',
    api_secret = 'pacUnfaWwm73BsnggQbnY20eGdA'
)

response = cloudinary.uploader.upload(r"C:\Users\Hp\OneDrive\Bureau\flaskUpworkGit\imagesExamples\laptop.jpg")
image_url = response['url']
print(f"Image URL: {image_url}")

response = cloudinary.uploader.upload(r"C:\Users\Hp\OneDrive\Bureau\flaskUpworkGit\imagesExamples\headphones.jpg")
image_url = response['url']
print(f"Image URL: {image_url}")

response = cloudinary.uploader.upload(r"C:\Users\Hp\OneDrive\Bureau\flaskUpworkGit\imagesExamples\smartphone.jpg")
image_url = response['url']
print(f"Image URL: {image_url}")

response = cloudinary.uploader.upload(r"C:\Users\Hp\OneDrive\Bureau\flaskUpworkGit\imagesExamples\keyboard.jpg")
image_url = response['url']
print(f"Image URL: {image_url}")