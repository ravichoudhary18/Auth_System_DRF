import axios from 'axios';
import useRefreshToken from './useRefreshToken'


const URL = 'http://localhost:8000/api/';


const useAxiosPrivate = () => {
  const refresh = useRefreshToken();
  const accessToken = localStorage.getItem('accessToken');

  const axiosPrivate = axios.create({
      baseURL: URL,
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
  });

  useEffect(() => {
    const requestIntercept = axiosPrivate.interceptors.request.use(
      (config) => {
        if (!config.headers.Authorization) {
          config.headers.Authorization = `Bearer ${accessToken}`;
        }
        return config;
      },

      (error) => Promise.reject(error)
    );

    const responseIntercept = axiosPrivate.interceptors.response.use(
      (response) => response,
      async (error) => {
        const prevRequest = error?.config;
        const message = error.response.data;

        if (
          error.response.status === 401 &&
          message === "Given token not valid for any token type"
        ) {
          const newAccessToken = await refresh();
          ReactSession.set("accessToken", newAccessToken);
          prevRequest.headers.Authorization = `Bearer ${newAccessToken}`;
          return axiosPrivate(prevRequest);
        }

        return Promise.reject(error);
      }
    );
    return () => {
      axiosPrivate.interceptors.request.eject(requestIntercept);
      axiosPrivate.interceptors.response.eject(responseIntercept);
    };

  }, [refresh, accessToken, axiosPrivate])

  return axiosPrivate;
};

export default useAxiosPrivate;