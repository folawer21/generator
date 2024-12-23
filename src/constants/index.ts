import { ControlFilled } from "@ant-design/icons";
import { QuestionCircleFilled } from "@ant-design/icons";
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
  }
];
