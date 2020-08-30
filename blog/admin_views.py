from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from blog.models import Blog


@staff_member_required
def get_comments(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    context = {
        'blog': blog
    }
    return render(request, 'admin/blog/get_comments.html', context=context)
