from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View

from .forms import SubmitUrlForm
from .models import KirrURL

"""
# Create your views here.
def kirr_redirect_view(request, shortcode=None, *args, **kwargs):
    print(args)
    print(shortcode)
    #try:
    #    obj = KirrURL.objects.get(shortcode=shortcode)
    ##except BaseException:
    #   obj = KirrURL.objects.all().first()

    # obj_url = None
    # qs = KirrURL.objects.filter(shortcode__iexact=shortcode.upper())
    # if qs.exists() and qs.count() == 1:
    #     obj = qs.first()
    #     obj_url = obj.url

    obj = get_object_or_404(KirrURL, shortcode=shortcode)
    #return HttpResponse("hello {sc}".format(sc=obj.url))
    return HttpResponseRedirect(obj.url)
"""

class HomeView(View):
    def get(self, request, *args, **kwargs):
        the_form = SubmitUrlForm()        
        context = {
            'title': 'Submit URL',
            'form': the_form
        }
        return render(request, "home.html", context)

    def post(self, request, *args, **kwargs):
        print("HomeView post ", request.POST)
        form = SubmitUrlForm(request.POST)
        context = {
            'title': 'Submit URL',
            'form': form
        }
        template = "home.html"
        if form.is_valid():
            print("HomeView cleaned_data ", form.cleaned_data)
            url = form.cleaned_data.get("url")
            obj, created = KirrURL.objects.get_or_create(url=url)
            context = {"object":obj, "created": created}
            if created:
                template = "success.html"
            else:
                template = "already-exists.html"

        
        return render(request, template, context)

class KirrCBView(View):

    def get(self, request, shortcode=None, *args, **kwargs):
        obj = get_object_or_404(KirrURL, shortcode=shortcode)
        #return HttpResponse("hello {sc}".format(sc=obj.url))
        return HttpResponseRedirect(obj.url)

    def post(self, request, *args, **kwargs):
        return HttpResponse()