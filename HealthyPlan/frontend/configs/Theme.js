export const Colors = {
    primary: "#23865D",
    primaryDark: "#176846",
    primaryLight: "#E4F3EB",
    accent: "#D9A441",
    background: "#F5F9F6",
    surface: "#FFFFFF",
    text: "#17342A",
    textSecondary: "#63766F",
    border: "#DDE8E2",
    success: "#23865D",
    warning: "#D28B28",
    error: "#C75252",
    disabled: "#A8B7B0",
    overlay: "rgba(16, 39, 31, 0.45)"
};

export const Spacing = {
    tiny: 4,
    small: 8,
    medium: 16,
    large: 24,
    huge: 32
};

export const Radius = {
    small: 8,
    medium: 14,
    large: 20,
    round: 999
};

export const Shadow = {
    shadowColor: "#183F30",
    shadowOffset: {width: 0, height: 3},
    shadowOpacity: 0.08,
    shadowRadius: 8,
    elevation: 2
};

export const NavigationTheme = {
    dark: false,
    colors: {
        primary: Colors.primary,
        background: Colors.background,
        card: Colors.surface,
        text: Colors.text,
        border: Colors.border,
        notification: Colors.error
    },
    fonts: {
        regular: {fontFamily: "System", fontWeight: "400"},
        medium: {fontFamily: "System", fontWeight: "500"},
        bold: {fontFamily: "System", fontWeight: "700"},
        heavy: {fontFamily: "System", fontWeight: "800"}
    }
};
