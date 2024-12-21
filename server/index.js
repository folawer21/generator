import jsonServer from "json-server";
import getQuestionsJSON from "./mocks/getQuestions.js";
import getCharacteristicsJSON from "./mocks/getCharacteristics.js";

const addDelay = (delay = 0) =>
  new Promise((resolve) => setTimeout(resolve, delay));

const server = jsonServer.create();
const middlewares = jsonServer.defaults();

server.use(jsonServer.bodyParser);
server.use(middlewares);

server.get("/api/v1/get-questions", async (req, res) => {
  await addDelay(300);
  await res.send(getQuestionsJSON);
});

server.get("/api/v1/get-characteristics", async (req, res) => {
  await addDelay(300);
  await res.send(getCharacteristicsJSON);
});

server.listen(3004, () => {
  console.log(`JSON Server is running: http://localhost:3004`);
});
