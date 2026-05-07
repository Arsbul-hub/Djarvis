from datetime import datetime

from app.executor import memory_manager, speech_manager


def execute(*args, **kwargs):
    if "last_greeting" in memory_manager:
        if (datetime.now() - memory_manager["last_greeting"]).seconds / 60 < 20:
            if memory_manager.get("greetings_count", 0) > 2:
                # Ничего не говорим
                memory_manager["last_greeting"] = datetime.now()
                memory_manager["greetings_count"] = memory_manager.get("greetings_count", 0) + 1
            else:
                speech_manager.say("Мы уже здоровались недавно")
                memory_manager["greetings_count"] = memory_manager.get("greetings_count", 0) + 1
    
        else:
            speech_manager.say("Привет")
            memory_manager["greetings_count"] = 0
            memory_manager["last_greeting"] = datetime.now()
    
    else:
        speech_manager.say("Привет")
        memory_manager["greetings_count"] = 0
        memory_manager["last_greeting"] = datetime.now()