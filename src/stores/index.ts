import { createContext, useContext } from "react";
import { MephiStore } from "./mephi";

export const createStore = (): MephiStore => new MephiStore();

export const StoreContext = createContext<MephiStore | null>(null);

export const useStore = (): MephiStore => {
  const stores = useContext(StoreContext);

  if (!stores) {
    throw new Error(
      "useStore() allow use inside <StoreContext.provider /> only"
    );
  }

  return stores;
};
