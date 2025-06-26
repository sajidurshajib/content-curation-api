import json

from fastapi.responses import JSONResponse


def standard_response(status, success, message, data):
	if isinstance(data, str):
		try:
			data = json.loads(data)
		except json.JSONDecodeError:
			pass
	return JSONResponse(
		status_code=status,
		content={'success': success, 'message': message, 'data': data},
	)
