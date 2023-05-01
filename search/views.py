import logging
from django.shortcuts import render


logger = logging.getLogger(__name__)


def search(request):
    logger.warning("!!! Entered 'search'.")
    return render(request, 'search/home.html', {})
