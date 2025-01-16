# views.py
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.validators import URLValidator
from .tasks import scrape_products


class ScrapeURL(APIView):
    def get(self, request):
        try:
            urls = request.data['url']
            if not urls:
                return Response({'success': False, 'message': 'No URLs provided'}, status=status.HTTP_400_BAD_REQUEST)
            validator = URLValidator()
            for url in urls:
                try:
                    validator(url)
                except:
                    return Response({'success': False, 'message': f'Invalid URL: {url}'}, status=status.HTTP_400_BAD_REQUEST)
            task_results = []
            for url in urls:
                task = scrape_products.apply_async(args=[url])
                task_result = task.get(timeout=300)
                task_results.append(task_result)
            return Response({'success': True, 'scrapped_urls': task_results}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error: {e}")
            return Response({'success': False, 'message': 'Error'}, status=status.HTTP_400_BAD_REQUEST)
