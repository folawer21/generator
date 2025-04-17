import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { MephiApi } from "src/api/mephi"; 
import { Avatar, Card, Descriptions, Divider, List, Tag, Typography, Spin, Alert } from "antd";
import { UserOutlined, BookOutlined, BulbOutlined, SmileOutlined } from "@ant-design/icons";
import axios from "axios";

const { Title, Paragraph } = Typography;

export const StudentProfilePage = (): JSX.Element => {
  const { studentId } = useParams<{ studentId: string }>();

  const [student, setStudent] = useState<any | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!studentId) {
      console.log(studentId)
      setError("Неверный ID студента");
      setLoading(false);
      return;
    }
  
    const fetchStudentPortrait = async () => {
      try {
        const studentIdNumber = parseInt(studentId, 10);
        console.log("Fetching data for studentId:", studentIdNumber);
        const response = await MephiApi.getStudentPortrait(studentIdNumber);
        console.log(response.data)
        setStudent(response.data);
      } catch (err: unknown) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError("Неизвестная ошибка");
        }
      } finally {
        setLoading(false);
      }
    };
  
    fetchStudentPortrait();
  }, [studentId]);
  

  if (loading) {
    return <Spin size="large" style={{ display: "block", margin: "auto" }} />;
  }

  if (error) {
    return <Alert message={error} type="error" showIcon />;
  }

  if (!student) {
    return <Alert message="Психологический портрет не найден" type="warning" showIcon />;
  }

  return (
    <Card
      style={{
        maxWidth: 800,
        margin: "40px auto",
        borderRadius: "16px",
        boxShadow: "0 4px 24px rgba(0,0,0,0.1)",
        padding: "24px"
      }}
    >
      <div style={{ display: "flex", alignItems: "center", marginBottom: 32 }}>
        <Avatar size={96} icon={<UserOutlined />} style={{ marginRight: 24 }} />
        <div>
          <Title level={3} style={{ margin: 0 }}>
            {student.fullName}
          </Title>
          <Paragraph type="secondary" style={{ marginBottom: 0 }}>
            Группа: {student.group}
          </Paragraph>
        </div>
      </div>

      <Descriptions
        title="Психологический профиль"
        layout="vertical"
        column={2}
        colon={false}
        style={{ marginBottom: 24 }}
      >
        <Descriptions.Item label="Тип темперамента">
          <Tag color="blue">
            <SmileOutlined /> {student.temperament}
          </Tag>
        </Descriptions.Item>
        <Descriptions.Item label="Репрезентативная система">
          <Tag color="purple">
            <BulbOutlined /> {student.representationalSystem}
          </Tag>
        </Descriptions.Item>
      </Descriptions>

      <Divider orientation="left">Черты личности</Divider>
      <List
        dataSource={student.traits}
        renderItem={(trait: { trait: string; value: string }) => (
          <List.Item>
            <Tag icon={<BookOutlined />} color="geekblue">
              {trait.trait}: {trait.value}
            </Tag>
          </List.Item>
        )}
        style={{ marginBottom: 32 }}
      />

      <Divider orientation="left">Рекомендуемые обучающие воздействия</Divider>
      <List
        dataSource={student.recommendations.split('\n')}  // Разделяем строку на части по переносу строки
        renderItem={(item: string) => <List.Item>📌 {item}</List.Item>}
      />
    </Card>
  );
};
