from django.apps import AppConfig
import logging
from django.conf import settings
# import openai

logger = logging.getLogger(__name__)

class SearchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'search'

    def ready(self):
        import os
        import pathlib
        from langchain.document_loaders import PyPDFDirectoryLoader
        from langchain.indexes import VectorstoreIndexCreator
        from .papers_paths import PATHS
        from .secret_key import API_KEY
        from .models import ResearchPaper

        paper_incremental_id = 0
        os.environ["OPENAI_API_KEY"] = API_KEY

        all_papers = list()
        loaders = list()
        for path in PATHS:
            logger.warning('~~~ Processing one dir path: ' + path)
            loaders.append(PyPDFDirectoryLoader(path))

            pathlib_path = pathlib.Path(path)
            all_papers.extend(pathlib_path.iterdir())

            for one_paper_path in all_papers:
                paper_object = ResearchPaper(paper_id=paper_incremental_id, absolute_path=one_paper_path)
                paper_object.save()
                paper_incremental_id += 1

        logger.warning("!!! All paperssss: " + str(all_papers))
        index = VectorstoreIndexCreator().from_loaders(loaders)
        logger.warning('!!! All papers added. Paths: ' + str(all_papers))
        settings.LANGCHAIN_INDEX = index
        logger.warning('Initialized langchain index: ' + str(settings.LANGCHAIN_INDEX))
