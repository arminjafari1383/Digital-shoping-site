import Cookies from "js-cookie";

const ACCESS_TOKEN = "access_token";
const REFRESH_TOKEN = "refresh_token";

export const getAccessToken = () => Cookies.get(ACCESS_TOKEN);

export const getRefreshToken = () => Cookies.get(REFRESH_TOKEN);

export const setTokens = (
    access: string,
    refresh: string
) => {
    Cookies.set(ACCESS_TOKEN,access);
    Cookies.set(REFRESH_TOKEN, refresh);
};

export const clearTokens = () => {
    Cookies.remove(ACCESS_TOKEN);
    Cookies.remove(REFRESH_TOKEN);
}