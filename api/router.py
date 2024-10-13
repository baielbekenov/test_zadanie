from django.urls import path, include


urlpatterns = [
    path("authentication/", include("api.authentication.urls")),
    path("websocket/",  include("api.authentication.routing")),
    path("products/", include("api.products.urls")),
    path("category/", include("api.category.urls")),
    path("docs/", include("api.openapi.urls")),
]