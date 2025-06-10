import { Client } from "jsr:@deno/postgres@0.220.1";
​
const client = new Client({
  user: "postgres",
  database: "labtracker_db",
  hostname: "localhost",
  password: "gjyzf27044",
  port: 5432,
});
​
await client.connect();
​
export default client;