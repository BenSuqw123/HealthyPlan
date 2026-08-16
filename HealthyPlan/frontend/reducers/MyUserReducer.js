export const initialUserState = {
    user: null,
    healthProfile: null,
    restoring: true,
    restoreError: null
};

const MyUserReducer = (current, action) => {
    switch (action.type) {
        case "RESTORE_SUCCESS":
        case "LOGIN":
            return {...current, user: action.payload.user, healthProfile: action.payload.healthProfile, restoring: false, restoreError: null};
        case "RESTORE_ANONYMOUS":
            return {...initialUserState, restoring: false};
        case "RESTORE_ERROR":
            return {...current, restoring: false, restoreError: action.payload};
        case "RESTORE_START":
            return {...current, restoring: true, restoreError: null};
        case "UPDATE_USER":
            return {...current, user: action.payload};
        case "UPDATE_HEALTH_PROFILE":
            return {...current, healthProfile: action.payload};
        case "LOGOUT":
            return {...initialUserState, restoring: false};
        default:
            return current;
    }
}

export default MyUserReducer;
