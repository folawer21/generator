import {
  Button,
  Card,
  message,
  Result,
  Row,
  Spin,
  List,
  Checkbox,
  Skeleton
} from "antd";
import { useEffect, useState } from "react";
import { MephiApi } from "src/api/mephi";
import { TQuestion } from "src/api/mephi/types";

export const QuestionPage = (): JSX.Element => {
  const [isLoading, setIsLoading] = useState(true);
  const [questions, setQuestions] = useState<TQuestion[]>([]);

  useEffect(() => {
    MephiApi.getQuestions()
      .then((res) => setQuestions(res.data))
      .catch(() => {
        message.error("Ошибка при загрузке");
      })
      .finally(() => setIsLoading(false));
  }, []);

  const renderContent = (): JSX.Element => {
    if (isLoading) {
      return (
        <div style={{ padding: '20px' }}>
          <Skeleton
            active
            paragraph={{ rows: 4 }}
            style={{ maxWidth: 600 }}
          />
          <div
            style={{
              marginTop: '20px',
              display: 'flex',
              justifyContent: 'center'
            }}
          >
            <Spin size="large" style={{ fontSize: '2em' }} />
          </div>
        </div>
      );
    }

    if (questions && questions.length > 0) {
      return (
        <>
          <Card
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 25,
              height: 50,
              marginBottom: 15
            }}>
            Вопросы
          </Card>
          {questions.map((item) => (
            <div key={item.id}>
              <Card
                style={{
                  height: 50,
                  display: "flex",
                  alignItems: "center",
                  fontWeight: 800
                }}>
                {item.id}. {item.text}
              </Card>
              <List
                itemLayout="horizontal"
                dataSource={item.answers}
                renderItem={(el) => (
                  <List.Item>
                    <List.Item.Meta
                      description={
                        <div
                          style={{
                            display: "flex",
                            gap: "15px",
                            fontWeight: 400,
                            color: "black"
                          }}>
                          <Checkbox></Checkbox>
                          <p>{el.text}</p>
                        </div>
                      }
                      style={{ marginLeft: 20 }}
                    />
                  </List.Item>
                )}
              />
            </div>
          ))}
        </>
      );
    } else {
      return (
        <Result
          title="Ошибка"
          subTitle="Что-то пошло не так"
          extra={<Button type="primary">Вернуться домой</Button>}
        />
      );
    }
  };

  return renderContent();
};