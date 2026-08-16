import { ActivityIndicator, Pressable, StyleSheet, Text } from "react-native";
import Ionicons from "@expo/vector-icons/Ionicons";

import { Colors, Radius, Spacing } from "../configs/Theme";

const AppButton = ({title, onPress, loading = false, disabled = false, variant = "primary", icon, accessibilityLabel, style}) => {
    const isDisabled = disabled || loading;

    return (
        <Pressable
            accessibilityRole="button"
            accessibilityLabel={accessibilityLabel || title}
            disabled={isDisabled}
            onPress={onPress}
            style={({pressed}) => [styles.button, styles[variant], isDisabled && styles.disabled, pressed && !isDisabled && styles.pressed, style]}
        >
            {loading ? (
                <ActivityIndicator color={variant === "primary" ? Colors.surface : Colors.primary} />
            ) : (
                <>
                    {icon && <Ionicons name={icon} size={19} color={variant === "primary" ? Colors.surface : variant === "danger" ? Colors.error : Colors.primary} style={styles.icon} />}
                    <Text style={[styles.text, styles[`${variant}Text`]]}>{title}</Text>
                </>
            )}
        </Pressable>
    );
}

const styles = StyleSheet.create({
    button: {
        minHeight: 50,
        paddingHorizontal: Spacing.large,
        borderRadius: Radius.medium,
        flexDirection: "row",
        alignItems: "center",
        justifyContent: "center",
        borderWidth: 1
    },
    primary: {backgroundColor: Colors.primary, borderColor: Colors.primary},
    secondary: {backgroundColor: Colors.primaryLight, borderColor: Colors.primaryLight},
    outline: {backgroundColor: Colors.surface, borderColor: Colors.border},
    danger: {backgroundColor: "#FFF2F2", borderColor: "#F2CCCC"},
    disabled: {opacity: 0.55},
    pressed: {opacity: 0.82},
    icon: {marginRight: Spacing.small},
    text: {fontSize: 16, fontWeight: "700"},
    primaryText: {color: Colors.surface},
    secondaryText: {color: Colors.primaryDark},
    outlineText: {color: Colors.primaryDark},
    dangerText: {color: Colors.error}
});

export default AppButton;
