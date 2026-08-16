import { createContext, useEffect, useReducer } from "react";

import Apis, { authApis, endpoints, getErrorMessage, requireResponseData } from "./Apis";
import { clearSession, loadSession, setSessionExpiredHandler } from "./Session";
import MyUserReducer, { initialUserState } from "../reducers/MyUserReducer";

export const MyUserContext = createContext();

export const MyUserProvider = ({children}) => {
    const [state, dispatch] = useReducer(MyUserReducer, initialUserState);

    const loadUserData = async () => {
        const userResponse = await Apis.get(endpoints.currentUser);
        const user = requireResponseData(userResponse, "Máy chủ không trả về thông tin người dùng.");
        let healthProfile = null;

        try {
            const profileResponse = await Apis.get(endpoints.currentProfile);
            healthProfile = requireResponseData(profileResponse, "Máy chủ không trả về hồ sơ sức khỏe.");
        } catch (error) {
            if (error.statusCode !== 404) {
                throw error;
            }
        }

        return {user, healthProfile};
    }

    const restoreUserSession = async () => {
        dispatch({type: "RESTORE_START"});

        try {
            const session = await loadSession();
            if (!session || (!session.accessToken && !session.refreshToken)) {
                dispatch({type: "RESTORE_ANONYMOUS"});
                return;
            }

            const userData = await loadUserData();
            dispatch({type: "RESTORE_SUCCESS", payload: userData});
        } catch (error) {
            if (error.statusCode === 401 || error.kind === "unauthorized") {
                await clearSession();
                dispatch({type: "RESTORE_ANONYMOUS"});
            } else {
                dispatch({type: "RESTORE_ERROR", payload: getErrorMessage(error)});
            }
        }
    }

    useEffect(() => {
        setSessionExpiredHandler(() => dispatch({type: "LOGOUT"}));
        restoreUserSession();

        return () => setSessionExpiredHandler(null);
    }, []);

    const login = async (username, password) => {
        await authApis.login(username, password);
        const userData = await loadUserData();
        dispatch({type: "LOGIN", payload: userData});
    }

    const logout = async () => {
        try {
            await authApis.revoke();
        } catch (error) {
            // Local logout must still finish when the server is unavailable.
        } finally {
            await clearSession();
            dispatch({type: "LOGOUT"});
        }
    }

    const updateUser = (user) => dispatch({type: "UPDATE_USER", payload: user});
    const updateHealthProfile = (profile) => dispatch({type: "UPDATE_HEALTH_PROFILE", payload: profile});

    const contextValue = {...state, login, logout, restoreUserSession, updateUser, updateHealthProfile};

    return <MyUserContext.Provider value={contextValue}>{children}</MyUserContext.Provider>;
}
