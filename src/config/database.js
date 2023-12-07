import { Sequelize } from "sequelize";

const db = new Sequelize('sobright','root','',{
    host: "localhost",
    dialect: "mysql"
});

export default db;