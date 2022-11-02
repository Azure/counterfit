from . import core, data, frameworks, reporting, targets
from .core.attacks import CFAttack
from .core.core import Counterfit
from .core.frameworks import CFFramework
from .core.logger import CFLogger
from .core.options import CFOptions
from .core.output import CFPrint
from .core.targets import CFTarget

import os
import warnings

# make tensorflow quiet
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
warnings.filterwarnings('ignore')

__version__ = '1.1.0'
name = 'counterfit'
