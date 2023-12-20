import { Sequelize } from "sequelize";
import db from "../config/database.js";

const {DataTypes} = Sequelize;

const Log = db.define('log',{
    lat:{
        type: DataTypes.STRING
    },
    longtitude:{
        type: DataTypes.STRING
    },
    longpanel:{
        type: DataTypes.FLOAT
    },
    pricekwh:{
        type: DataTypes.FLOAT
    },
    result:{
        type: DataTypes.FLOAT
    },
    iduser:{
        type: DataTypes.INTEGER
    }
},{
    freezeTableName: true
})

export default Log;
