from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Livro
from .serializer import LivroSerializer

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs["content_type"] = "application/json"
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def livro_list_create(request):
    if request.method == 'GET':
        livros = Livro.objects.all()
        serializer = LivroSerializer(livros, many=True)
        return JSONResponse(serializer.data)
    
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = LivroSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def livro_detail(request, pk):
    try:
        livro = Livro.objects.get(pk=pk)
    except Livro.DoesNotExist:
        return JsonResponse({'error': 'Livro não encontrado'}, status=404)
    
    if request.method == 'GET':
        serializer = LivroSerializer(livro)
        return JSONResponse(serializer.data)
    
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = LivroSerializer(livro, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)
    
    if request.method == 'DELETE':
        livro.delete()
        return HttpResponse(content=None, status=204)
    return HttpResponse(status=405)