import pathlib

import orjson


class CFLogger:
    """ Base class for all loggers.
    """
    num_queries: int
    
    def __init__(self) -> None:
        pass


class BasicLogger(CFLogger):
    """ The default logger. Only logs the number of queries against a model.
    """
    def __init__(self, **kwargs):
        super(CFLogger).__init__()
        self.num_queries = 0

    def log(self, item):
        self.num_queries += 1


class JSONLogger(CFLogger):
    """Logs queries to a json file saved to disk.
    """
    def __init__(self, **kwargs):
        super(CFLogger).__init__()
        attack_id = kwargs["attack_id"]
        ts = kwargs['ts']
        self.num_queries = 0
        self.filepath = pathlib.Path(f"attack_logs/{attack_id}_{ts}_logs.json")
        self.logs = []
        self.filepath.parent.mkdir(parents=True, exist_ok=True)

    def log(self, item):
        options = orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_APPEND_NEWLINE
        data = orjson.dumps(item,option=options)
        with self.filepath.open('a+b') as fd:
            fd.write(data)
        self.logs.append(item)
        self.num_queries += 1


def get_attack_logger_obj(logger_type: str) -> CFLogger:
    """ Factory method to get the requested logger.
    """

    attack_logger_obj_map = {
        'basic': BasicLogger,
        'json': JSONLogger
    }

    if logger_type not in attack_logger_obj_map:
        raise KeyError(
            f'Logger is not supported {logger_type}...Please provide one of: {list(attack_logger_obj_map.keys())}...')

    return attack_logger_obj_map[logger_type]
