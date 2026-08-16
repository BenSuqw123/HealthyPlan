import * as SecureStore from "expo-secure-store";

const SESSION_KEY = "healthyplan.oauth.session";

let accessToken = null;
let refreshToken = null;
let expiresAt = null;
let sessionExpiredHandler = null;

export const saveSession = async (tokenData) => {
    if (!tokenData || !tokenData.access_token) {
        throw new Error("Phản hồi đăng nhập không có access token.");
    }

    const session = {
        accessToken: tokenData.access_token,
        refreshToken: tokenData.refresh_token || refreshToken,
        expiresAt: Date.now() + Number(tokenData.expires_in || 0) * 1000
    };

    accessToken = session.accessToken;
    refreshToken = session.refreshToken;
    expiresAt = session.expiresAt;
    await SecureStore.setItemAsync(SESSION_KEY, JSON.stringify(session));

    return session;
}

export const loadSession = async () => {
    const storedSession = await SecureStore.getItemAsync(SESSION_KEY);

    if (!storedSession) {
        return null;
    }

    try {
        const session = JSON.parse(storedSession);
        accessToken = session.accessToken || null;
        refreshToken = session.refreshToken || null;
        expiresAt = session.expiresAt || null;

        return session;
    } catch (error) {
        await clearSession();
        return null;
    }
}

export const clearSession = async () => {
    accessToken = null;
    refreshToken = null;
    expiresAt = null;
    await SecureStore.deleteItemAsync(SESSION_KEY);
}

export const getAccessToken = () => accessToken;
export const getRefreshToken = () => refreshToken;
export const getTokenExpiresAt = () => expiresAt;

export const setSessionExpiredHandler = (handler) => {
    sessionExpiredHandler = handler;
}

export const notifySessionExpired = () => {
    if (sessionExpiredHandler) {
        sessionExpiredHandler();
    }
}
