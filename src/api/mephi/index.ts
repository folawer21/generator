import { ApiCommon } from "../Common";
import { TResponse } from "../Common/types";
import { TQuestion, TCharacteristics } from "./types";

export class MephiApiClass extends ApiCommon {
  public getQuestions = <T = TQuestion[]>(): TResponse<T> =>
    this.get<T>("/api/v1/get-questions");

  public getCharacteristics = <T = TCharacteristics[]>(): TResponse<T> =>
    this.get<T>("/api/v1/get-characteristics");
}

export const MephiApi = new MephiApiClass();
