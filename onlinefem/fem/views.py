import requests as req
from django.http import JsonResponse


def dolfin_view(request):
    r""""""
    data = {'name': 'numbers'}
    r = req.post('http://femdolfinx:5555', data)
    out = r.json()
    if out is None:
        return JsonResponse({'out': 'nothing'})
    else:
        n = out['numbers']
        x = n[1] + n[2]
        return JsonResponse({'out': x})
