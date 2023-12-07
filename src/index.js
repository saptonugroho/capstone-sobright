import express from "express";
import cookieParser from "cookie-parser";
import cors from "cors";
import router from "./routes/index.js";
import db from "./config/database.js";
//import Users from "./models/User.js";
import dotenv from "dotenv";
dotenv.config();

const app = express();

try {
    await db.authenticate();
    console.log('db ok');
    //await Users.sync();
} catch (error) {
    console.error(error);
}

app.use(cors({credentials:true, origin:'http://localhost:3000'}))
app.use(cookieParser());
app.use(express.json());
app.use(router);
app.listen(5000, ()=> console.log('Berjalan di port 5000'));