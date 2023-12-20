import Result from "../models/Result.js";

export const getResult = async(req, res)=> {
    const {lat, longtitude} = req.body;
    try {
        const result = await Result.findAll({
            where:{
                lat: lat,
                longtitude: longtitude,
            }
        });
        res.json(result);
    } catch (error) {
        console.log(error);
    }
}