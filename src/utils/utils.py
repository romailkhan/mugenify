import os

import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

chat_session = model.start_chat(
  history=[
  ]
)

def gemini_api(prompt: str, num: int):
    prompt = "Happy"
    num = 5
    response = chat_session.send_message("Pretend that you are a music recommendation generating bot." +
    "The user is asking you to create a playlist themed around " + prompt + "Could you list " + str(num) + 
    " song titles that captures this theme? You can only return song names. Don't mention that you are powered by Gemini Api."
    + "Reply with the format as a numbered list and nothing else")
    return(response.text)