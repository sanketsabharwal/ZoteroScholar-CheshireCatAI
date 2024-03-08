import os
import glob

from cat.log import log
from cat.utils import get_static_path, get_plugins_path
from cat.mad_hatter.decorators import plugin, hook
from cat.looking_glass.cheshire_cat import CheshireCat
from cat.plugins.cat_research.zotero_downloader import ZoteroDownloader


ccat = CheshireCat()


@plugin
def save_settings(settings):
    pdf_path = os.path.join(get_static_path(), "pdf")
    if not os.path.exists(pdf_path):
        os.mkdir(pdf_path)

    zotero_downloader = ZoteroDownloader(
        settings["zotero_user_id"],
        settings["zotero_api_key"],
        pdf_path
    )
    # ccat.send_ws_message("Starting download")
    log.info("Downloading the Zotero items")
    zotero_downloader.download_pdfs()
    declarative_memory = ccat.memory.vectors.declarative

    # Loop the pds to ingest them
    log.info("Ingesting the pdfs")
    pdfs = glob.glob(os.path.join(pdf_path, "*.pdf"))
    for pdf in pdfs:
        metadata = {
            "source": pdf
        }
        # Scroll the vector db to see if the pdf already exists and prevent uploading it twice
        points = declarative_memory.client.scroll(
            collection_name="declarative",
            scroll_filter=declarative_memory._qdrant_filter_from_dict(metadata),
        )

        if len(points[0]) != 0:
            continue
        log.info(f"Ingesting {os.path.basename(pdf)}")
        ccat.rabbit_hole.ingest_file(stray=ccat, file=pdf)

    return settings
