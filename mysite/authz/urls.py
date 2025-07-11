from django.urls import path

from . import views
from authz.views import ProtectedView, MyLogout, ManualForm, SaveFileView, list_my_directory, serve_text_file
app_name = "authz"
urlpatterns = [
    path("", views.main, name="main"),
    path("orgmode/", views.orgmode, name="orgmode"),
    path("protect/", ProtectedView.as_view(), name="protect"),
    path("context_testing/", views.context_testing, name="context_testing"),
    path("logout/", MyLogout.as_view(), name="logout"),
    path("form/", ManualForm.as_view(), name="form"),
    path("modelform/", views.AuthorList.as_view(), name="author_list"),
    path("modelform/<int:pk>/", views.AuthorDetail.as_view(), name="author_detail"),
    path("modelform/create/", views.AuthorCreate.as_view(), name="author_create"),
    path("modelform/<int:pk>/delete/", views.AuthorDelete.as_view(), name="author_delete"),
    path("modelform/<int:pk>/update/", views.AuthorUpdate.as_view(), name="author_update"),
    path("modelform/bookcreate/", views.BookCreate.as_view(), name="book_create"),
    path("modelform/<int:pk>/bookdelete/", views.BookDelete.as_view(), name="book_delete"),
    path("modelform/<int:pk>/bookupdate/", views.BookUpdate.as_view(), name="book_update"),
    path("ownerupdate/<int:pk>/", views.OwnerAuthorUpdate.as_view(), name="owner_update"),
    path('open/', list_my_directory.as_view(), name='list_my_directory'),
    path('open/<str:filename>/', serve_text_file.as_view(), name='serve_text_file'),
    path('save_file/', SaveFileView.as_view(), name='save_file'),
]