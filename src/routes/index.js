import express from "express";
import {getUsers, Register, Login, Logout} from "../controller/Users.js";
import {getLog, createLog} from "../controller/Log.js";
import {getResult} from "../controller/Result.js";
import {verifyToken} from "../middleware/verifyToken.js";
import {refreshToken} from "../controller/refreshToken.js";

const router = express.Router();

router.get('/users',verifyToken, getUsers);
router.post('/users', Register);
router.post('/login', Login);
router.delete('/logout', Logout);
router.get('/token', refreshToken);
router.post('/getlog', getLog);
router.post('/createlog', createLog);
router.post('/result', getResult);


export default router;