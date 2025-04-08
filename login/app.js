document.getElementById("login-form").addEventListener("submit", function(e) {
    e.preventDefault();
    
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    
    // Aquí puedes agregar la lógica para verificar las credenciales (por ejemplo, con un backend)
    if (username === "admin" && password === "1234") {
      alert("Inicio de sesión exitoso");
      // Aquí puedes redirigir al usuario a otra página
    } else {
      alert("Usuario o contraseña incorrectos");
    }
  });
  