import { TableOutlined } from "@ant-design/icons";
import { ControlFilled } from "@ant-design/icons";
import { createElement } from "react";
import { clientRoutes } from "src/routes/client";

export const MENU_ITEMS = [
  {
    key: clientRoutes.characteristics,
    icon: createElement(ControlFilled),
    label: "Генерация психологического теста"
  },
  {
    key: clientRoutes.questions,
    icon: createElement(TableOutlined),
    label: "Вопросы"
  }
];
