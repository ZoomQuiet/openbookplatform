from apps.site.models import BlogSite

def siteinfo(request):
    sites = BlogSite.objects.all()
    if len(sites) > 0:
        site = sites[0]
    else:
        site = None
    return {'site': site}
