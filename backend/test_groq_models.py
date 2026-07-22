from groq import Groq
from app.config import get_settings

settings = get_settings()
client = Groq(api_key=settings.groq_api_key)

for model in client.models.list().data:
    print(model.id)