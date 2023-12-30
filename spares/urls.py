from django.urls import path

from spares.views import *

urlpatterns = [
    # Набор методов для услуг (Авизапчастей)
    path('api/spares/', get_spares), #
    path('api/spares/search', search_spares), # GET
    path('api/spares/<int:pk>/', get_spare), # GET
    path('api/spares/<int:pk>/image', get_spare_image), # GET
    path('api/spares/<int:pk>/update', update_spare), # PUT
    path('api/spares/<int:pk>/delete/', delete_spare), # DELETE
    path('api/spares/create/', create_spare), # POST
    path('api/spares/<int:pk>/add_to_order/', add_to_order), # POST

    # Набор методов для заявок (Заказов)
    path('api/orders/', get_orders),  # GET
    path('api/orders/<int:pk>/', get_order),  # GET
    path('api/orders/<int:pk>/update/', update_order),  # PUT
    path('api/orders/<int:pk>/update_status_user/', update_order_user),  # PUT
    path('api/orders/<int:pk>/update_status_admin/', update_order_admin),  # PUT
    path('api/orders/<int:pk>/delete/', delete_order),  # DELETE
    path('api/orders/<int:order_id>/delete_spare/<int:spare_id>/', delete_spare_from_order), # DELETE
]