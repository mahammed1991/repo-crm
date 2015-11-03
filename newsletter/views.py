from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def archive(request):
    """ Newsletter Archive list """
    return render(request, 'newsletter/archive.html')


@login_required
def get_newsletter(request, vol_year, vol_month, volume):
    """ Newsletter Archive list """
    template = vol_year + '/' + vol_month + '-vol-' + volume + '.html'
    return render(request, 'newsletter/' + template)
