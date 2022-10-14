import os

class Config:
    version = "1.1.0"
    start_banner = f"""
                              __            _____ __
      _________  __  ______  / /____  _____/ __(_) /_
     / ___/ __ \/ / / / __ \/ __/ _ \/ ___/ /_/ / __/
    / /__/ /_/ / /_/ / / / / /_/  __/ /  / __/ / /
    \___/\____/\__,_/_/ /_/\__/\___/_/  /_/ /_/\__/

                    Version: {version}
        
    """

    counterfit_dir = "counterfit"
    targets_dir = "../targets"
    supported_data_types = [
        "image",
        "tabular"
    ]



