import { makeAutoObservable } from "mobx";

export class MephiStore {
  constructor() {
    makeAutoObservable(this);
  }
}
