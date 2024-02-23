from django.urls import path

from . import views

# when using Categories, and CategoryDetail ( APIVew )
urlpatterns = [
    path("", views.Categories.as_view()),
    path("<int:pk>", views.CategoryDetail.as_view()),
]


# # when using CategoryViewSet ( ModelViewSet )
# urlpatterns = [
#     path(
#         "",
#         views.CategoryViewSet.as_view(
#             {
#                 "get": "list",
#                 "post": "create",
#             }
#         ),
#     ),
#     path(
#         "<int:pk>",
#         views.CategoryViewSet.as_view(
#             {
#                 "get": "list",
#                 "post": "create",
#                 "put": "update",
#                 "delete": "destroy",
#             }
#         ),
#     ),
# ]
