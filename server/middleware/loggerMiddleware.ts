import { Context } from "@oak/oak";

export async function logger(ctx: Context, next: () => Promise<unknown>) {
  const start = Date.now();
  await next();
  const ms = Date.now() - start;
  ctx.response.headers.set("X-Response-Time", `${ms}ms`);
  
  console.log(
    `${new Date().toISOString()} | ${ctx.request.method} ${ctx.request.url} - ${ctx.response.status} (${ms}ms)`
  );
}
