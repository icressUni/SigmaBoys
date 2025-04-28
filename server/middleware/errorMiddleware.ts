import { Context, Status, isHttpError } from "@oak/oak";

export async function errorMiddleware(ctx: Context, next: () => Promise<unknown>) {
  try {
    await next();
  } catch (err) {
    if (isHttpError(err)) {
      ctx.response.status = err.status;
      ctx.response.body = {
        success: false,
        error: err.message,
        status: err.status
      };
    } else {
      ctx.response.status = Status.InternalServerError;
      ctx.response.body = {
        success: false,
        error: err.message || "Error interno del servidor",
        status: Status.InternalServerError
      };
      console.error("Unhandled error:", err);
    }
  }
}
