import {
  Button,
  Card,
  Result,
  Row,
  Spin,
  List,
  Skeleton,
  Input,
  Select,
  Form,
  message,
  Radio
} from "antd";
import { useEffect, useState } from "react";
import { TQuestion } from "src/api/mephi/types";
import { MephiApi } from "src/api/mephi"; // Импорт API

interface QuestionPageProps {
  questions: TQuestion[] | null;
}

const { Option } = Select;

export const QuestionPage = ({ questions }: QuestionPageProps): JSX.Element => {
  const [isLoading, setIsLoading] = useState(true);
  const [userInfoEntered, setUserInfoEntered] = useState(false);
  const [studentName, setStudentName] = useState<string | null>(null);
  const [studentGroup, setStudentGroup] = useState<string | null>(null);
  const [answers, setAnswers] = useState<Record<number, number | null>>({});
  const [form] = Form.useForm();

  useEffect(() => {
    if (questions === null) {
      setIsLoading(true);
    } else {
      setIsLoading(false);
    }
  }, [questions]);

  const handleStartTest = () => {
    form.validateFields().then(values => {
      setStudentName(values.name);
      setStudentGroup(values.group);
      setUserInfoEntered(true);
    }).catch(() => {
      message.error("Пожалуйста, заполните все поля.");
    });
  };

  const handleFinishTestClick = async () => {
    if (!studentName || !studentGroup) return;

    const formattedAnswers = Object.entries(answers).map(([questionId, answerId]) => ({
      questionId: Number(questionId),
      answerId: answerId as number
    }));

    const answersAsRecord: Record<number, number> = Object.fromEntries(
      Object.entries(answers).map(([questionId, answerId]) => [
        Number(questionId),
        answerId as number
      ])
    );

    try {
      await MephiApi.submitResultsFromTest({
        fullName: studentName,
        group: studentGroup,
        answers: answersAsRecord
      });

      message.success("Результаты успешно отправлены!");
      console.log("Отправлено:", {
        name: studentName,
        group: studentGroup,
        answers: formattedAnswers
      });

      // Здесь можно сбросить состояние, показать финальный экран и т.п.

    } catch (error) {
      console.error("Ошибка при отправке:", error);
      message.error("Ошибка при отправке результатов");
    }
  };

  const renderForm = (): JSX.Element => (
    <Card
      title="Введите данные студента"
      style={{ maxWidth: 600, margin: "40px auto" }}
    >
      <Form form={form} layout="vertical">
        <Form.Item label="ФИО студента" name="name" rules={[{ required: true, message: "Введите ФИО" }]}>
          <Input placeholder="Иванов Иван Иванович" />
        </Form.Item>

        <Form.Item label="Группа" name="group" rules={[{ required: true, message: "Выберите группу" }]}>
          <Select placeholder="Выберите группу">
            <Option value="Б21-524">Б21-524</Option>
            <Option value="Б21-525">Б21-525</Option>
            <Option value="Б21-526">Б21-526</Option>
          </Select>
        </Form.Item>

        <Button type="primary" onClick={handleStartTest}>
          Начать тест
        </Button>
      </Form>
    </Card>
  );

  const renderQuestions = (): JSX.Element => {
    if (isLoading) {
      return (
        <div style={{ padding: '20px' }}>
          <Skeleton active paragraph={{ rows: 4 }} style={{ maxWidth: 600 }} />
          <div style={{ marginTop: '20px', display: 'flex', justifyContent: 'center' }}>
            <Spin size="large" />
          </div>
        </div>
      );
    }

    if (questions && questions.length > 0) {
      return (
        <>
          <Card style={{
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
              <Card style={{
                height: 50,
                display: "flex",
                alignItems: "center",
                backgroundColor: '#1890ff',
                color: 'white',
                fontWeight: 800
              }}>
                {item.id}. {item.text}
              </Card>
              <div style={{ padding: 20 }}>
                <Radio.Group
                  onChange={(e) => {
                    const answerId = e.target.value;
                    setAnswers(prev => ({ ...prev, [item.id]: answerId }));
                  }}
                  value={answers[item.id] || null}
                >
                  {item.answers.map((el) => (
                    <Radio key={el.id} value={el.id} style={{ display: "block", marginBottom: 8 }}>
                      {el.text}
                    </Radio>
                  ))}
                </Radio.Group>
              </div>
            </div>
          ))}
          <Row justify="center" style={{ marginTop: 30 }}>
            <Button
              type="primary"
              onClick={handleFinishTestClick}
              style={{ width: 300, height: 80 }}
            >
              Закончить тест
            </Button>
          </Row>
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

  return userInfoEntered ? renderQuestions() : renderForm();
};
