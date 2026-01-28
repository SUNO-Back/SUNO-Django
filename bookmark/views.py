from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from bookmark.models import  Bookmark
from django.http import Http404


# Create your views here.
def bookmark_list(request):
    bookmarks = Bookmark.objects.filter(id__gte=50)
    # .objects.all() = SELECT * FROM bookmark  bookmark전체를 가져와라.

    context ={'bookmarks':bookmarks}

    return render(request, 'bookmark_list.html', context)

def bookmark_detail(request,pk):
    # try:
    #     bookmark = Bookmark.objects.get(pk=pk)
    # except:
    #     raise Http404

    # 이건 위에 try문 한줄로 줄인것
    # Bookmark에서 get으로 pk=pk조건으로 가져오는데 오류나면 404 보냄
    bookmark = get_object_or_404(Bookmark,pk=pk)

    context = {'bookmark':bookmark}
    return render(request, 'bookmark_detail.html', context)