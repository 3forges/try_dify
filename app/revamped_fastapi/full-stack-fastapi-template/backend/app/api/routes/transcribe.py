import uuid
from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlmodel import col, delete, func, select

from app.speechtotext import whisper_service
from app import crud
from app.api.deps import (
    CurrentUser, # CurrentUser = Annotated[User, Depends(get_current_user)]
    SessionDep,
    get_current_active_supercontribution,
)
from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app.models import (
    Item,
    Message,
    UpdatePassword,
    Contribution,
    ContributionCreate,
    ContributionPublic,
    ContributionsPublic,
    ContributionUpdate,
)
from app.utils import generate_new_account_email, send_email

router = APIRouter(prefix="/transcribe", tags=["contributions"])

###########################################
###########################################
### TRANSCRIPTIONS
###########################################
###########################################

class TranscriptionPublic():
    transcribed_text: str | None

# Very good example fast api and audio files:
# https://github.com/fastapi/fastapi/issues/5278
@app.post("/")
async def transcribe_audio(audio: UploadFile = File(...)):
    audio_path = audio.filename
    with open(audio_path, "wb+") as fp:
        fp.write(audio.file.read())

    transcribed_text_result = whisper_service.transcribe_audio(audio.filename)
    
    # return RedirectResponse(url='/', status_code=303)
    return TranscriptionPublic(transcribed_text=transcribed_text_result)



################
########## Ok j'ai ausssi trouvé cet exemple:
# (vient de [app\other_with_react\backend\main.py])



# Post bot response
# Note: Not playing back in browser when using post request.
@app.post("/post-audio/")
async def post_audio(file: UploadFile = File(...)):

    # Convert audio to text - production
    # Save the file temporarily
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename, "rb")

    # Decode audio : donc là c'est là que j'appellerais mon composant whisper
    message_decoded = convert_audio_to_text(audio_input)

    # Guard: Ensure output
    if not message_decoded:
        raise HTTPException(status_code=400, detail="Failed to decode audio")

    # Get chat response
    chat_response = get_chat_response(message_decoded)

    # Store messages
    store_messages(message_decoded, chat_response)

    # Guard: Ensure output
    if not chat_response:
        raise HTTPException(status_code=400, detail="Failed chat response")

    # Convert chat response to audio
    audio_output = convert_text_to_speech(chat_response)

    # Guard: Ensure output
    if not audio_output:
        raise HTTPException(status_code=400, detail="Failed audio output")

    # Create a generator that yields chunks of data
    def iterfile():
        yield audio_output

    # Use for Post: Return output audio
    return StreamingResponse(iterfile(), media_type="application/octet-stream")