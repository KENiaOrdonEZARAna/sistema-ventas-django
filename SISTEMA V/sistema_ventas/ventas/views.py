from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria, Producto, Cliente, Pedido, DetallePedido
from .forms import CategoriaForm, ProductoForm, ClienteForm, PedidoForm, DetallePedidoForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    return redirect("ventas:login_view")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not User.objects.filter(username=username).exists():
            messages.error(request, "Usuario no registrado")
            return render(request, "auth/login.html")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("ventas:menu_principal")
        else:
            messages.error(request, "Credenciales incorrectas")
            return render(request, "auth/login.html")
    return render(request, "auth/login.html")


def logout_view(request):
    logout(request)
    return redirect("ventas:login_view")


def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Registro creado. Puedes iniciar sesión ahora.")
        return redirect("ventas:login_view")
    return render(request, "auth/register.html", {"form": form})


@login_required
def menu_principal(request):
    total_productos = Producto.objects.count()
    total_categorias = Categoria.objects.count()
    total_clientes = Cliente.objects.count()
    total_pedidos = Pedido.objects.count()
    return render(request, "menu/menu_principal.html", {
        "total_productos": total_productos,
        "total_categorias": total_categorias,
        "total_clientes": total_clientes,
        "total_pedidos": total_pedidos
    })


@login_required
def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, "categorias/listar.html", {"categorias": categorias})


@login_required
def crear_categoria(request):
    form = CategoriaForm(request.POST or None)
    if form.is_valid():
        form.cleaned_data["nombre"] = form.cleaned_data["nombre"].strip().capitalize()
        form.save()
        messages.success(request, "Categoría creada con éxito")
        return redirect("ventas:listar_categorias")
    return render(request, "categorias/crear.html", {"form": form})


@login_required
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    form = CategoriaForm(request.POST or None, instance=categoria)
    if form.is_valid():
        form.cleaned_data["nombre"] = form.cleaned_data["nombre"].strip().capitalize()
        form.save()
        messages.success(request, "Categoría actualizada")
        return redirect("ventas:listar_categorias")
    return render(request, "categorias/editar.html", {"form": form, "categoria": categoria})


@login_required
def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == "POST":
        categoria.delete()
        messages.success(request, "Categoría eliminada")
        return redirect("ventas:listar_categorias")
    return render(request, "categorias/eliminar.html", {"categoria": categoria})



@login_required
def listar_productos(request):
    productos = Producto.objects.select_related("categoria").all()
    return render(request, "productos/listar.html", {"productos": productos})


@login_required
def crear_producto(request):
    form = ProductoForm(request.POST or None)
    if form.is_valid():
        form.cleaned_data["nombre"] = form.cleaned_data["nombre"].strip().capitalize()
        form.save()
        messages.success(request, "Producto creado")
        return redirect("ventas:listar_productos")
    return render(request, "productos/crear.html", {"form": form})


@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    form = ProductoForm(request.POST or None, instance=producto)
    if form.is_valid():
        form.cleaned_data["nombre"] = form.cleaned_data["nombre"].strip().capitalize()
        form.save()
        messages.success(request, "Producto actualizado")
        return redirect("ventas:listar_productos")
    return render(request, "productos/editar.html", {"form": form, "producto": producto})


@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        producto.delete()
        messages.success(request, "Producto eliminado")
        return redirect("ventas:listar_productos")
    return render(request, "productos/eliminar.html", {"producto": producto})


@login_required
def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, "clientes/listar.html", {"clientes": clientes})


@login_required
def crear_cliente(request):
    form = ClienteForm(request.POST or None)
    if form.is_valid():
        form.cleaned_data["nombres"] = form.cleaned_data["nombres"].strip().capitalize()
        form.cleaned_data["apellidos"] = form.cleaned_data["apellidos"].strip().capitalize()
        form.cleaned_data["direccion"] = form.cleaned_data["direccion"].strip().capitalize()
        form.save()
        messages.success(request, "Cliente creado")
        return redirect("ventas:listar_clientes")
    return render(request, "clientes/crear.html", {"form": form})


@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    form = ClienteForm(request.POST or None, instance=cliente)
    if form.is_valid():
        form.cleaned_data["nombres"] = form.cleaned_data["nombres"].strip().capitalize()
        form.cleaned_data["apellidos"] = form.cleaned_data["apellidos"].strip().capitalize()
        form.cleaned_data["direccion"] = form.cleaned_data["direccion"].strip().capitalize()
        form.save()
        messages.success(request, "Cliente actualizado")
        return redirect("ventas:listar_clientes")
    return render(request, "clientes/editar.html", {"form": form, "cliente": cliente})


@login_required
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        cliente.delete()
        messages.success(request, "Cliente eliminado")
        return redirect("ventas:listar_clientes")
    return render(request, "clientes/eliminar.html", {"cliente": cliente})


@login_required
def listar_pedidos(request):
    pedidos = Pedido.objects.select_related("cliente").all()
    return render(request, "pedidos/listar.html", {"pedidos": pedidos})


@login_required
def crear_pedido(request):
    form = PedidoForm(request.POST or None)
    if form.is_valid():
        pedido = form.save(commit=False)
        pedido.total = 0
        pedido.save()
        messages.success(request, "Pedido creado")
        return redirect("ventas:editar_pedido", pk=pedido.pk)
    return render(request, "pedidos/crear.html", {"form": form})


@login_required
def editar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    form = PedidoForm(request.POST or None, instance=pedido)
    detalle_form = DetallePedidoForm(request.POST or None)
    detalles = DetallePedido.objects.filter(pedido=pedido).select_related("producto")

    if request.method == "POST":

        if "save_pedido" in request.POST:
            if detalles.count() == 0:
                messages.error(request, "No puede guardar el pedido sin agregar al menos un detalle.")
            else:
                if form.is_valid():
                    form.save()
                    messages.success(request, "Pedido guardado correctamente.")
                    return redirect("ventas:listar_pedidos")
                else:
                    messages.error(request, "Hay errores en el formulario del pedido.")

        if "add_detalle" in request.POST:
            if detalle_form.is_valid():
                detalle = detalle_form.save(commit=False)
                detalle.pedido = pedido

                producto = detalle.producto
                cantidad = detalle.cantidad

                if producto.stock < cantidad:
                    messages.error(request, f"Stock insuficiente. Disponible: {producto.stock}")
                    return redirect("ventas:editar_pedido", pk=pedido.pk)

                producto.stock -= cantidad
                producto.save()

                detalle.save()

                pedido.total = sum(d.subtotal for d in DetallePedido.objects.filter(pedido=pedido))
                pedido.save()

                messages.success(request, "Detalle agregado correctamente y stock actualizado.")
                return redirect("ventas:editar_pedido", pk=pedido.pk)
            else:
                messages.error(request, "Complete correctamente los datos del detalle.")

    return render(request, "pedidos/editar.html", {
        "form": form,
        "pedido": pedido,
        "detalle_form": detalle_form,
        "detalles": detalles
    })



@login_required
def eliminar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == "POST":
        pedido.delete()
        messages.success(request, "Pedido eliminado")
        return redirect("ventas:listar_pedidos")
    return render(request, "pedidos/eliminar.html", {"pedido": pedido})



@login_required
def agregar_detalle(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    form = DetallePedidoForm(request.POST or None)

    if request.method == "POST":
        producto = request.POST.get("producto")
        cantidad = request.POST.get("cantidad")

        if not producto or producto == "":
            messages.error(request, "Debe seleccionar un producto.")
        elif not cantidad or int(cantidad) <= 0:
            messages.error(request, "La cantidad debe ser mayor a 0.")
        else:
            if form.is_valid():
                detalle = form.save(commit=False)
                detalle.pedido = pedido
                detalle.save()

                pedido.total = sum(d.subtotal for d in DetallePedido.objects.filter(pedido=pedido))
                pedido.save()

                messages.success(request, "Detalle agregado correctamente.")
                return redirect("ventas:editar_pedido", pk=pedido.pk)

    return render(request, "detalles/agregar.html", {"form": form, "pedido": pedido})


@login_required
def editar_detalle(request, pk):
    detalle = get_object_or_404(DetallePedido, pk=pk)
    form = DetallePedidoForm(request.POST or None, instance=detalle)

    if form.is_valid():
        detalle = form.save(commit=False)
        detalle.save()

        pedido = detalle.pedido
        pedido.total = sum(d.subtotal for d in DetallePedido.objects.filter(pedido=pedido))
        pedido.save()

        messages.success(request, "Detalle actualizado")
        return redirect("ventas:editar_pedido", pk=pedido.pk)

    return render(request, "detalles/editar.html", {"form": form, "detalle": detalle})


@login_required
def eliminar_detalle(request, pk):
    detalle = get_object_or_404(DetallePedido, pk=pk)
    pedido = detalle.pedido
    if request.method == "POST":
        detalle.delete()
        pedido.total = sum(d.subtotal for d in DetallePedido.objects.filter(pedido=pedido))
        pedido.save()
        messages.success(request, "Detalle eliminado")
        return redirect("ventas:editar_pedido", pk=pedido.pk)
    return render(request, "detalles/eliminar.html", {"detalle": detalle})
