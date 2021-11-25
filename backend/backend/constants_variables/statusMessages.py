MESSAGE_SUCCESS={'msg':'Success'}
MESSAGE_INSERT={'msg':'Successfully Inserted'}
MESSAGE_UPDATE={'msg':'Successfully Updated'}
MESSAGE_DELETE={'msg':'Successfully Deleted'}
MESSAGE_CONFLICT={'msg':'Duplicate Data'}
MESSAGE_DATA_NOT_FOUND={'msg':'Data not found'}
MESSAGE_BAD_REQUEST={'msg':'Bad Request'}
MESSAGE_SERVER_ERROR={'msg':'Internal Server Error'}
MESSAGE_UNAUTHORIZED={'msg':'Session Expired'}
MESSAGE_LOGIN_UNAUTHORIZED={'msg':'Kindly Check the entered login credentials'}
MESSAGE_FORBIDDEN={'msg':'You are not authorized to access this page'}
MESSAGE_NOT_FOUND={'msg':'URL not found'}
MESSAGE_METHOD_NOT_ALLOWED={'msg':'Invalid request method'}
MESSAGE_SERVICE_UNAVAILABLE={'msg':'Service Currently Unavailable. Sorry for the inconvenience.'}
MESSAGE_ALREADY_FILLED={'msg':'Form already filled.'}
MESSAGE_FILLED={'msg':'Form filled.'}
MESSAGE_NOT_ELEGIBLE={'msg':'Not Eligible for filling Form.'}
MESSAGE_PORTAL_LOCKED={'msg':'Portal is Locked, please contact Dean Academics office to unlock the portal.'}
FEATURE_IS_NOT_SUPPORTED_FOR_SESSION={'msg':'Feature is not supported by Current Session. Please change the session.'}

def CUSTOM_MESSAGE(msg):
	return {'msg':msg}