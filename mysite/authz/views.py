from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from authz.forms import BasicForm, AuthorForm
from django.http import HttpResponse, Http404
from .models import Author, Book
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from authz.owner import OwnerUpdateView
import os
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.contrib.auth.views import LogoutView
def main(request):
    # code kiểm tra authenticated để trong template
    # Có lẽ để code kiểm tra authenticated trong view sẽ gọn gàng hơn
    return render(request, "authz/main.html", {'next':'authz/'})

class serve_text_file(LoginRequiredMixin, View):
    def get(self, request, filename):
        # Define the directory where your .txt files are stored
        base_dir = '/home/DjangoN1/trieudtc.github.io/org_files'

        # Sanitize the filename to prevent directory traversal attacks
        safe_filename = os.path.basename(filename)
        file_path = os.path.join(base_dir, safe_filename)

        # Check if file exists and serve i
        allowed_extensions = ('.txt', '.org', '.html', '.csv')
        if os.path.exists(file_path) and file_path.endswith(allowed_extensions):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return render(request, 'authz/orgmode.html', {'content': content, 'filename': filename})
        else:
            raise Http404("Text file not found.")

def orgmode(request):
    return render(request, 'authz/orgmode.html', {'content': "", 'filename': "new_file"})



class ProtectedView(LoginRequiredMixin, View):
    def get(seft, request):
        # tự động chuyển về trang login nếu chưa login
        # accounts/login/?next=/authz/protect/
        # Có lẽ overide việc redirect được, đọc thêm docs
        return render(request, 'authz/login_required_mixin.html')

def context_testing(request):
    x = 3
    y = 4
    return render(request, 'authz/context_testing.html', {'y':y})

class MyLogout(LogoutView):
    template_name = 'registration/logout.html'

class ManualForm(View):
    def get(self, request):
        old_data = {'name': 'Trung Quân', 'age': 25, 'birth_date': '2020-15-01'}
        form = BasicForm(initial=old_data)
        return render(request, 'authz/form.html', {'form':form})

    def post(self, request):
        #load data từ user vào form
        form = BasicForm(request.POST)
        #Validating. It may pass Browser validation but still not validated
        if not form.is_valid():
            return render(request, 'authz/form.html', {'form':form})
        #Save data
        return redirect('/authz/form/') #Nên redirect sau POST thành công vì khi web refresh sẽ dubble POST

# view cho model sách
class AuthorList(generic.ListView):
    model = Author
    template_name = "authz/author_list.html"

class OwnerAuthorUpdate(OwnerUpdateView):
    model = Author
    template_name = "authz/author_update.html"
    fields = '__all__'

class AuthorDetail(generic.DetailView):
    model = Author
    template_name = "authz/author_detail.html"

#creat, update, delete views

class AuthorCreate(View):
    template = 'authz/author_create_form.html'
    success_url = reverse_lazy('authz:author_list')

    def get(self, request):
        form = AuthorForm()
        ctx = {'form': form}
        return render(request, self.template, ctx)

    def post(self, request):
        form = AuthorForm(request.POST)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template, ctx)

        form.save()
        return redirect(self.success_url)

class AuthorDelete(View):
    model = Author
    success_url = reverse_lazy('authz:author_list')
    template = 'authz/author_confirm_delete.html'

    def get(self, request, pk):
        aut = get_object_or_404(self.model, pk=pk)
        ctx = {'author': aut}
        return render(request, self.template, ctx)

    def post(self, request, pk):
        aut = get_object_or_404(self.model, pk=pk)
        aut.delete()
        return redirect(self.success_url)

class AuthorUpdate(generic.DetailView):
    model = Author
    success_url = reverse_lazy('authz:author_list')
    template_name = 'authz/author_detail.html'
    def get(self, request, pk):
        aut = get_object_or_404(self.model, pk=pk)
        form = AuthorForm(instance=aut)
        self.object = self.get_object()
        '''
        The base implementation of this method requires that the self.object attribute be set by the view (even if None).
        Be sure to do this if you are using this mixin without one of the built-in views that does so
        '''
        ctx = self.get_context_data()
        ctx["form"] = form

        return render(request, self.template_name, ctx)

    def post(self, request, pk):
        aut = get_object_or_404(self.model, pk=pk)
        form = AuthorForm(request.POST, instance=aut)
        if not form.is_valid():
            self.object = self.get_object()
            ctx = self.get_context_data()

            ctx["form"] = form
            return render(request, self.template_name, ctx)

        form.save()
        return redirect(self.success_url)
class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('authz:author_list')

class BookDelete(DeleteView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('authz:author_list')
class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('authz:author_list')
class list_my_directory(LoginRequiredMixin, View):
    def get(self, request):
        # Set the absolute path to your target directory
        base_dir = '/home/DjangoN1/trieudtc.github.io/org_files'  # <- Change this to the real path

        if not os.path.isdir(base_dir):
            raise Http404("Directory not found.")

        try:
            entries = os.listdir(base_dir)
            entries = sorted(entries, key=lambda e: (not os.path.isdir(os.path.join(base_dir, e)), e.lower()))
        except OSError as e:
            return HttpResponse(f"Error reading directory: {e}", status=500)

        context = {
            'directory_name': 'myDirectory',
            'entries': entries,
        }
        return render(request, 'authz/list_my_directory.html', context)




from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator


# Allowed extensions
ALLOWED_EXTENSIONS = {'.txt', '.org', '.csv', '.html'}

# Save directory
SAVE_DIR = '/home/DjangoN1/trieudtc.github.io/org_files'
os.makedirs(SAVE_DIR, exist_ok=True)


@method_decorator(csrf_protect, name='dispatch')
class SaveFileView(LoginRequiredMixin, View):
    login_url = None  # disables redirect
    raise_exception = False  # prevents HTTP 403 by default

    def handle_no_permission(self):
        return JsonResponse({
            'success': False,
            'error': 'Authentication required. Please log in.'
        }, status=401)  # or 403 if you prefer

    def post(self, request):
        filename = request.POST.get('filename')
        content = request.POST.get('content')

        if not filename or not content:
            return JsonResponse({'success': False, 'error': 'Missing filename or content.'}, status=400)

        _, ext = os.path.splitext(filename.lower())
        if ext not in ALLOWED_EXTENSIONS:
            return JsonResponse({'success': False, 'error': f'File extension "{ext}" is not allowed.'}, status=400)

        filepath = os.path.join(SAVE_DIR, os.path.basename(filename))

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return JsonResponse({'success': True, 'message': f'File saved as {filename}'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)