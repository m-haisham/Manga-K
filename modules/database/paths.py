from pathlib import Path

# directories
base_directory = Path('data')
base_directory.mkdir(parents=True, exist_ok=True)

# base
base_path = base_directory / Path('base.db')

# meta
meta_path = base_directory / Path('meta.db')

# manga info
mangas_directory = base_directory / Path('manga')
mangas_directory.mkdir(parents=True, exist_ok=True)

# manga saves
# mangas_save_directory = base_directory / Path('manga')
# mangas_save_directory.mkdir(parents=True, exist_ok=True)