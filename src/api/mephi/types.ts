export type TQuestion = {
  id: number;
  text: string;
  answers: answer[];
};

export type answer = {
  id: number;
  text: string;
};

export type TCharacteristics = {
  id: number;
  name: string;
  usage: boolean;
};

export type TGeneratedTests = {
  id: number,
  testName: string,
  charachteristicsList: string,
  questionCount: number
}
