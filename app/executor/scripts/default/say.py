from app.executor import speech_manager


def execute( *args, **kwargs):
    speech_manager.say(args[0])

