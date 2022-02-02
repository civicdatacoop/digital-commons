import shutil
from pathlib import Path
import crinita as cr
import json
import datetime

# Constants
PATH_TO_OUTPUTS: Path = Path('docs')
PATH_TO_CONFIG_JSON: Path = Path('config.json')
PATH_TO_PAGES: Path = Path('./pages')
PATH_TO_ARTICLES: Path = Path('./articles')
PATH_TO_DATASETS: Path = Path('./catalogue')

# CREATE FOLDER FOR OUTPUTS
# Remove all old content
shutil.rmtree(PATH_TO_OUTPUTS)
# Create output folder again
PATH_TO_OUTPUTS.mkdir(exist_ok=True)

# RUN CRINITA
# 1. Load config:
cr.Config.from_json(PATH_TO_CONFIG_JSON.open('r').read())
# Common parameters
cr.Config.global_template_parameters = {
    'generated_date': datetime.date.today().strftime("%B %Y")
}
# 2. Load entities:
page_files = [f_p for f_p in PATH_TO_PAGES.iterdir() if f_p.is_file()]
page_list: list[dict] = [json.load(fh.open()) for fh in page_files]
article_files = [f_p for f_p in PATH_TO_ARTICLES.iterdir() if f_p.is_file()]
article_list: list[dict] = [json.load(fh.open()) for fh in article_files]
dataset_files = [f_p for f_p in PATH_TO_DATASETS.iterdir() if f_p.is_file()]
dataset_list: list[dict] = [json.load(fh.open()) for fh in dataset_files]
# 3. Create website content:
website = cr.Sites.sites_from_json(
    {"list_of_entities": [*page_list, *article_list, *dataset_list]}
)
# 4. Generate pages:
website.generate_pages(
    # Output path
    Path(PATH_TO_OUTPUTS), rewrite_if_exists=True
)
