from django.http import HttpResponse,JsonResponse
from django.db.models import Func
import json
def RESPONSE(data,statusCode):
	return JsonResponse(data=data,status=statusCode,safe=False)

class Round(Func):
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 2)'

def CONVERT(obj, enc):
    if isinstance(obj, str):
        return obj.decode(enc)
    if isinstance(obj, (list, tuple)):
        return [CONVERT(item, enc) for item in obj]
    if isinstance(obj, dict):
        return {CONVERT(key, enc) : CONVERT(val, enc)
                for key, val in obj.items()}
    else: return obj

def LOAD_DATA(body):
	try:
		data=json.loads(CONVERT(body, 'cp1252'))
	except:
		json.loads(body,default="utf-8")
	else:
		data=json.dumps(body, ensure_ascii=False)
	return data