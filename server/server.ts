import { serve } from "https://deno.land/std@0.114.0/http/server.ts";
import { db, todos } from "./db.ts";
import { ObjectId } from "https://deno.land/x/mongo@v0.31.1/mod.ts";

const handler = async (req: Request): Promise<Response> => {
  const url = new URL(req.url);
  const id = url.pathname.split("/")[2];
  if (req.method === "GET" && url.pathname === "/todos") {
    try {
      const allTodos = await todos.find({}).toArray();
      return new Response(JSON.stringify(allTodos), { status: 200 });
    } catch (error) {
      return new Response(JSON.stringify({ error: "Failed to fetch todos" }), { status: 500 });
    }
  }
  if (req.method === "PUT" && id) {
    try {
      const updateData = await req.json();
      const result = await todos.updateOne({ _id: new ObjectId(id) }, { $set: updateData });
      if (result.matchedCount > 0) {
        return new Response(JSON.stringify({ message: "Todo updated successfully" }), { status: 200 });
      } else {
        return new Response(JSON.stringify({ message: "Todo not found" }), { status: 404 });
      }
    } catch (error) {
      return new Response(JSON.stringify({ error: "Failed to update todo" }), { status: 500 });
    }
  }
  return new Response("Not Found", { status: 404 });
};
console.log("Server running on http://localhost:8000");
serve(handler, { port: 8000 });