
def current_url(request):
    # Ensure the URL is safe
    return {
        'current_url': request.build_absolute_uri(request.get_full_path())
    }
