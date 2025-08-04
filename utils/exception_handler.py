from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    print("its running")
    if response is not None:
        # Format ulang error detail
        errors = response.data
        if isinstance(errors, dict):
            # Ambil error pertama yang tersedia
            first_key = next(iter(errors))
            first_error = errors[first_key][0]
            response.data = {
                'status': False,
                'message': str(first_error)
            }
        else:
            response.data = {
                'status': False,
                'message': str(errors[0])
            }

    return response
