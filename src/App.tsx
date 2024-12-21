import { Routes, Route, useNavigate, useLocation } from "react-router-dom";
import { observer } from "mobx-react-lite";
import { Menu } from "antd";
import {
  AppStyled,
  AppWrapper,
  Content,
  Header,
  HeaderContent
} from "./AppStyle";
import { QuestionPage } from "./pages/Questions";
import { CharacteristicsPage } from "./pages/Characteristics";
import { clientRoutes } from "src/routes/client";
import { MENU_ITEMS } from "src/constants";

export const App = observer((): JSX.Element => {
  const location = useLocation();
  const navigate = useNavigate();

  return (
    <AppWrapper>
      <Header>
        <HeaderContent>
          <img src="https://i.yapx.ru/W2oMO.png" />
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
            <Route
              path={clientRoutes.characteristics}
              element={<CharacteristicsPage />}
            />
            <Route path={clientRoutes.questions} element={<QuestionPage />} />
          </Routes>
        </Content>
      </AppStyled>
    </AppWrapper>
  );
});
