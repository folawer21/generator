import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { ConfigProvider } from "antd";
import ru_RU from "antd/lib/locale/ru_RU";
import { createStore, StoreContext } from "./stores";
import { App } from "./App";

const stores = createStore();

ReactDOM.createRoot(document.getElementById("root")!).render(
  <BrowserRouter>
    <ConfigProvider locale={ru_RU}>
      <StoreContext.Provider value={stores}>
        <App />
      </StoreContext.Provider>
    </ConfigProvider>
  </BrowserRouter>
);
