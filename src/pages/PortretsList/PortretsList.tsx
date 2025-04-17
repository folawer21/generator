import React, { useEffect, useState } from "react";
import { Card, Collapse, List, Typography, Spin, message } from "antd";
import { useNavigate } from "react-router-dom";
import { MephiApi } from "src/api/mephi"; 
import { TGroupsList } from "src/api/mephi/types";

const { Panel } = Collapse;
const { Text } = Typography;

export const GroupsPage = (): JSX.Element => {
  const [groups, setGroups] = useState<[string, { id: number; full_name: string }[]][]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchGroups = async () => {
        try {
          const response = await MephiApi.getGroups();
          const data = response.data;
          
          // Логируем полученные данные
          console.log("Полученные данные:", data);

          const entries = Object.entries(data) as [string, { id: number; full_name: string }[]][];
          
          // Логируем результат преобразования данных
          console.log("Преобразованные данные:", entries);
          
          setGroups(entries);
        } catch (error) {
          message.error("Ошибка при загрузке групп");
        } finally {
          setLoading(false);
        }
      };

    fetchGroups();
  }, []);

  const handleStudentClick = (studentId: number) => {
    navigate(`/student/${studentId}`);
  };

  return (
    <Card
      title="Список студенческих групп"
      style={{ maxWidth: 800, margin: "30px auto" }}
    >
      {loading ? (
        <Spin size="large" />
      ) : (
        <Collapse accordion>
          {groups.map(([groupName, students]) => (
            <Panel header={groupName} key={groupName}>
              <List
                bordered
                dataSource={students}
                renderItem={(student) => {
                  if (!student.full_name) {
                    console.error('Ошибка: Студент не имеет имени', student);
                  }
                  return (
                    <List.Item
                      style={{
                        cursor: "pointer",
                        padding: "10px",
                        backgroundColor: "#f0f0f0",
                      }}
                      onClick={() => handleStudentClick(student.id)}
                    >
                      <div>{student.full_name || "Нет имени"}</div>
                    </List.Item>
                  );
                }}
                locale={{ emptyText: "Нет студентов в группе" }}
              />
            </Panel>
          ))}
        </Collapse>
      )}
    </Card>
  );
};
