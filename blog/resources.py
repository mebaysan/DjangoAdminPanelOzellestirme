from import_export import resources
from blog.models import Yorum


class YorumResource(resources.ModelResource):
    class Meta:
        model = Yorum # default all fields
        # fields = ('yayin_Mi','blog')
