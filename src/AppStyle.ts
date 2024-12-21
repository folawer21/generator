import styled from "styled-components";

export const AppWrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100vw;
  height: 100vh;
  background: #f5f5f5;
`;

export const AppStyled = styled.div`
  display: flex;
  width: 100%;
  height: 100%;
  min-width: 800px;
  max-width: 1920px;
  min-height: 500px;
  max-height: 1440px;
  margin: 0;
`;

export const Header = styled.header`
  display: flex;
  justify-content: center;
  width: 100%;
  height: 64px;
  background: #001529;
`;

export const HeaderContent = styled.div`
  display: flex;
  align-items: center;
  width: 100%;
  min-width: 800px;
  max-width: 1920px;
  padding: 0 32px;
  gap: 40px;

  img {
    width: 44px;
    height: 44px;
  }
`;

export const Content = styled.main`
  display: flex;
  flex: 1 0 0;
  flex-direction: column;
  min-height: 300px;
  margin: 24px;
  padding: 24px;
  border-radius: 16px;
  background: rgb(255, 255, 255);
  overflow-y: auto;
`;
