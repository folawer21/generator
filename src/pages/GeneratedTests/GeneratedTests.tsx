// import {
//     Button,
//     Card,
//     Popconfirm,
//     Result,
//     Row,
//     Skeleton,
//     Table,
//     message
//   } from "antd";
//   import { useEffect, useState } from "react";
//   import { MephiApi } from "src/api/mephi";
//   import { TGeneratedTests } from "src/api/mephi/types";
//   import { useNavigate } from "react-router-dom";
//   import { clientRoutes } from "src/routes/client";
  
//   export const GeneratedTestsPage = (): JSX.Element => {
//     const [isLoading, setIsLoading] = useState(true);
//     const [generatedTests, setGeneratedTests] = useState<TGeneratedTests[]>([]);
//     const navigate = useNavigate();
  
//     useEffect(() => {
//         MephiApi.getGeneratedTests()
//           .then((res) => {
//             console.log('Loaded data:', res.data);
//             setGeneratedTests(res.data);
//           })
//           .catch((error) => {
//             console.error('Error fetching data:', error);
//             message.error("Ошибка при загрузке");
//           })
//           .finally(() => setIsLoading(false));
//       }, []
//     );
    
//     const handleStartTestClick = (id: number) => {
//       console.log("Начать тест для: ${id}");
//       navigate(clientRoutes.questions);
//     };
  
//     const handleButtonClick = () => {
//       console.log("Запрос отправлен!");
//       navigate(clientRoutes.questions);
//     };
  
//     const columns: any = [
//       {
//         title: "Номер",
//         dataIndex: "id",
//         width: "5%"
//       },
//       {
//         title: "Название",
//         dataIndex: "testName",
//         width: "15%"
//       },
//       {
//         title: "Выявляемые характеристики психологического портрета личности",
//         dataIndex: "charachteristicsList",
//         width: "45%"
//       },
//       {
//         title: "Количество вопросов",
//         dataIndex: "questionCount",
//         width: "10%"
//       },
//       {
//         title: "Начать тест",
//         dataIndex: "action",
//         width: "10%",
//         render: (_: any, record: TGeneratedTests) => (
//           <div style={{ display: "flex", justifyContent: "center" }}>
//             <Button type="primary" onClick={() => handleStartTestClick(record.id)}>
//               Начать тест
//             </Button>
//           </div>
//         )
//       },
//       {
//         title: "Удаление",
//         dataIndex: "delete",
//         width: "10%",
//         render: () => (
//           <div style={{ display: "flex", justifyContent: "center" }}>
//             <Popconfirm title="Уверены?">
//               <a>Удалить</a>
//             </Popconfirm>
//           </div>
//         )
//       }
//     ];
  
//     const renderContent = (): JSX.Element => {
//       if (isLoading) {
//         return (
//           <Row justify="center">
//             <Skeleton />
//           </Row>
//         );
//       }
//       if (generatedTests) {
//         return (
//           <>
//             <Card
//               style={{
//                 marginBottom: 10,
//                 height: "80px",
//                 alignItems: "center",
//                 fontSize: 25,
//                 display: "flex",
//                 justifyContent: "center"
//               }}
//             >
//               Сгенерированные психологические тесты
//             </Card>
//             <Table
//               bordered
//               pagination={{ defaultPageSize: 8 }}
//               columns={columns}
//               dataSource={generatedTests}
//               rowKey="id"
//             />
//           </>
//         );
//       } else {
//         return (
//           <Result
//             title="Ошибка"
//             subTitle="Что-то пошло не так"
//             extra={<Button type="primary">Вернуться домой</Button>}
//           />
//         );
//       }
//     };
  
//     return renderContent();
//   };
  
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
import { useNavigate } from "react-router-dom";
import { clientRoutes } from "src/routes/client";

export const GeneratedTestsPage = (): JSX.Element => {
  const [isLoading, setIsLoading] = useState(true);
  const [generatedTests, setGeneratedTests] = useState<TGeneratedTests[]>([]);
  const navigate = useNavigate();

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
      console.log(`Начать тест для: ${id}`);
      navigate(clientRoutes.questions);
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
  };

  return renderContent();
};
