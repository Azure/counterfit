
class Config:
    version = "1.0.0"
    start_banner = f"""
                              __            _____ __
      _________  __  ______  / /____  _____/ __(_) /_
     / ___/ __ \/ / / / __ \/ __/ _ \/ ___/ /_/ / __/
    / /__/ /_/ / /_/ / / / / /_/  __/ /  / __/ / /
    \___/\____/\__,_/_/ /_/\__/\___/_/  /_/ /_/\__/

                    Version: {version}
        
    """

    targets_path = "counterfit/targets"
    frameworks_path = "counterfit/frameworks"
    commands_path = "counterfit/commands"

    supported_data_types = ["image", "tabular"]
