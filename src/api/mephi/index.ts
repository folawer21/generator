import { ApiCommon } from "../Common";
import { TResponse } from "../Common/types";
import { TQuestion, TCharacteristics, TGeneratedTests } from "./types";

export class MephiApiClass extends ApiCommon {
  public getQuestions = <T = TQuestion[]>(): TResponse<T> =>
    this.get<T>("http://127.0.0.1:8000/api/v1/get-questions");

  public getCharacteristics = <T = TCharacteristics[]>(): TResponse<T> =>
    this.get<T>("http://127.0.0.1:8000/api/v1/get-characteristics");

  public getGeneratedTests = <T = TGeneratedTests[]>(): TResponse<T> =>
    this.get<T>("http://127.0.0.1:8000/api/v1/get-generatedTests");

  public generateTest = <T = TQuestion[]>(
    data: { characteristics: string[] }
  ): TResponse<T> =>
    this.post<T, { characteristics: string[] }>( 
      "http://127.0.0.1:8000/api/v1/get-generateTests", 
      data
    );

  public deleteCombinedTest = <T = { status: string; message: string }>(
    id: number
  ): TResponse<T> =>
    this.post<T, { id: number }>("http://127.0.0.1:8000/api/v1/delete-combinedTest", {
      id,
    });

    public getCombinedTestQuestions = <T = TQuestion[]>(
      id: number
    ): TResponse<T> =>
      this.post<T, { id: number }>("http://127.0.0.1:8000/api/v1/get-combined-test", {
        id,
      });
}

export const MephiApi = new MephiApiClass();
