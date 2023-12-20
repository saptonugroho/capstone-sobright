import Log from "../models/Log.js";

export const getLog = async(req, res)=> {
    const {iduser} = req.body;
    try {
        const log = await Log.findAll({
            where:{
                iduser: iduser
            }
        });
        res.json(log);
    } catch (error) {
        console.log(error);
    }
}

export const createLog = async(req, res)=>{
    const {lat, long, longpanel, pricekwh, result, iduser} = req.body;
    try {
        await Log.create({
           lat : lat,
           longtitude : long,
           longpanel : longpanel,
           pricekwh : pricekwh,
           result : result,
           iduser : iduser
        })
        res.status(201).json({message: "Save Log success", data: req.body})
    } catch (error) {
        res.status(500).json({
            message: 'Server Error',
            serverMessage: error,
        })
    }

}