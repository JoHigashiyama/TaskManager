from .forms import SearchForm

def search_form(request):
    return {'searchForm':SearchForm()}