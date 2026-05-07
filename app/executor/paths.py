from app.executor.scripts.default import say, greeting
from app.executor.scripts.error import e404, e4041


DEFAULT_SCRIPTS_PATHS = {
    "say": say.execute,
    "greeting": greeting.execute,

}
ERROR_SCRIPTS_PATHS = {
    404: e404.execute,
    4041: e4041.execute
}