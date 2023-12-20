import { Sequelize } from "sequelize";
import db from "../config/database.js";

const {DataTypes} = Sequelize;

const Result = db.define('result',{
    lat:{
        type: DataTypes.STRING
    },
    longtitude:{
        type: DataTypes.STRING
    },
    result:{
        type: DataTypes.FLOAT
    },
    date_at:{
        type: DataTypes.DATE
    }
},{
    freezeTableName: true
})

export default Result;
