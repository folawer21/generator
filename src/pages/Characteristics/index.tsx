import {
  Button,
  Card,
  Checkbox,
  Popconfirm,
  Result,
  Row,
  Skeleton,
  Table,
  message
} from "antd";
import { useEffect, useState } from "react";
import { MephiApi } from "src/api/mephi";
import { TCharacteristics } from "src/api/mephi/types";
import { useNavigate } from "react-router-dom";
import { clientRoutes } from "src/routes/client";


export const CharacteristicsPage = (): JSX.Element => {
  const [isLoading, setIsLoading] = useState(true);

  const [characteristics, setCharacteristics] = useState<TCharacteristics[]>(
    []
  );
  const navigate = useNavigate();

  useEffect(() => {
    MephiApi.getCharacteristics()
      .then((res) => setCharacteristics(res.data))
      .catch(() => {
        message.error("Ошибка при загрузке");
      })
      .finally(() => setIsLoading(false));
  }, []);

  const handleCheckboxChange = (id: number, checked: boolean) => {
    setCharacteristics((prevCharacteristics) =>
      prevCharacteristics.map((characteristic) =>
        characteristic.id === id
          ? { ...characteristic, usage: checked }
          : characteristic
      )
    );
  };

  const handleButtonClick = () => {
    console.log("Запрос отправлен!"); // Имитация запроса на сервер
    navigate(clientRoutes.questions); // Перейти на страницу вопросов
  };

  const columns: any = [
    {
      title: "Номер",
      dataIndex: "id",
      width: "10%"
    },
    {
      title: "Характеристика психологического портрета личности",
      dataIndex: "name",
      width: "70%"
    },
    {
      title: "Использование",
      dataIndex: "usage",
      width: "10%",
      render: (_: any, record: TCharacteristics) => (
        <Checkbox
          checked={record.usage}
          onChange={(e) => handleCheckboxChange(record.id, e.target.checked)}
          style={{ display: "flex", justifyContent: "center" }}
        />
      )
    },
    {
      dataIndex: "edit",
      width: "10%",
      render: () => (
        <div style={{ display: "flex", justifyContent: "center" }}>
          <a>Редактировать</a>
        </div>
      )
    },
    {
      dataIndex: "delete",
      width: "10%",
      render: () => (
        <div style={{ display: "flex", justifyContent: "center" }}>
          <Popconfirm title="Уверены?">
            <a>Удалить</a>
          </Popconfirm>
        </div>
      )
    }
  ];

  const renderContent = (): JSX.Element => {
    if (isLoading) {
      return (
        <Row justify="center">
          <Skeleton />
        </Row>
      );
    }
    if (characteristics) {
      return (
        <>
          <Card
            style={{
              marginBottom: 10,
              height: "80px",
              alignItems: "center",
              fontSize: 25,
              display: "flex",
              justifyContent: "center"
            }}>
            Список психологических черт
          </Card>
          <Table
            bordered
            pagination={{ defaultPageSize: 8 }}
            columns={columns}
            dataSource={characteristics}
          />
          <Row justify="center" style={{ marginTop: 20 }}>
          <Button 
            type="primary"
            onClick={handleButtonClick}
            style={{width: 300, height: 80}}
            >
              Сгенерировать тест
          </Button>
          </Row>
        </>
      );
    } else {
      return (
        <Result
          title="Ошибка"
          subTitle="Что-то пошло не так"
          // TODO добавить кнопку назад
          extra={<Button type="primary">Вернуться домой</Button>}
        />
      );
    }
  };

  return renderContent();
};