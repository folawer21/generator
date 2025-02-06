import React, { useState, useEffect } from "react";
import {
  Button,
  Card,
  Checkbox,
  Popconfirm,
  Result,
  Row,
  Skeleton,
  Table,
  Modal,
  Input,
  Slider,
  message
} from "antd";
import { MephiApi } from "src/api/mephi";
import { TCharacteristics } from "src/api/mephi/types";
import { TQuestion } from "src/api/mephi/types"; 
import { useNavigate } from "react-router-dom";
import { clientRoutes } from "src/routes/client";
import { QuestionPage } from "src/pages/Questions/Questions.tsx";  

export const CharacteristicsPage = (): JSX.Element => {
  const [isLoading, setIsLoading] = useState(true);
  const [characteristics, setCharacteristics] = useState<TCharacteristics[]>([]);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [testName, setTestName] = useState("");
  const [paramA, setParamA] = useState(0);
  const [paramB, setParamB] = useState(0);
  const [selectedCharacteristics, setSelectedCharacteristics] = useState<string[]>([]);
  const [questions, setQuestions] = useState<TQuestion[]>([]);
  const [testGenerated, setTestGenerated] = useState(false); // Флаг для отслеживания успешной генерации теста

  const navigate = useNavigate();

  useEffect(() => {
    // Загружаем характеристики при монтировании компонента
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

    setSelectedCharacteristics((prevSelected) => {
      if (checked) {
        const characteristic = characteristics.find((c) => c.id === id);
        return characteristic ? [...prevSelected, characteristic.name] : prevSelected;
      } else {
        return prevSelected.filter((name) => name !== characteristics.find((c) => c.id === id)?.name);
      }
    });
  };

  const showModal = () => {
    setIsModalVisible(true);
  };

  const handleOk = () => {
    if (selectedCharacteristics.length === 0) {
      message.error("Не выбраны характеристики для генерации теста.");
      return;
    }
  
    if (!testName.trim()) {
      message.error("Введите название теста.");
      return;
    }
  
    // Генерируем тест на основе выбранных характеристик и названия
    MephiApi.generateTest({
      characteristics: selectedCharacteristics,
      test_name: testName, // Теперь передаем название теста
    })
      .then((res) => {
        console.log("Тест сгенерирован!", res);
        setQuestions(res.data);  // Сохраняем полученные вопросы
        setIsModalVisible(false);
        setTestGenerated(true); // Устанавливаем флаг о том, что тест сгенерирован
      })
      .catch(() => {
        message.error("Ошибка при генерации теста.");
      });
  };
  

  const handleCancel = () => {
    setIsModalVisible(false);
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

    if (!testGenerated) {
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
              onClick={showModal}
              style={{ width: 300, height: 80 }}
            >
              Сгенерировать тест
            </Button>
          </Row>
        </>
      );
    } else {
      return (
        <QuestionPage questions={questions} /> // Строим экран с вопросами
      );
    }
  };

  return (
    <>
      {renderContent()}
      <Modal
        title="Параметры генерации"
        visible={isModalVisible}
        onOk={handleOk}
        onCancel={handleCancel}
      >
        <Input
          placeholder="Название теста"
          value={testName}
          onChange={(e) => setTestName(e.target.value)}
          style={{ marginBottom: 20 }}
        />
        <div style={{ marginBottom: 20 }}>
          <label>Штраф за избыточность</label>
          <Slider min={0} max={1} step={0.01} value={paramA} onChange={setParamA} />
        </div>
        <div>
          <label>Штраф за несбалансированность</label>
          <Slider min={0} max={1} step={0.01} value={paramB} onChange={setParamB} />
        </div>
      </Modal>
    </>
  );
};
