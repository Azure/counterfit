import orjson
from counterfit.core.logging import CFAttackLogger

class DefaultLogger(CFAttackLogger):
    """The default logger. Only logs the number of queries against a model.
    """
    def __init__(self, **kwargs):
        self.num_queries = 0

    def log(self, item):
        self.num_queries += 1

class ListLogger(CFAttackLogger):
    """Logs queries to a list.
    """
    def __init__(self, **kwargs):
        self.logs = []
        self.queries = 0

    def log(self, item):
        self.logs.append(item)
        self.queries += 1
        
class JSONLogger(CFAttackLogger):
    """Logs queries to a json file saved to disk.
    """
    def __init__(self, filepath):
        self.num_queries = 0
        self.filename = f"{filepath}/logs.json"

    def log(self, item):
        with open(self.filename, "a+") as log_file:
            data = orjson.dumps(
                item,
                option=orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_APPEND_NEWLINE
            )

            log_file.write(data.decode())
            self.num_queries += 1

def get_attack_logger_obj(logger_type: str) -> object:
    """Factory method to get the requested logger.

    Args:
        logger_type ([type]): [description]

    Raises:
        KeyError: [description]

    Returns:
        [type]: [description]
    """

    attack_logger_obj_map = {
        'default': DefaultLogger,
        'list': ListLogger,
        'json': JSONLogger
    }

    if logger_type not in attack_logger_obj_map:
        raise KeyError(
            f'Logger is not supported {logger_type}...Please provide one of: {list(attack_logger_obj_map.keys())}...')

    return attack_logger_obj_map[logger_type]
