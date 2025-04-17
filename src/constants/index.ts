import { ControlFilled } from "@ant-design/icons";
import { QuestionCircleFilled, QuestionOutlined, PropertySafetyTwoTone } from "@ant-design/icons";
import Icon from "@ant-design/icons/lib/components/Icon";
import { createElement } from "react";
import { clientRoutes } from "src/routes/client";

export const MENU_ITEMS = [
  {
    key: clientRoutes.characteristics,
    icon: createElement(ControlFilled),
    label: "Генерация психологического теста"
  },
  {
    key: clientRoutes.generatedTests,
    icon: createElement(QuestionCircleFilled),
    label: 'Сгенерированные тесты',
  },
  {
    key: clientRoutes.authorsTests,
    icon: createElement(QuestionOutlined),
    label: 'Авторские тесты',
  },
  {
    key: clientRoutes.portretsList,
    icon: createElement(PropertySafetyTwoTone),
    label: 'Психологические портреты'
  }
];
