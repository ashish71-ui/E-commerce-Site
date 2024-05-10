

from django.contrib import admin
from django.urls import path , include
from core.views import index
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("core.urls")),
     path('user/', include("userauths.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




# a59641e7-d0cd-43e9-87b4-d134dcc004f8

# c54724d1-1352-411e-b575-c1b4536553ee

# dc41ab9c-84c3-4a74-9142-92c8f5bde052

# 65df59f0-88dd-479f-8396-2f53ae4d7cbb

# cd476f27-53b6-4bff-8258-cf38f9c1e4a3

# ee5b8a8b-b3a5-44ed-860c-f83f55be6150

# 08e77816-238f-4dfd-a5e5-04d70989f8d6

# 7b2cd9c1-3239-42f7-b2cf-e9d2e538ee2d
