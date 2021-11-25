def GET_REQUEST(request):
	if request.method=='GET':
		return True
	else:
		return False

def POST_REQUEST(request):
	if request.method=='POST':
		return True
	else:
		return False

def PUT_REQUEST(request):
	if request.method=='PUT':
		return True
	else:
		return False

def DELETE_REQUEST(request):
	if request.method=='DELETE':
		return True
	else:
		return False
		
def custom_request_type(data,req_type):
	if data['request_type']== req_type :
		return True
	else:
		return False
