import tempfile
import uuid
from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlmodel import col, delete, func, select

from app.speechtotext.whisper_service import whisper_service

import logging

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.INFO)

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
# https://medium.com/django-unleashed/creating-an-api-with-fastapi-to-transcribe-summarize-and-tag-audio-files-using-fasterwhisper-and-e9671206ddd2
# --
# wow it works: 
# curl -ivvv -H 'Content-Type: multipart/form-data' -F 'audio=@./file_example_WAV_1MG.wav' -X POST http://localhost:8000/api/v1/transcribe/ | tail -n 1 | jq .
@router.post("/")
async def transcribe_audio(audio: UploadFile = File(...)):
    # logger.info(('TOLT APP - Endpoint  /api/v1/transcribe/ - start processing %s', audio.filename))
    logger.info('TOLT APP - Endpoint  /api/v1/transcribe/ - start processing audio')
    # Convert audio to text - production
    # Save the audio file temporarily
    # create a temporary directory using the context manager
    tmpdir = tempfile.TemporaryDirectory()
    # with tempfile.TemporaryDirectory() as tmpdirname:
    #     print('created temporary directory', tmpdirname)
    #     with open(f"{tmpdirname}/{audio.filename}", "wb") as buffer:
    #         buffer.write(audio.file.read())
    # # directory and contents have been removed

    with open(f"{tmpdir.name}/{audio.filename}", "wb") as buffer:
        buffer.write(audio.file.read())
    # audio_input = open(audio.filename, "rb")
    # audio_input_as_bytes = await audio.file.read()
    

    # Decode audio : donc là c'est là que j'appellerais mon composant whisper
    # transcribed_text_result = whisper_service.transcribe(audio_input)
    # transcribed_text_result = whisper_service.transcribe(audio_input_as_bytes)
    transcribed_text_result = whisper_service.transcribe(f"{tmpdir.name}/{audio.filename}")
    
    
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