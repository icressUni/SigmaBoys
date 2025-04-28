import { Application, Context } from "https://deno.land/x/oak/mod.ts";
import { multipart } from "https://deno.land/x/oak/multipart.ts";
import { join } from "https://deno.land/std/path/mod.ts";
import { serve } from "https://deno.land/std/http/server.ts";

// Usa alguna librería de procesamiento de imágenes o realiza el reconocimiento facial en un servidor aparte
// Aquí va el código para configurar el servidor con Oak, el cual maneja el API en Deno

const app = new Application();

app.use(multipart());  // Para manejar la carga de archivos (imágenes)

app.use(async (ctx: Context) => {
  if (ctx.request.hasBody) {
    const body = ctx.request.body({ type: "form-data" });
    const data = await body.value.read();  // Aquí obtienes el archivo cargado
    const file = data.files[0];  // Suponiendo que el nombre del campo sea 'imagen'

    // Aquí puedes integrar con tu lógica de reconocimiento facial (en un servidor externo, si es necesario)
    // O utilizar alguna librería compatible con Deno
    const imagePath = join(Deno.cwd(), "uploads", file.filename);
    await Deno.writeFile(imagePath, file.content);

    // Puedes hacer el reconocimiento aquí y devolver el resultado
    // Ejemplo de respuesta simulada:
    ctx.response.body = { message: "Imagen recibida", image: file.filename };
  } else {
    ctx.response.status = 400;
    ctx.response.body = { message: "No image file uploaded" };
  }
});

app.listen({ port: 8000 });  // El backend escuchará en el puerto 8000

console.log("Servidor corriendo en http://localhost:8000");
