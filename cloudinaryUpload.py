import cloudinary
import cloudinary.uploader

# Set up Cloudinary configuration
cloudinary.config(
    cloud_name = 'dxqcqtzo2',
    api_key = '333815531534449',
    api_secret = 'pacUnfaWwm73BsnggQbnY20eGdA'
)

# Upload the image
response = cloudinary.uploader.upload(r"C:\Users\Hp\OneDrive\Bureau\flaskUpworkGit\imagesExamples\laptop.jpg")

# Get the URL of the uploaded image
image_url = response['url']

# Save the image URL in your database
print(f"Image URL: {image_url}")



response = cloudinary.uploader.upload(r"C:\Users\Hp\OneDrive\Bureau\flaskUpworkGit\imagesExamples\headphones.jpg")

# Get the URL of the uploaded image
image_url = response['url']

# Save the image URL in your database
print(f"Image URL: {image_url}")

response = cloudinary.uploader.upload(r"C:\Users\Hp\OneDrive\Bureau\flaskUpworkGit\imagesExamples\smartphone.jpg")

# Get the URL of the uploaded image
image_url = response['url']

# Save the image URL in your database
print(f"Image URL: {image_url}")

response = cloudinary.uploader.upload(r"C:\Users\Hp\OneDrive\Bureau\flaskUpworkGit\imagesExamples\keyboard.jpg")

# Get the URL of the uploaded image
image_url = response['url']

# Save the image URL in your database
print(f"Image URL: {image_url}")