import {
  Button,
  Card,
  Popconfirm,
  Result,
  Row,
  Skeleton,
  Table,
  message
} from "antd";
import { useEffect, useState } from "react";
import { MephiApi } from "src/api/mephi";
import { TGeneratedTests } from "src/api/mephi/types";
import { TQuestion } from "src/api/mephi/types";
import { useNavigate } from "react-router-dom";
import { clientRoutes } from "src/routes/client";
import { QuestionPage } from "../Questions/Questions";

export const GeneratedTestsPage = (): JSX.Element => {
  const [isLoading, setIsLoading] = useState(true);
  const [generatedTests, setGeneratedTests] = useState<TGeneratedTests[]>([]);
  const [questions, setQuestions] = useState<TQuestion[]>([]);
  const navigate = useNavigate();
  const [testOpened, setTestOpened] = useState(false); // Флаг для отслеживания успешной генерации теста


  useEffect(() => {
      MephiApi.getGeneratedTests()
          .then((res) => {
              console.log("Loaded data:", res.data);
              setGeneratedTests(res.data);
          })
          .catch((error) => {
              console.error("Error fetching data:", error);
              message.error("Ошибка при загрузке");
          })
          .finally(() => setIsLoading(false));
  }, []);

  const handleStartTestClick = (id: number) => {
    console.log(`Загрузка вопросов для теста: ${id}`);
  
    MephiApi.getCombinedTestQuestions(id)
      .then((res) => {
        console.log("Вопросы загружены:", res.data);
        setQuestions(res.data);  // Сохраняем полученные вопросы
        setTestOpened(true);
      })
      .catch((error) => {
        console.error("Ошибка при загрузке вопросов:", error);
        message.error("Ошибка при загрузке вопросов теста");
      });
  };

  // Функция для удаления теста
  const handleDeleteTest = (id: number) => {
      MephiApi.deleteCombinedTest(id)
          .then(() => {
              message.success("Тест успешно удалён");
              setGeneratedTests((prevTests) =>
                  prevTests.filter((test) => test.id !== id)
              );
          })
          .catch((error) => {
              console.error("Ошибка при удалении теста:", error);
              message.error("Ошибка при удалении теста");
          });
  };

  const columns: any = [
      {
          title: "Номер",
          dataIndex: "id",
          width: "5%"
      },
      {
          title: "Название",
          dataIndex: "testName",
          width: "15%"
      },
      {
          title: "Выявляемые характеристики психологического портрета личности",
          dataIndex: "charachteristicsList",
          width: "45%"
      },
      {
          title: "Количество вопросов",
          dataIndex: "questionCount",
          width: "10%"
      },
      {
          title: "Начать тест",
          dataIndex: "action",
          width: "10%",
          render: (_: any, record: TGeneratedTests) => (
              <div style={{ display: "flex", justifyContent: "center" }}>
                  <Button type="primary" onClick={() => handleStartTestClick(record.id)}>
                      Начать тест
                  </Button>
              </div>
          )
      },
      {
          title: "Удаление",
          dataIndex: "delete",
          width: "10%",
          render: (_: any, record: TGeneratedTests) => (
              <div style={{ display: "flex", justifyContent: "center" }}>
                  <Popconfirm
                      title="Вы уверены, что хотите удалить тест?"
                      onConfirm={() => handleDeleteTest(record.id)}
                      okText="Да"
                      cancelText="Нет"
                  >
                      <a style={{ color: "red" }}>Удалить</a>
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
      if (!testOpened) {
        if (generatedTests.length > 0) {
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
                      }}
                  >
                      Сгенерированные психологические тесты
                  </Card>
                  <Table
                      bordered
                      pagination={{ defaultPageSize: 8 }}
                      columns={columns}
                      dataSource={generatedTests}
                      rowKey="id"
                  />
              </>
          );
      } else {
          return (
              <Result
                  title="Нет сгенерированных тестов"
                  subTitle="Создайте тест перед удалением"
                  extra={<Button type="primary" onClick={() => navigate(clientRoutes.characteristics)}>Вернуться домой</Button>}
              />
          );
      }
      } else {
        return (
          <QuestionPage questions={questions} />
        )
      }
      
  };

  return renderContent();
};
