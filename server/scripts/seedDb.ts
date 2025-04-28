import { AlumnoModel } from "../models/alumnoModel.ts";
import { initializeDb } from "../config/db.ts";

async function seedDatabase() {
  console.log("Initializing database...");
  await initializeDb();
  
  console.log("Creating admin user...");
  try {
    const adminExists = await AlumnoModel.findByRut("admin-rut");
    
    if (!adminExists) {
      await AlumnoModel.create({
        nombres: "Admin",
        apellidos: "System",
        rut: "admin-rut",
        password: "adminpassword",
        admin: true
      });
      console.log("Admin user created successfully");
    } else {
      console.log("Admin user already exists");
    }
  } catch (error) {
    console.error("Error creating admin user:", error);
  }
  
  console.log("Database seeding complete");
}

await seedDatabase();
