import logging
import os
from django.shortcuts import render
from django.conf import settings
from django.http import FileResponse
from .secret_key import API_KEY as SECRET_API_KEY
from .papers_paths import PATHS
from .models import ResearchPaper


logger = logging.getLogger(__name__)


def find_paper_in_db(paper_path: str):
    all_papers = ResearchPaper.objects.all()
    for paper in all_papers:
        if paper_path in paper.absolute_path:
            return paper
    return None

def search(request):
    question = request.GET.get('search')
    if question is None:
        return render(request, 'search/home.html', {'query': question})
    os.environ["OPENAI_API_KEY"] = SECRET_API_KEY
    llm_answer = settings.LANGCHAIN_INDEX.query_with_sources(question)
    logger.info("Question: " + str(question))
    logger.info("llm_answer: " + str(llm_answer))
    # Verify sources.
    sources = llm_answer['sources']

    sources_str_list = list()
    sources_objects = list()
    paper_id = 0
    while sources:
        index = sources.find('.pdf')
        if index == -1:
            sources = ""
        else:
            one_source = sources[:index + 4]
            if one_source[0] == ',' and one_source[1] == ' ':
                one_source = one_source[2:]
            one_source = one_source.strip()
            sources_str_list.append(one_source)

            found_paper = find_paper_in_db(one_source)
            if not found_paper:
                logger.warning("Could not find paper with path in the db: " + one_source)
            else:
                sources_objects.append(found_paper)

            paper_id += 1
            sources = sources[index + 4:]

    file_response_sources = list()
    for source_path in sources_str_list:
        if PATHS[0] not in source_path:
            source_path = PATHS[0] + '/' + source_path
        logger.info('New source path: ' + source_path)

    return render(request, 'search/home.html', {'question': question,
                                                'answer': str(llm_answer['answer']),
                                                'sources': sources_str_list,
                                                'sources_objects': sources_objects,
                                                'file_responses': file_response_sources
                                                })


def redirect(request, paper_id):
    paper = ResearchPaper.objects.filter(paper_id=paper_id)[0]
    good_source_path = paper.absolute_path
    return FileResponse(open(good_source_path, 'rb'), content_type='application/pdf')