from django.shortcuts import redirect

def redirect_view(request):
    """Return the response for root URL."""
    response = redirect('/cities/')
    return response