from django.urls import path
from . import views

app_name = "ventas"

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login_view"),
    path("logout/", views.logout_view, name="logout_view"),
    path("register/", views.register_view, name="register_view"),
    path("menu/", views.menu_principal, name="menu_principal"),

    path("categorias/", views.listar_categorias, name="listar_categorias"),
    path("categorias/crear/", views.crear_categoria, name="crear_categoria"),
    path("categorias/editar/<int:pk>/", views.editar_categoria, name="editar_categoria"),
    path("categorias/eliminar/<int:pk>/", views.eliminar_categoria, name="eliminar_categoria"),

    path("productos/", views.listar_productos, name="listar_productos"),
    path("productos/crear/", views.crear_producto, name="crear_producto"),
    path("productos/editar/<int:pk>/", views.editar_producto, name="editar_producto"),
    path("productos/eliminar/<int:pk>/", views.eliminar_producto, name="eliminar_producto"),

    path("clientes/", views.listar_clientes, name="listar_clientes"),
    path("clientes/crear/", views.crear_cliente, name="crear_cliente"),
    path("clientes/editar/<int:pk>/", views.editar_cliente, name="editar_cliente"),
    path("clientes/eliminar/<int:pk>/", views.eliminar_cliente, name="eliminar_cliente"),

    path("pedidos/", views.listar_pedidos, name="listar_pedidos"),
    path("pedidos/crear/", views.crear_pedido, name="crear_pedido"),
    path("pedidos/editar/<int:pk>/", views.editar_pedido, name="editar_pedido"),
    path("pedidos/eliminar/<int:pk>/", views.eliminar_pedido, name="eliminar_pedido"),

    path("detalles/editar/<int:pk>/", views.editar_detalle, name="editar_detalle"),
    path("detalles/eliminar/<int:pk>/", views.eliminar_detalle, name="eliminar_detalle"),
]
