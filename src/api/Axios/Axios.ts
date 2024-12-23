// eslint-disable-next-line import/no-named-as-default
import Axios, { AxiosInstance } from "axios";
import NProgress from "nprogress";

export class AxiosService {
  public axios: AxiosInstance;
  private numberOfAjaxCAllPending = 0;

  constructor() {
    this.axios = Axios.create({

      validateStatus: (status) => status >= 200 && status < 400,
      timeout: 30000,
      headers: {
        Accept: "application/json"
      }
    });

    this.axios.interceptors.response.use(
      (response) => {
        this.numberOfAjaxCAllPending--;
        if (this.numberOfAjaxCAllPending === 0) {
          NProgress.done(true);
        }
        return response;
      },
      async (error) => {
        this.numberOfAjaxCAllPending--;
        if (this.numberOfAjaxCAllPending === 0) {
          NProgress.done(true);
        }
        console.error("Ошибка запроса:", {
          url: error.config.url,
          status: error.response.status,
          data: error.response.data,
        });
    
        // Убедитесь, что обрабатываете случаи, когда `error.response` может отсутствовать
        if (error.response && error.response.data && error.response.data.detail) {
          return Promise.reject(error.response.data.detail);
        }
    
        return Promise.reject(error);
      }
    );
  }
};