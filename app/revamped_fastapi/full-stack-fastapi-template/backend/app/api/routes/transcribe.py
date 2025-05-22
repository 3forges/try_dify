import uuid
from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlmodel import col, delete, func, select

from app.speechtotext.whisper_service import whisper_service

# from app.models import (
#     Item,
#     Contribution
# )

router = APIRouter(prefix="/transcribe", tags=["transcribe"])

###########################################
###########################################
### TRANSCRIPTIONS
###########################################
###########################################

# Very good example fast api and audio files:
# https://github.com/fastapi/fastapi/issues/5278
@router.post("/")
async def transcribe_audio(audio: UploadFile = File(...)):
    # Convert audio to text - production
    # Save the audio file temporarily
    with open(audio.filename, "wb") as buffer:
        buffer.write(audio.file.read())
    audio_input = open(audio.filename, "rb")

    # Decode audio : donc là c'est là que j'appellerais mon composant whisper
    transcribed_text_result = whisper_service.transcribe(audio_input)
    
    # Guard: Ensure output
    if not transcribed_text_result:
        raise HTTPException(status_code=400, detail="Failed to transcribe audio")
    return transcribed_text_result
    # return TranscriptionPublic(transcribed_text=transcribed_text_result)
#     # Get chat response
#     chat_response = get_chat_response(message_decoded)
# 
#     # Store messages
#     store_messages(message_decoded, chat_response)
# 
#     # Guard: Ensure output
#     if not chat_response:
#         raise HTTPException(status_code=400, detail="Failed chat response")
# 
#     # Convert chat response to audio
#     audio_output = convert_text_to_speech(chat_response)
# 
#     # Guard: Ensure output
#     if not audio_output:
#         raise HTTPException(status_code=400, detail="Failed audio output")
# 
#     # Create a generator that yields chunks of data
#     def iterfile():
#         yield audio_output
# 
#     # Use for Post: Return output audio
#     return StreamingResponse(iterfile(), media_type="application/octet-stream")