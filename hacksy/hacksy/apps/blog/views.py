#standard django views
from django.shortcuts import *
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.comments.forms import CommentForm

from blog.models import BlogPost

def blogpost_list(request):
    context = {
        "posts": BlogPost.objects.all()
    }
    return render_to_response("blog/blogpost_list.html",context,context_instance=RequestContext(request))

def blogpost_detail(request,slug):
    post = get_object_or_404(BlogPost,slug=slug)
    context = {
        "post": post
    }
    return render_to_response("blog/blogpost_detail.html",context,context_instance=RequestContext(request))
