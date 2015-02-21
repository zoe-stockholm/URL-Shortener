from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from shortener.forms import URLInputForm
from shortener.models import URLPair
from urlparse import urlparse


def file_len(fname):
    """
    Calculates the number of lines of the file
    return the result
    """
    with open(fname) as f:
        i = 1
        for i, l in enumerate(f):
            pass
    return i + 1


def shorten_url(request):
    """
    View for submitting a URL which need to be shortened

    If successfully,
    Returns a HttpResponse with the dict {'original_url': new_url_pair.original_url,
                                          'shortened_url': new_url_pair.shortened_url}
    to template 'result_page.html'

    If the input URL is invalid or missing,
    Return a HttpResponse with the dict {'message': 'The input URL is invalid.'}
    to template 'shortening_failed_page.html'

    If the input URL is not able to be shortened,
    Return a HttpResponse with the dict {'message': 'The input URL is unshortenable.'}
    to template 'shortening_failed_page.html'

    If request.method != 'POST',
    Return a HttpResponse back to the template 'front_page.html'

    If the URL input was shortened before,
    Return a HttpResponse with the dict {'original_url': new_url_pair.original_url,
                                          'shortened_url': new_url_pair.shortened_url}
    to template 'shorten_url_existed_page.html'

    """

    if request.method == 'POST':
        form = URLInputForm(request.POST)
        if not form.is_valid():
            return render_to_response('shortening_failed_page.html',
                                      {'message': 'The input URL is invalid.'},
                                      context_instance=RequestContext(request))

        url_input = form.cleaned_data['url_input']

        # # handle if this URL input is not able to be shortened.
        if not urlparse(url_input).path[1:]:
            return render_to_response('shortening_failed_page.html',
                                      {'message': 'The input URL is unshortenable.'},
                                      context_instance=RequestContext(request))

        # # handle if this URL input was shortened before.
        if URLPair.objects.filter(original_url=url_input).exists():
            url_pair = URLPair.objects.get(original_url=url_input)
            result_return = {'original_url': url_pair.original_url,
                             'shortened_url': url_pair.shortened_url
                             }
            return render_to_response('shorten_url_existed_page.html',
                                      result_return,
                                      context_instance=RequestContext(request))

        # # handle if all words in wordslist were used
        if file_len(settings.PROJECT_ROOT + settings.TEST_DATA_PATH) == len(URLPair.objects.all()):
            URLPair.objects.order_by('created')[0].delete()

        # if file_len(settings.PROJECT_ROOT + settings.TEST_SMALL_DATA_PATH) == len(URLPair.objects.all()):
        #     URLPair.objects.order_by('created')[0].delete()

        new_url_pair = URLPair.objects.create_url_pair(original_url=url_input)

        result_return = {'original_url': new_url_pair.original_url,
                         'shortened_url': new_url_pair.shortened_url
                         }
        return render_to_response('result_page.html',
                                  result_return, context_instance=RequestContext(request))

    else:
        form = URLInputForm()
        return render_to_response('front_page.html', {'form': form},
                                  context_instance=RequestContext(request)
                                  )


def redirect(request, key):
    """
    View which gets the link for the given key value and redirects to it.
    """

    url_pair = get_object_or_404(URLPair, key=key)
    url_pair.save()
    return HttpResponsePermanentRedirect(url_pair.original_url)


