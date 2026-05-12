from app.executor import speech_manager



def execute(shared_buffer, *args, **kwargs):
    speech_manager.say("Я не понял")