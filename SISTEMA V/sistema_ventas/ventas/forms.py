from django import forms
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from .models import Categoria, Producto, Cliente, Pedido, DetallePedido
import datetime
import re


def validar_cedula_ecuador(cedula):
    if not isinstance(cedula, str):
        return False
    ced = cedula.strip()
    if not ced.isdigit() or len(ced) != 10:
        return False
    provincia = int(ced[:2])
    if provincia < 1 or provincia > 24:
        return False
    tercer = int(ced[2])
    if tercer >= 6:
        return False
    coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    total = 0
    for i in range(9):
        valor = int(ced[i]) * coeficientes[i]
        if valor >= 10:
            valor -= 9
        total += valor
    digito_verificador = 10 - (total % 10) if (total % 10) != 0 else 0
    return digito_verificador == int(ced[9])


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nombre",]

    def clean_nombre(self):
        nombre = (self.cleaned_data.get("nombre") or "").strip()
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', nombre):
            raise forms.ValidationError("El nombre solo debe contener letras y espacios.")
        return nombre


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["categoria", "nombre", "precio", "stock"]

    def validar_categoria(self):
        categoria = self.cleaned_data.get("categoria")
        if categoria is None:
            raise forms.ValidationError("Debe seleccionar una categoría válida.")
        return categoria


    def clean_nombre(self):
        nombre = (self.cleaned_data.get("nombre") or "").strip()
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', nombre):
            raise forms.ValidationError("El nombre solo debe contener letras y espacios.")
        return nombre

    def validar_precio(self):
        precio = self.cleaned_data.get("precio")
        if precio is None:
            raise forms.ValidationError("El precio es obligatorio.")
        try:
            if float(precio) <= 0:
                raise forms.ValidationError("El precio debe ser un número positivo mayor que cero.")
        except (TypeError, ValueError):
            raise forms.ValidationError("El precio debe ser un número válido.")
        return precio

    def validar_stock(self):
        stock = self.cleaned_data.get("stock")
        if stock is None:
            raise forms.ValidationError("El stock es obligatorio.")
        try:
            if int(stock) < 0:
                raise forms.ValidationError("El stock no puede ser negativo.")
        except (TypeError, ValueError):
            raise forms.ValidationError("El stock debe ser un número entero válido.")
        return stock


class ClienteForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = Cliente

        fields = [
            "cedula",
            "nombres",
            "apellidos",
            "correo",
            "telefono",
            "fecha_nacimiento",
            "direccion",
        ]

    def clean_cedula(self):
        cedula = (self.cleaned_data.get("cedula") or "").strip()
        if not cedula:
            raise forms.ValidationError("La cédula es obligatoria y no puede estar vacía.")
        if not validar_cedula_ecuador(cedula):
            raise forms.ValidationError("La cédula ecuatoriana no es válida.")
        qs = Cliente.objects.filter(cedula=cedula)
        if self.instance and getattr(self.instance, "pk", None):
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Esta cédula ya está registrada en el sistema.")
        return cedula

    def validar_nombres(self):
        nombres = (self.cleaned_data.get("nombres") or "").strip()
        if not nombres:
            raise forms.ValidationError("El campo nombres es obligatorio y no puede estar vacío.")
        return nombres

    def validar_apellidos(self):
        apellidos = (self.cleaned_data.get("apellidos") or "").strip()
        if not apellidos:
            raise forms.ValidationError("El campo apellidos es obligatorio y no puede estar vacío.")
        return apellidos

    def clean_correo(self):
        correo = (self.cleaned_data.get("correo") or "").strip()
        if not correo:
            raise forms.ValidationError("El correo es obligatorio y no puede estar vacío.")
        qs_cliente = Cliente.objects.filter(correo=correo)
        if self.instance and getattr(self.instance, "pk", None):
            qs_cliente = qs_cliente.exclude(pk=self.instance.pk)
        if qs_cliente.exists():
            raise forms.ValidationError("Este correo ya está registrado para otro cliente.")
        if User.objects.filter(email=correo).exists():
            if not (self.instance and getattr(self.instance, "correo", None) == correo):
                raise forms.ValidationError("Este correo ya está registrado como usuario del sistema.")
        return correo

    def clean_telefono(self):
        telefono = (self.cleaned_data.get("telefono") or "").strip()

        if not telefono:
            raise forms.ValidationError("El teléfono es obligatorio y no puede estar vacío.")

        if not telefono.isdigit():
            raise forms.ValidationError("El teléfono solo debe contener números.")

        if len(telefono) < 10:
            raise forms.ValidationError("El teléfono debe tener 10 dígitos.")

        if not telefono.startswith("09"):
            raise forms.ValidationError("El teléfono debe empezar con 09.")

        return telefono

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get("fecha_nacimiento")
        if not fecha_nacimiento:
            raise forms.ValidationError("La fecha es obligatoria y no puede estar vacía.")
        if not isinstance(fecha_nacimiento, datetime.date):
            raise forms.ValidationError("La fecha de nacimiento debe ser una fecha válida.")
        if fecha_nacimiento >= datetime.date.today():
            raise forms.ValidationError("La fecha de nacimiento no puede ser hoy o futura.")
        return fecha_nacimiento

    def clean_direccion(self):
        direccion = (self.cleaned_data.get("direccion") or "").strip()
        if not direccion:
            raise forms.ValidationError("La fecha es obligatoria y no puede estar vacía.")
        return direccion


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ["cliente"]

    def validar_cliente(self):
        cliente = self.cleaned_data.get("cliente")
        if cliente is None:
            raise forms.ValidationError("Debe seleccionar un cliente válido.")
        return cliente


class DetallePedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = ["producto", "cantidad"]

    def validar_producto(self):
        producto = self.cleaned_data.get("producto")
        if producto is None:
            raise forms.ValidationError("Debe seleccionar un producto válido.")
        return producto

    def validar_cantidad(self):
        cantidad = self.cleaned_data.get("cantidad")
        if cantidad is None:
            raise forms.ValidationError("La cantidad es obligatoria.")
        try:
            if int(cantidad) <= 0:
                raise forms.ValidationError("La cantidad debe ser un número entero mayor que cero.")
        except (TypeError, ValueError):
            raise forms.ValidationError("La cantidad debe ser un número entero válido.")
        return cantidad


class RegisterForm(forms.Form):
    cedula = forms.CharField(max_length=10, required=True)
    nombres = forms.CharField(max_length=100, required=True)
    apellidos = forms.CharField(max_length=100, required=True)
    correo = forms.EmailField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
    telefono = forms.CharField(max_length=15, required=True)
    fecha_nacimiento = forms.DateField(required=True, widget=forms.DateInput(attrs={"type": "date"}))
    direccion = forms.CharField(max_length=250, required=True)

    def clean_correo(self):
        correo = (self.cleaned_data.get("correo") or "").strip()
        if len(correo) == 0:
            raise forms.ValidationError("El correo es obligatorio.")
        if User.objects.filter(username__iexact=correo).exists() or User.objects.filter(email__iexact=correo).exists():
            raise forms.ValidationError("Este correo ya está registrado como usuario del sistema.")
        return correo

    def clean_password(self):
        password = self.cleaned_data.get("password") or ""
        if len(password) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        return password

    def clean_telefono(self):
        telefono = (self.cleaned_data.get("telefono") or "").strip()
        if not telefono:
            raise forms.ValidationError("El telefono es obligatorio.")
        if not telefono.isdigit():
            raise forms.ValidationError("El teléfono solo debe contener números.")
        if len(telefono) < 7 or len(telefono) > 15:
            raise forms.ValidationError("El teléfono debe tener entre 7 y 15 dígitos.")
        return telefono

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get("fecha_nacimiento")
        if fecha is None:
            raise forms.ValidationError("la fecha no pudede esta vacia")
        if fecha >= datetime.date.today():
            raise forms.ValidationError("La fecha de nacimiento no puede ser hoy o futura.")
        return fecha

    def clean_direccion(self):
        direccion = (self.cleaned_data.get("direccion") or "").strip()
        if direccion == "":
            raise forms.ValidationError("La dirección es obligatoria.")
        return direccion

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get("password")
        confirm = cleaned.get("confirm_password")
        if password and confirm and password != confirm:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned

    def save(self, commit=True):
        correo = self.cleaned_data.get("correo")
        password = self.cleaned_data.get("password")
        username = correo.lower().strip()

        if User.objects.filter(username=username).exists() or User.objects.filter(email=correo).exists():
            raise forms.ValidationError("Este correo/usuario ya existe.")

        try:
            with transaction.atomic():

                user = User(
                    username=username,
                    email=correo,
                    first_name=self.cleaned_data.get("nombres"),
                    last_name=self.cleaned_data.get("apellidos")
                )
                user.set_password(password)
                if commit:
                    user.save()

                cliente = Cliente(
                    cedula=self.cleaned_data.get("cedula"),
                    nombres=self.cleaned_data.get("nombres"),
                    apellidos=self.cleaned_data.get("apellidos"),
                    correo=correo,
                    telefono=self.cleaned_data.get("telefono"),
                    fecha_nacimiento=self.cleaned_data.get("fecha_nacimiento"),
                    direccion=self.cleaned_data.get("direccion")
                )
                if commit:
                    cliente.save()

                return user, cliente

        except IntegrityError:
            raise forms.ValidationError(
                "No se pudo crear el usuario porque el correo ya existe. Intente con otro correo."
            )
