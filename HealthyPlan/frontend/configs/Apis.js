import axios from "axios";

import { clearSession, getAccessToken, getRefreshToken, notifySessionExpired, saveSession } from "./Session";

const rawApiUrl = process.env.EXPO_PUBLIC_API_URL;
const publicClientId = process.env.EXPO_PUBLIC_OAUTH_CLIENT_ID;
const apiUrl = rawApiUrl ? rawApiUrl.replace(/\/+$/, "") : "";
const oauthUrl = apiUrl.replace(/\/api$/, "");

export const endpoints = {
    users: "/users/",
    currentUser: "/users/current-user/",
    healthProfiles: "/health-profiles/",
    currentProfile: "/health-profiles/current-profile/",
    healthIssues: "/health-issues/",
    foods: "/foods/",
    foodDetails: (foodId) => `/foods/${foodId}/`,
    healthPlans: "/health-plans/",
    healthPlanDetails: (planId) => `/health-plans/${planId}/`,
    generateMealPlan: "/health-plans/generate-meal-plan/",
    consultations: "/consultations/",
    consultationSessions: "/consultations/sessions/",
    consultationSession: (sessionId) => `/consultations/sessions/${sessionId}/`,
    consultationMessages: (sessionId) => `/consultations/sessions/${sessionId}/messages/`
};

const configMessage = !apiUrl
    ? "Thiếu EXPO_PUBLIC_API_URL. Hãy cấu hình địa chỉ Backend trong file .env.local."
    : !apiUrl.endsWith("/api")
        ? "EXPO_PUBLIC_API_URL phải kết thúc bằng /api."
        : null;

const createConfigurationError = (message) => {
    const error = new Error(message);
    error.kind = "configuration";
    error.userMessage = message;
    return error;
}

const firstErrorMessage = (value) => {
    if (Array.isArray(value)) {
        return value.length > 0 ? firstErrorMessage(value[0]) : null;
    }

    if (value && typeof value === "object") {
        const firstKey = Object.keys(value)[0];
        return firstKey ? firstErrorMessage(value[firstKey]) : null;
    }

    return typeof value === "string" ? value : null;
}

export const normalizeApiError = (error) => {
    if (error.userMessage) {
        return error;
    }

    const statusCode = error.response?.status;
    const responseData = error.response?.data;
    error.statusCode = statusCode;
    error.fieldErrors = responseData && typeof responseData === "object" ? responseData : {};

    if (error.code === "ECONNABORTED") {
        error.kind = "timeout";
        error.userMessage = "Yêu cầu mất quá nhiều thời gian. Vui lòng thử lại.";
    } else if (!error.response) {
        error.kind = "network";
        error.userMessage = "Không thể kết nối máy chủ. Hãy kiểm tra mạng và địa chỉ API.";
    } else if (statusCode === 401) {
        error.kind = "unauthorized";
        error.userMessage = "Phiên đăng nhập không còn hợp lệ.";
    } else if (statusCode === 403) {
        error.kind = "forbidden";
        error.userMessage = "Bạn không có quyền thực hiện thao tác này.";
    } else if (statusCode === 404) {
        error.kind = "not_found";
        error.userMessage = firstErrorMessage(responseData) || "Không tìm thấy dữ liệu yêu cầu.";
    } else if (statusCode === 400) {
        error.kind = "validation";
        error.userMessage = firstErrorMessage(responseData) || "Thông tin chưa hợp lệ. Vui lòng kiểm tra lại.";
    } else if (statusCode >= 500) {
        error.kind = "server";
        error.userMessage = "Máy chủ đang gặp sự cố. Vui lòng thử lại sau.";
    } else {
        error.kind = "unknown";
        error.userMessage = "Không thể hoàn thành yêu cầu. Vui lòng thử lại.";
    }

    return error;
}

export const getErrorMessage = (error, fallback = "Không thể hoàn thành yêu cầu.") => {
    return error?.userMessage || fallback;
}

export const getFieldError = (error, field) => {
    return firstErrorMessage(error?.fieldErrors?.[field]);
}

export const requireResponseData = (response, message = "Máy chủ không trả về dữ liệu hợp lệ.") => {
    if (response?.data === undefined || response?.data === null) {
        const error = new Error(message);
        error.kind = "invalid_response";
        error.userMessage = message;
        throw error;
    }

    return response.data;
}

const toFormBody = (values) => {
    return Object.entries(values)
        .filter(([, value]) => value !== undefined && value !== null)
        .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
        .join("&");
}

const oauthClient = axios.create({baseURL: oauthUrl || "http://invalid.local", timeout: 20000});
const Apis = axios.create({
    baseURL: apiUrl || "http://invalid.local",
    timeout: 20000,
    headers: {Accept: "application/json"}
});

let refreshPromise = null;

const refreshAccessToken = async () => {
    if (!publicClientId) {
        throw createConfigurationError("Thiếu EXPO_PUBLIC_OAUTH_CLIENT_ID cho public OAuth client.");
    }

    const storedRefreshToken = getRefreshToken();
    if (!storedRefreshToken) {
        throw new Error("Không có refresh token.");
    }

    if (!refreshPromise) {
        const requestBody = toFormBody({grant_type: "refresh_token", refresh_token: storedRefreshToken, client_id: publicClientId});
        refreshPromise = oauthClient.post("/o/token/", requestBody, {headers: {"Content-Type": "application/x-www-form-urlencoded"}})
            .then(async (response) => {
                await saveSession(response.data);
                return response.data.access_token;
            })
            .finally(() => {
                refreshPromise = null;
            });
    }

    return refreshPromise;
}

Apis.interceptors.request.use((request) => {
    if (configMessage) {
        return Promise.reject(createConfigurationError(configMessage));
    }

    const token = getAccessToken();
    if (token) {
        request.headers.Authorization = `Bearer ${token}`;
    }

    return request;
});

Apis.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && getRefreshToken() && originalRequest && !originalRequest.hasRetried) {
            originalRequest.hasRetried = true;

            try {
                const token = await refreshAccessToken();
                originalRequest.headers.Authorization = `Bearer ${token}`;
                return Apis(originalRequest);
            } catch (refreshError) {
                await clearSession();
                notifySessionExpired();
                return Promise.reject(normalizeApiError(refreshError));
            }
        }

        return Promise.reject(normalizeApiError(error));
    }
);

export const authApis = {
    login: async (username, password) => {
        if (configMessage) {
            throw createConfigurationError(configMessage);
        }

        if (!publicClientId) {
            throw createConfigurationError("Thiếu EXPO_PUBLIC_OAUTH_CLIENT_ID cho public OAuth client.");
        }

        const requestBody = toFormBody({grant_type: "password", username, password, client_id: publicClientId});

        try {
            const response = await oauthClient.post("/o/token/", requestBody, {headers: {"Content-Type": "application/x-www-form-urlencoded"}});
            await saveSession(response.data);
            return response.data;
        } catch (error) {
            throw normalizeApiError(error);
        }
    },
    revoke: async () => {
        const token = getRefreshToken() || getAccessToken();
        if (!token || !publicClientId || configMessage) {
            return;
        }

        const requestBody = toFormBody({token, token_type_hint: getRefreshToken() ? "refresh_token" : "access_token", client_id: publicClientId});
        await oauthClient.post("/o/revoke_token/", requestBody, {headers: {"Content-Type": "application/x-www-form-urlencoded"}});
    }
};

export default Apis;
