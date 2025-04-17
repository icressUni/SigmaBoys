import { MongoClient } from "npm:mongodb@5.6.0";
const { MongoClient, ServerApiVersion } = require('mongodb');
const uri = "mongodb+srv://icressall:<OBeuoRvcUN2leEcd>@cluster0.hpg0l23.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0";
// Create a MongoClient with a MongoClientOptions object to set the Stable API version
const client = new MongoClient(uri, {
  serverApi: {
    version: ServerApiVersion.v1,
    strict: true,
    deprecationErrors: true,
  }
});
async function run() {
  try {
    // Connect the client to the server	(optional starting in v4.7)
    await client.connect();
    // Send a ping to confirm a successful connection
    await client.db("admin").command({ ping: 1 });
    console.log("Pinged your deployment. You successfully connected to MongoDB!");
  } finally {
    // Ensures that the client will close when you finish/error
    await client.close();
  }
}
run().catch(console.dir);


import "../diseños/Camera.css"; // Reutilizamos el mismo CSS para estilos consistentes

function demoMongo() {
  return (
    <div className="container">
      <h1>Bienvenido</h1>
      <div className="button-group">
        <button className="login-button" onClick={() => alert("Sección Admin no implementada aún")}>
          Admin
        </button>
        <button className="login-button" onClick={() => alert("prueba")}>
          Lab Tracker
        </button>
      </div>
    </div>
  );
}

export default demoMongo;
