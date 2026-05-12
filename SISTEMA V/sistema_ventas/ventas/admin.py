from django.contrib import admin
from .models import Categoria, Producto, Cliente, Pedido, DetallePedido


# Register your models here.
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", )
    search_fields = ("nombre", )


admin.site.register(Categoria, CategoriaAdmin)


class ProductoAdmin(admin.ModelAdmin):
    list_display = ("categoria", "codigo", "nombre", "precio", "stock")
    search_fields = ("categoria", "codigo", "nombre", "precio", "stock")


admin.site.register(Producto, ProductoAdmin)


class ClienteAdmin(admin.ModelAdmin):
    list_display = ("cedula", "nombres", "apellidos", "correo", "telefono", "fecha_nacimiento", "direccion")
    search_fields = ("cedula", "nombres", "apellidos", "correo", "telefono", "fecha_nacimiento", "direccion")


admin.site.register(Cliente, ClienteAdmin)


class PedidoAdmin(admin.ModelAdmin):
    list_display = ("cliente", "fecha", "total")
    search_fields = ("cliente", "fecha", "total")


admin.site.register(Pedido, PedidoAdmin)


class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ("pedido", "producto", "cantidad", "subtotal")
    search_fields = ("pedido", "producto", "cantidad",  "subtotal")


admin.site.register(DetallePedido, DetallePedidoAdmin)
