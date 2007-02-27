def get_full_path(request):
    return 'http://' + request.META['HTTP_HOST'] + request.path