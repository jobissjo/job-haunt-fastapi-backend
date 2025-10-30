import cloudinary
import cloudinary.uploader
from app.settings import settings


class CloudinaryService:
    def __init__(self):
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
        )

    async def upload_image(self, file):
        """
        Upload an image file to Cloudinary.
        """
        try:
            result = cloudinary.uploader.upload(
                file,
                folder="images/",  # optional folder in your Cloudinary account
                resource_type="image",
            )
            return {
                "url": result.get("secure_url"),
                "public_id": result.get("public_id"),
                "format": result.get("format"),
            }
        except Exception as e:
            raise Exception(f"Image upload failed: {e}")

    async def upload_document(self, file):
        """
        Upload a document (PDF, DOCX, etc.) to Cloudinary.
        """
        try:
            result = cloudinary.uploader.upload(
                file,
                folder="documents/",
                resource_type="raw",  # use raw for non-image files
            )
            return {
                "url": result.get("secure_url"),
                "public_id": result.get("public_id"),
                "bytes": result.get("bytes"),
            }
        except Exception as e:
            raise Exception(f"Document upload failed: {e}")
