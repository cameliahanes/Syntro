from django.db import models
from django.http import FileResponse


class ResearchPaper(models.Model):
    paper_id = models.IntegerField()
    absolute_path = models.CharField(max_length=500)
    filename = models.CharField(max_length=300)

    def get_file_response(self):
        return FileResponse(open(self.absolute_path, 'rb'), content_type='application/pdf')
