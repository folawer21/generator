import { Routes, Route, useNavigate, useLocation, Navigate } from "react-router-dom";
import { observer } from "mobx-react-lite";
import { Menu } from "antd";

import {
  AppStyled,
  AppWrapper,
  Content,
  Header,
  HeaderContent
} from "./AppStyle";
import { QuestionPage } from "./pages/Questions/Questions";
import { CharacteristicsPage } from "./pages/GenerateTests/GenerateTests";
import { GeneratedTestsPage } from "./pages/GeneratedTests/GeneratedTests";
import { clientRoutes } from "src/routes/client";
import { MENU_ITEMS } from "src/constants";

export const App = observer((): JSX.Element => {
  const location = useLocation();
  const navigate = useNavigate();

  return (
    <AppWrapper>
      <Header>
        <HeaderContent>
          <img src="https://i.yapx.ru/W2oMO.png" alt="Logo" />
          <Menu
            theme="dark"
            mode="horizontal"
            selectedKeys={[location.pathname]}
            items={MENU_ITEMS}
            style={{ flex: 1, minWidth: 0 }}
            onClick={(info) => navigate(info.key)}
          />
        </HeaderContent>
      </Header>
      <AppStyled>
        <Content>
          <Routes>
            <Route path="/" element={<Navigate to="/characteristics" />} />
            <Route path={clientRoutes.characteristics} element={<CharacteristicsPage />} />
            <Route path={clientRoutes.questions} element={<QuestionPage />} />
            <Route path={clientRoutes.generatedTests} element={<GeneratedTestsPage />} />
          </Routes>
        </Content>
      </AppStyled>
    </AppWrapper>
  );
});