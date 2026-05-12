function validarCedula(cedula) {
  if (!/^\d{10}$/.test(cedula)) return false;
  var provincia = parseInt(cedula.substring(0,2), 10);
  if (provincia < 1 || provincia > 24) return false;
  var tercer = parseInt(cedula.charAt(2), 10);
  if (tercer >= 6) return false;
  var coef = [2,1,2,1,2,1,2,1,2];
  var total = 0;
  for (var i=0;i<9;i++){
    var val = parseInt(cedula.charAt(i),10) * coef[i];
    if (val >= 10) val -= 9;
    total += val;
  }
  var dig = (total % 10 === 0) ? 0 : 10 - (total % 10);
  return dig === parseInt(cedula.charAt(9),10);
}

document.addEventListener('DOMContentLoaded', function(){
  var form = document.getElementById('registerForm');
  if (!form) return;
  form.addEventListener('submit', function(e){
    var cedula = form.querySelector('input[name="cedula"]').value.trim();
    var correo = form.querySelector('input[name="correo"]').value.trim();
    var pwd = form.querySelector('input[name="password"]').value;
    var confirm = form.querySelector('input[name="confirm_password"]').value;
    var errors = [];

    if (!validarCedula(cedula)) errors.push("Cédula inválida.");
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correo)) errors.push("Correo con formato inválido.");
    if (pwd.length < 8) errors.push("La contraseña debe tener al menos 8 caracteres.");
    if (pwd !== confirm) errors.push("Las contraseñas no coinciden.");

    if (errors.length > 0) {
      e.preventDefault();
      alert(errors.join("\n"));
    }
  });
});

