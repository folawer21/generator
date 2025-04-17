import { Card } from "antd";

export const AuthorsTestsPage = (): JSX.Element => {
  return (
    <Card style={{ width: "100%", height: "100%", padding: 0 }}>
      <iframe
        src="http://185.17.141.230:1841/personality_tests"
        style={{ width: "100%", height: "100vh", border: "none" }}
        title="Embedded Page"
      ></iframe>
    </Card>
  );
};
