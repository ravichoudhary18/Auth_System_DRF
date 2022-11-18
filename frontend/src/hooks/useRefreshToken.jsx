import axios from "axios";
// import { ReactSession } from "react-client-session";

const URL = 'http://127.0.0.1:8000/api/accounts/token/refresh/'

const useRefreshToken = () => {
  const refreshToken = localStorage.getItem("refreshToken");

  const refershToken = async () => {
    const response = await axios.post(
      URL,
      {
        refresh: refreshToken,
      }
    );
    // ReactSession.set("accessToken", response.data.access);
    localStorage.setItem("accessToken", response.data.access);

    return await response.data.access;
  };

  return refershToken;
};

export default useRefreshToken;
