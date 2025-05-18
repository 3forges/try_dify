from langchain_community.llms import Ollama
import gradio as gr
import json
import whisper
import torch


#function to load convert name of the country to the language spoken in that country
def get_language(country, file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data[country]


#function to load examples of phrases for few shot learning
def get_examples(file):
    with open(file, 'r') as f:
        data = f.read()
    return data

def jbl_test(audio_file):
    cheminFichier =   "Donc voilà le audio_file: [%s]" % audio_file
    print(" Donc voilà le audio: [%s]", audio_file)
    # testFIchier = '/c/Users/Utilisateur/AppData/Local/Temp/gradio/f4d2ba5e63db118ad186d35d1aa2b50ffe8325422d9e5e4963c93eb66a373e94/audio.wav'
    # resultat = transcribe_audio(testFIchier)
    # resultat = transcribe_audio(audio_file)
    # return "%s is %s" % (cheminFichier, resultat)
    # model = whisper.load_model("base")
    model = whisper.load_model("medium")
    print (" POKUS in jbl_test the  is %s", audio_file)
    audio = whisper.load_audio(audio_file,sr=16000)
    audio_tensor = torch.from_numpy(audio).to(torch.float32)
    result = model.transcribe(audio_tensor, fp16=False)['text']
    print (" POKUS in jbl_test before returning the transcribed text: the transcribed text is %s", result)
    return result
#function to transcribe audio to text using whisper
def transcribe_audio(audio_file):
    model = whisper.load_model("base")
    print (" POKUS the  is %s", audio_file)
    audio = whisper.load_audio(audio_file,sr=16000)
    audio_tensor = torch.from_numpy(audio).to(torch.float32)
    result = model.transcribe(audio_tensor, fp16=False)['text']
    return result


#function to match the task to the input provided: audio or text
def match_task(text, audio):
    if text and audio:
        return text
    elif text:
        return text
    elif audio:
        return transcribe_audio(audio)
    else:
        return ReferenceError("No input provided.")


#function to generate phrases for the user
def llm(task, country, number):
    # llm = Ollama(model="mistral")
    llm = Ollama(model="mistral:7b", base_url='http://192.168.1.13:11434')
    lang = get_language(country, file="utils/country_to_language.json")
    few_shot = get_examples(file="utils/fewshot_learning.txt")
    context = f"You are a helpful assistant. You give an enumerated list of phrases. You answer concisely and only in {lang}."
    icl = f"For example, {few_shot}"
    query = f"I'm travelling to {country}. Which {number} most popular phrases should I learn to {task}?"
    phrases = llm.invoke(context+icl+query)    
    return phrases
    

#function to launch the application
def main():    
    demo = gr.Blocks()
    #create a gradio interface
    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        gr.Markdown("# Assistant for Travelers")
        gr.Markdown("### What do you want to do: order food in the restaurant, ask for direction, buy tickets?")
        gr.Markdown("### Record audio or enter text.")
        #create a row with two columns
        with gr.Row():
            with gr.Column():
                text = gr.Textbox(label="Enter text", placeholder="order food, ask for directions, etc.")
            with gr.Column():
                audio = gr.Audio(sources=["microphone"], label="Record your voice", type="filepath", max_length=300) 
                print("GR COLUMN - DOnc voilà le audio: [%s]", audio)
        # create a row with two blocks
        with gr.Row():
            country = gr.Radio(["France", "Germany", "Italy", "Spain"], label="Location", info="Where are you travelling?")
            num = gr.Slider(0, 10, value=5, step=1, info="How many phrases?", label="Number of phrases")    
        #create a row with two buttons
        with gr.Row():
            with gr.Column():
                response = gr.Button("Generate response", variant="primary")
            with gr.Column():
                clear = gr.Button("Clear")
        #create a row for response
        with gr.Row():
            out = gr.Textbox(label="Response")
            task = match_task(text, audio)

        
        response.click(fn=jbl_test, inputs=[audio], outputs=out)
        # response.click(fn=llm, inputs=[task, country, num], outputs=out) 
        # response.click(fn=transcribe_audio, inputs=[audio], outputs=out) 
        # gr.ClearButton.add(clear, [text, audio, country, num, out])   
    demo.queue(status_update_rate = "auto")
    demo.launch(share=False, debug=True, server_name='0.0.0.0')


if __name__ == '__main__':
    main()