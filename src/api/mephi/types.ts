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

export type TGroupsList = {
  [groupName: string]: {
    id: number;
    full_name: string;
  }[];
};

export type TPortrait = {
  studentId: number;
  fullName: string;
  group: string;
  temperament: string;
  representationSystem: string;
  psychologicalTraits: string[];
  recommendedApproaches: string[];
};

export type TSubmitResultsPayload = {
  student_id: string;
  test_name: string;
  results: Record<string, number>;
};