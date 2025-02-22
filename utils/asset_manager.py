from pathlib import Path

# Base directory for assets
ASSETS_BASE_PATH = Path(r"C:\Users\RAJAVEL MS\myproject\TestAPI\assets")

def get_asset_path(page_name: str, filename: str) -> str:
    """
    Returns the absolute path to an asset file located in a specific page's folder.

    Parameters:
    - page_name (str): The name of the page (folder) where the asset is stored.
    - filename (str): The name of the asset file.

    Returns:
    - str: The absolute path to the requested asset file.
    """
    asset_path = ASSETS_BASE_PATH / page_name / filename
    if not asset_path.exists():
        raise FileNotFoundError(f"Asset '{filename}' not found in '{page_name}' directory.")
    return str(asset_path)
