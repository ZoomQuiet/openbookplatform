from django.contrib.contenttypes.models import ContentType

def get(generic_model, relate_obj, **kwargs):
    ctype = ContentType.objects.get_for_model(relate_obj)
    return generic_model.objects.get(content_type__pk=ctype.id, object_id=relate_obj.id, **kwargs)

def get_or_none(generic_model, relate_obj, **kwargs):
    try:
        return get(generic_model, relate_obj, **kwargs)
    except generic_model.DoesNotExist:
        return None
    
def all(generic_model, relate_obj, **kwargs):
    ctype = ContentType.objects.get_for_model(relate_obj)
    return generic_model.objects.filter(content_type__pk=ctype.id, object_id=relate_obj.id, **kwargs)

